import { getDb, getClient } from "../config/db.mjs";

export class AllocationWorker {
  constructor(db = null) {
    this.db = db;
  }

  getDatabase() {
    return this.db || getDb();
  }

  /**
   * Executes atomic Single-Document Compare-And-Swap (CAS) with OCC version guard
   */
  async attemptAtomicCas(targetDepot, requestedQty, incidentId) {
    const db = this.getDatabase();

    const result = await db.collection("resource_inventory").updateOne(
      {
        _id: targetDepot._id,
        __v: targetDepot.__v,                        // Optimistic Concurrency version check
        availableQuantity: { $gte: requestedQty },  // Authoritative capacity guardrail
        status: "available"
      },
      {
        $inc: { availableQuantity: -requestedQty, __v: 1 },
        $push: {
          allocations: {
            $each: [{ incidentId, qty: requestedQty, at: new Date() }],
            $slice: -10 // Bound embedded array length to prevent hot document bloat
          }
        }
      }
    );

    return result.modifiedCount === 1;
  }

  /**
   * High-contention reservation worker with Full Jitter and Randomized Candidate Window
   */
  async claimResourceWithRematch(incidentId, initialCandidate, candidatesShortlist, requestedQty, maxRetries = 3) {
    const db = this.getDatabase();
    let target = initialCandidate;
    let attempts = 0;

    console.log(`\n[OCC ALLOCATION] Initiating claim for Incident: ${incidentId} | Target: ${target._id} (${target.depotCode}) | Demand: ${requestedQty} units`);

    while (attempts < maxRetries) {
      attempts++;
      console.log(`  [Attempt #${attempts}] Testing CAS Predicate on Depot ${target._id} (Expected __v: ${target.__v}, Needed >= ${requestedQty} units)...`);

      const startTime = Date.now();
      const success = await this.attemptAtomicCas(target, requestedQty, incidentId);
      const elapsedMs = Date.now() - startTime;

      if (success) {
        console.log(`  ✓ [CAS COMMITTED] Allocation succeeded in ${elapsedMs}ms! Depot: ${target._id}, Decremented: ${requestedQty} units, Version bumped.`);

        // Append non-repudiable audit ledger entry
        await db.collection("audit_logs").insertOne({
          incidentId,
          resourceId: target._id,
          depotCode: target.depotCode,
          allocatedQty: requestedQty,
          versionAtCommit: target.__v + 1,
          strategy: "SINGLE_DOC_OCC_CAS",
          attempts,
          timestamp: new Date()
        });

        // Fetch refreshed depot state
        const refreshedDepot = await db.collection("resource_inventory").findOne({ _id: target._id });

        return {
          success: true,
          allocatedDepotId: target._id,
          depotCode: target.depotCode,
          remainingQuantity: refreshedDepot.availableQuantity,
          newVersion: refreshedDepot.__v,
          attempts,
          elapsedMs
        };
      }

      // Predicate failed: Contention occurred (modifiedCount === 0)
      console.warn(`  ✕ [CAS PREDICATE FAILED] Depot ${target._id} condition violated (stale __v or insufficient stock). Cheap failure in ${elapsedMs}ms.`);

      if (attempts >= maxRetries) break;

      // 1. Calculate Exponential Backoff with Full Jitter algorithm:
      // t_backoff = random(0, min(T_max, T_base * 2^attempts))
      const maxBackoff = Math.min(1000, 50 * Math.pow(2, attempts));
      const jitterMs = Math.floor(Math.random() * maxBackoff);
      console.log(`  [THUNDERING HERD DEFENSE] Applying Full Jitter Backoff: sleeping ${jitterMs}ms before rematch...`);
      await new Promise(r => setTimeout(r, jitterMs));

      // 2. Randomized Selection Window across top-3 candidates from the shortlist
      const availablePool = candidatesShortlist.filter(c => c._id !== target._id).slice(0, 3);
      if (!availablePool.length) {
        console.warn(`  [REMATCH] No alternative candidates remain in shortlist.`);
        break;
      }

      // Random selection avoids lock convoying where all losers crash into Candidate #2
      const candidateIndex = Math.floor(Math.random() * availablePool.length);
      const chosenCandidate = availablePool[candidateIndex];

      // Refresh candidate state from authoritative DB before next attempt
      const authoritativeCandidate = await db.collection("resource_inventory").findOne({ _id: chosenCandidate._id });
      if (authoritativeCandidate && authoritativeCandidate.availableQuantity >= requestedQty) {
        target = authoritativeCandidate;
        console.log(`  [REMATCH] Redirecting to randomized candidate: ${target._id} (${target.depotCode}) [Avail: ${target.availableQuantity}, __v: ${target.__v}]`);
      } else {
        console.warn(`  [REMATCH] Alternate candidate ${chosenCandidate._id} also depleted. Retrying pool...`);
      }
    }

    // Rematch Circuit Breaker Tripped!
    console.error(`  [CIRCUIT BREAKER TRIPPED] Contention limit exceeded (${attempts} attempts). Escalating to Regional Supervisor Queue!`);
    return {
      success: false,
      reason: "CONCURRENT_ALLOCATION_EXHAUSTED",
      circuitBreakerTripped: true,
      attempts
    };
  }

  /**
   * Cross-Collection Multi-Document ACID Transaction (Missions + Inventory + Audit)
   */
  async commitMissionWithTransaction(missionData, depotId, requestedQty) {
    const client = getClient();
    const session = client.startSession();

    try {
      let transactionResult = null;
      await session.withTransaction(async () => {
        const db = this.getDatabase();

        // 1. Authoritative decrement on depot
        const depotUpdate = await db.collection("resource_inventory").updateOne(
          { _id: depotId, availableQuantity: { $gte: requestedQty }, status: "available" },
          { $inc: { availableQuantity: -requestedQty, __v: 1 } },
          { session }
        );

        if (depotUpdate.modifiedCount === 0) {
          throw new Error("INSUFFICIENT_INVENTORY_IN_TRANSACTION");
        }

        // 2. Insert active mission
        const missionInsert = await db.collection("active_missions").insertOne(
          {
            ...missionData,
            status: "in_transit",
            allocatedAt: new Date(),
            __v: 0
          },
          { session }
        );

        // 3. Immutable audit ledger
        await db.collection("audit_logs").insertOne(
          {
            missionId: missionInsert.insertedId,
            resourceId: depotId,
            allocatedQty: requestedQty,
            strategy: "MULTI_DOC_ACID_TRANSACTION",
            timestamp: new Date()
          },
          { session }
        );

        transactionResult = {
          success: true,
          missionId: missionInsert.insertedId,
          allocatedDepotId: depotId
        };
      });

      return transactionResult;
    } finally {
      await session.endSession();
    }
  }
}
