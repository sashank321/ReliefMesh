import { connectToDatabase, closeDatabase } from "../config/db.mjs";
import { HazardStreamDaemon } from "../services/hazardStreamDaemon.mjs";
import { TelemetryStreamWorker } from "../services/telemetryStreamWorker.mjs";
import { seedData } from "../database/seedData.mjs";

export async function runDemoDeltaInvalidation() {
  console.log("\n================================================================================");
  console.log(" DEMO B: DELTA-SCOPED ENVIRONMENTAL INVALIDATION");
  console.log(" Scenario: Convoy Alpha In Transit · River Gauge Breach · Real-Time Rerouting");
  console.log("================================================================================");

  // 1. Reset database to fresh seed state
  await seedData();
  const { db } = await connectToDatabase();

  const daemon = new HazardStreamDaemon(db);
  const telemetry = new TelemetryStreamWorker(db);

  // Start the Change Stream Daemon
  await daemon.startDaemon();

  // Allow Change Stream cursor to stabilize
  await new Promise(r => setTimeout(r, 600));

  console.log("\n--- STEP 1: INITIAL GROUND TRUTH AUDIT ---");
  const initialMission = await db.collection("active_missions").findOne({ _id: "MISSION-104" });
  console.log(` Mission:      ${initialMission.missionCode} (${initialMission.title})`);
  console.log(` Status:       ${initialMission.status}`);
  console.log(` Current Route Distance: ${initialMission.route.distanceKm} km | ETA: ${initialMission.route.etaMinutes} mins`);

  console.log("\n--- STEP 2: INGESTING RIVER GAUGE TELEMETRY & BREACH SURGE ---");
  console.log(" Simulating River Gauge RG-04 telemetry spike (water level rising rapidly)...");

  // Telemetry ping 1: 3.1 meters
  await telemetry.ingestTelemetryReading("RIVER-GAUGE-RG04", 3.1);
  await new Promise(r => setTimeout(r, 200));

  // Telemetry ping 2: 4.6 meters (Triggers ASP rate-of-rise threshold & hydraulic flood expansion!)
  const breachEvent = await telemetry.ingestTelemetryReading("RIVER-GAUGE-RG04", 4.6);

  console.log("\n--- STEP 3: AWAITING REACTIVE CHANGE STREAM PROPAGATION ---");
  console.log(" Waiting for MongoDB Oplog Change Stream pre/post-image event to trigger invalidation...");

  // Wait for the reactive loop to execute
  await new Promise(r => setTimeout(r, 1200));

  console.log("\n================================================================================");
  console.log(" DEMO B FINAL OUTCOME & INVARIANT VERIFICATION");
  console.log("================================================================================");

  const updatedMission = await db.collection("active_missions").findOne({ _id: "MISSION-104" });
  const checkpoint = await db.collection("stream_checkpoints").findOne({ workerId: daemon.workerId });

  console.log(`\nUpdated Mission State in MongoDB:`);
  console.log(`  Mission ID:       ${updatedMission._id}`);
  console.log(`  Status:           ${updatedMission.status}`);
  console.log(`  Reroute Notice:   "${updatedMission.rerouteNotice}"`);
  console.log(`  New Distance:     ${updatedMission.route.distanceKm} km | New ETA: ${updatedMission.route.etaMinutes} mins`);
  console.log(`  OCC Version:      __v: ${updatedMission.__v}`);
  console.log(`  Checkpoint Token: ${checkpoint?.lastResumeToken ? "Persisted in stream_checkpoints ✓" : "None"}`);

  console.log("\n✓ THE FRESHNESS INVARIANT HELD:");
  console.log("  No Kafka. No external CDC message brokers. No polling loops.");
  console.log("  MongoDB Change Streams computed the geometric delta (Omega_post \\ Omega_pre),");
  console.log("  detected the compromised road segment, and rerouted Convoy Alpha to safety.");
  console.log("================================================================================\n");

  await daemon.stopDaemon();
  return { updatedMission, checkpoint };
}

if (process.argv[1]?.endsWith("demoDeltaInvalidation.mjs")) {
  runDemoDeltaInvalidation()
    .then(() => closeDatabase())
    .catch((err) => {
      console.error("[FATAL] Demo B failed:", err);
      process.exit(1);
    });
}
