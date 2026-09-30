import { connectToDatabase, closeDatabase } from "../config/db.mjs";

export async function bootstrapDatabase() {
  const { db } = await connectToDatabase();
  console.log("================================================================================");
  console.log(" RELIEFMESH: MONGODB OPERATIONAL CORE BOOTSTRAP & SCHEMA INITIALIZATION");
  console.log(" Target: MongoDB 8.3 Replica Set (Single Control Plane)");
  console.log("================================================================================");

  const collections = [
    "living_incidents",
    "resource_inventory",
    "hazard_perimeters",
    "active_missions",
    "synonym_mappings",
    "stream_checkpoints",
    "audit_logs",
    "sensor_telemetry",
    "processed_events",
    "agent_registry",
    "live_slo_metrics"
  ];

  const existingCollections = (await db.listCollections().toArray()).map(c => c.name);

  for (const name of collections) {
    if (!existingCollections.includes(name)) {
      await db.createCollection(name);
      console.log(`[SCHEMA] Created collection: ${name}`);
    } else {
      console.log(`[SCHEMA] Verified collection exists: ${name}`);
    }
  }

  // 1. Enable Change Stream Pre- and Post-Images for Hazard Perimeters & Missions
  console.log("\n[REACTIVITY] Enabling Change Stream Pre/Post Images...");
  try {
    await db.command({
      collMod: "hazard_perimeters",
      changeStreamPreAndPostImages: { enabled: true }
    });
    console.log("  ✓ Enabled pre/post-images on: hazard_perimeters");
  } catch (err) {
    console.warn("  ! Note on hazard_perimeters pre/post-images:", err.message);
  }

  try {
    await db.command({
      collMod: "active_missions",
      changeStreamPreAndPostImages: { enabled: true }
    });
    console.log("  ✓ Enabled pre/post-images on: active_missions");
  } catch (err) {
    console.warn("  ! Note on active_missions pre/post-images:", err.message);
  }

  try {
    await db.command({
      collMod: "resource_inventory",
      changeStreamPreAndPostImages: { enabled: true }
    });
    console.log("  ✓ Enabled pre/post-images on: resource_inventory");
  } catch (err) {
    console.warn("  ! Note on resource_inventory pre/post-images:", err.message);
  }

  // 2. Build 2dsphere Geospatial Indexes
  console.log("\n[SPATIAL] Creating 2dsphere Geospatial Indexes...");
  await db.collection("resource_inventory").createIndex({ location: "2dsphere" }, { name: "idx_depot_2dsphere" });
  console.log("  ✓ Created 2dsphere index on resource_inventory.location");

  await db.collection("hazard_perimeters").createIndex({ polygon: "2dsphere" }, { name: "idx_hazard_2dsphere" });
  console.log("  ✓ Created 2dsphere index on hazard_perimeters.polygon");

  await db.collection("active_missions").createIndex({ "route.geometry": "2dsphere" }, { name: "idx_route_2dsphere" });
  console.log("  ✓ Created 2dsphere index on active_missions.route.geometry");

  await db.collection("living_incidents").createIndex({ location: "2dsphere" }, { name: "idx_incident_2dsphere" });
  console.log("  ✓ Created 2dsphere index on living_incidents.location");

  // 3. Build Operational & Concurrency Indexes
  console.log("\n[PERFORMANCE] Creating Operational & OCC Indexes...");
  await db.collection("resource_inventory").createIndex(
    { status: 1, availableQuantity: -1, depotCode: 1 },
    { name: "idx_depot_availability" }
  );
  await db.collection("resource_inventory").createIndex(
    { itemDescription: "text", category: "text" },
    { name: "idx_depot_text_lexical" }
  );

  await db.collection("active_missions").createIndex(
    { status: 1, priority: -1 },
    { name: "idx_missions_status_prio" }
  );

  await db.collection("stream_checkpoints").createIndex(
    { workerId: 1 },
    { unique: true, name: "idx_worker_checkpoint_uniq" }
  );

  await db.collection("sensor_telemetry").createIndex(
    { sensorId: 1, timestamp: -1 },
    { name: "idx_sensor_ts" }
  );

  await db.collection("audit_logs").createIndex(
    { timestamp: -1, resourceId: 1 },
    { name: "idx_audit_timeline" }
  );

  // 4. Agent Heartbeat Registry with MongoDB Native TTL Index (30s Expiry)
  console.log("\n[CONSENSUS] Creating Agent Registry TTL Index...");
  await db.collection("agent_registry").createIndex(
    { lastHeartbeat: 1 },
    { expireAfterSeconds: 30, name: "idx_agent_ttl_heartbeat" }
  );
  await db.collection("agent_registry").createIndex(
    { agentId: 1 },
    { unique: true, name: "idx_agent_id_uniq" }
  );

  // 5. Change Stream Event Idempotency & SLO Telemetry Indexes
  console.log("\n[RELIABILITY] Creating Event Idempotency & SLO Indexes...");
  await db.collection("processed_events").createIndex(
    { eventId: 1 },
    { unique: true, name: "idx_event_dedup_uniq" }
  );
  await db.collection("processed_events").createIndex(
    { processedAt: 1 },
    { expireAfterSeconds: 86400, name: "idx_processed_events_ttl" } // 24-hr TTL
  );
  await db.collection("live_slo_metrics").createIndex(
    { recordedAt: -1 },
    { name: "idx_slo_recorded_ts" }
  );

  console.log("\n================================================================================");
  console.log(" RELIEFMESH DATABASE BOOTSTRAP COMPLETED SUCCESSFULLY");
  console.log("================================================================================");
}

// Allow direct execution
if (process.argv[1]?.endsWith("bootstrapDatabase.mjs")) {
  bootstrapDatabase()
    .then(() => closeDatabase())
    .catch((err) => {
      console.error("[FATAL] Bootstrap failed:", err);
      process.exit(1);
    });
}
