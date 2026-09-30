# ReliefMesh: Operational Crisis Coordination Engine

> **The Freshness Invariant:** *No operational allocation may outlive its physical ground truth.*

```
$$\mathbf{The\ Freshness\ Invariant:}\quad \forall a \in \mathcal{A}_{\text{active}},\; \Delta t(a) \le t_{\text{oplog\_propagation}} + t_{\text{spatial\_eval}} + t_{\text{worker\_commit}}$$
```

ReliefMesh is an operational crisis coordination engine designed for MongoDB Atlas / MongoDB 8.1+ Core Engine. It solves **Operational State Drift** by unifying situational awareness and scarce resource allocation into a single transactional state control plane.

---

## 🏗️ Architecture: The 4-R Operational Spine

```
 ┌────────────────────────────────────────────────────────────────────────────────────────┐
 │                              MONGODB ATLAS 8.1+ CORE ENGINE                            │
 │                                                                                        │
 │  [1. RELEVANT]       [2. REACHABLE]         [3. RESERVED]          [4. RESILIENT]      │
 │  Hybrid Retrieval    Spatial Gating         Atomic OCC Commit      Delta Invalidation  │
 │  -----------------   -----------------      ------------------     ------------------  │
 │  • Lucene Synonyms   • 2dsphere indexing    • Single-doc CAS       • Change Streams    │
 │  • Vector Embeddings • Boundary pruning     • Predicate check      • Pre/Post Images   │
 │  • Uniform RRF       • OSRM road sidecar    • Full jitter retry    • Spatial Δ diff    │
 │  • Fallback Probe    • Spatial exclusion    • Randomized window    • Auto-reroute      │
 └────────────────────────────────────────────────────────────────────────────────────────┘
```

---

## ⚡ Quickstart

### Prerequisites
- Node.js v20+ (Running on Node v25)
- MongoDB 8.x Replica Set (`rs0` active on port 27018)

### Running the Live System

```bash
# 1. Run the complete automated demo evaluation suite (Demo A & Demo B)
npm run demo:all

# 2. Run Demo A: Deterministic Concurrency Race & Self-Healing Retrieval
npm run demo:race

# 3. Run Demo B: Delta-Scoped Environmental Invalidation & Real-Time Rerouting
npm run demo:delta

# 4. Start the Live Operational Server & Dispatcher Web Console
npm start
# Opens on http://localhost:3000
```

---

## 🔬 Core Database Primitives Implemented

### 1. Stage 1 & 2: Relevant & Reachable (`src/services/adaptiveRetrievalService.mjs`)
* **Vernacular Synonym Normalization:** Maps colloquial dialects (*"khoon"* → blood, *"dawa"* → medicine, *"paani"* → flood) natively using the `synonym_mappings` collection without costly cloud LLM roundtrips.
* **Recall Probe (`$searchMeta`):** Evaluates candidate availability before dispatch. Automatically widens spatial radius from 50km to 100km if matches `< 3`.
* **Adaptive Circuit Breaker:** Wraps external vector embedding APIs in a strict 3,000ms timeout. Gracefully degrades from `FULL_HYBRID` to `DEGRADED_LEXICAL_GEO` mode during field network outages.
* **Uniform Reciprocal Rank Fusion (`$rankFusion` / RRF):** Fuses lexical Lucene rankings and spatial proximity distances into a single authoritative candidate ranking.

### 2. Stage 3: Reserved (`src/services/allocationWorker.mjs`)
* **Single-Document Optimistic Concurrency Control (OCC):**
  ```javascript
  db.resource_inventory.updateOne(
    { _id: targetDepotId, __v: version, availableQuantity: { $gte: requestedQty }, status: "available" },
    {
      $inc: { availableQuantity: -requestedQty, __v: 1 },
      $push: { allocations: { $each: [{ incidentId, qty, at: new Date() }], $slice: -10 } }
    }
  );
  ```
* **Bounded Allocation History:** Enforces `$slice: -10` on the embedded allocation history array to prevent document bloat and memory fragmentation under high contention.
* **Cheap Failed Predicate:** Contention surfaces as `modifiedCount: 0` in `<5ms` without expensive multi-row lock waits or distributed locks.
* **Thundering Herd Defense:** Applies **Exponential Backoff with Full Jitter** and selects randomly across a **Randomized Candidate Window** (top-3 candidates) so competing dispatchers don't crash into the same fallback depot.

### 3. Stage 4: Resilient (`src/services/hazardStreamDaemon.mjs`)
* **Change Streams with Pre- and Post-Images:**
  ```javascript
  db.command({ collMod: "hazard_perimeters", changeStreamPreAndPostImages: { enabled: true } });
  ```
* **Geometric Spatial Delta ($\Delta \Omega$):**
  $$\Delta \Omega = \Omega_{\text{post}} \setminus \Omega_{\text{pre}}$$
  Evaluates **only** the newly flooded expansion difference rather than scanning the entire historical map.
* **Delta-Scoped Invalidation:** Executes `$geoIntersects` exclusively on the spatial delta geometry against active `in_transit` missions.
* **Automated Detour Rerouting:** Automatically flags compromised missions (`route_compromised`) and generates safe bypass trajectories.
* **Cold-Start Resync Protocol:** Detects `ChangeStreamHistoryLost` (code 286), falls back to a full active scan, and re-establishes the Change Stream cursor.

---

## 🖥️ Live Dispatcher Web Console (`http://localhost:3000`)
* **Interactive SVG Map:** Visualizes Sector 7 depots, active convoy trajectories, river gauge pings, and expanding flood hazard polygons in real time.
* **Live WebSocket Feed:** Streams real-time oplog push notifications directly from the MongoDB Replica Set.
* **Interactive Trigger Buttons:**
  * **⚡ Trigger Concurrency Race:** Replays Ambulance 14 vs Mobile Surgical Unit 3 contesting 5 blood units.
  * **🌊 Trigger Flood Breach:** Ingests river gauge surge and watches the Change Stream invalidate and reroute Convoy Alpha live.
  * **🔄 Reseed Baseline State:** Restores authoritative seed ground truth.
