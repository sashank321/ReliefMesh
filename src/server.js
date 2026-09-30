import express from "express";
import http from "http";
import { WebSocketServer, WebSocket } from "ws";
import cors from "cors";
import path from "path";
import { fileURLToPath } from "url";
import { connectToDatabase, getDb } from "./config/db.mjs";
import { bootstrapDatabase } from "./database/bootstrapDatabase.mjs";
import { seedData } from "./database/seedData.mjs";
import { AdaptiveRetrievalService } from "./services/adaptiveRetrievalService.mjs";
import { AllocationWorker } from "./services/allocationWorker.mjs";
import { HazardStreamDaemon } from "./services/hazardStreamDaemon.mjs";
import { TelemetryStreamWorker } from "./services/telemetryStreamWorker.mjs";

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

const app = express();
const server = http.createServer(app);
const wss = new WebSocketServer({ server });

app.use(cors());
app.use(express.json());
app.use(express.static(path.join(__dirname, "../public")));

let retrievalService = null;
let allocationWorker = null;
let hazardDaemon = null;
let telemetryWorker = null;

// Helper to broadcast JSON over WebSockets
function broadcast(type, payload) {
  const message = JSON.stringify({ type, payload, timestamp: new Date() });
  wss.clients.forEach(client => {
    if (client.readyState === WebSocket.OPEN) {
      client.send(message);
    }
  });
}

// WebSocket Connection Lifecycle
wss.on("connection", async (ws) => {
  try {
    const db = getDb();
    const isMaster = await db.command({ hello: 1 });
    ws.send(JSON.stringify({
      type: "SYSTEM_CONNECTED",
      payload: {
        engine: "MongoDB 8.3 Replica Set (Primary)",
        setName: isMaster.setName,
        time: new Date()
      }
    }));
  } catch (err) {
    console.error("WS Handshake error:", err);
  }
});

// REST API Endpoints

// 1. Cluster Status & Architecture Invariants
app.get("/api/status", async (req, res) => {
  try {
    const db = getDb();
    const isMaster = await db.command({ hello: 1 });
    const [depotsCount, missionsCount, hazardsCount, auditsCount] = await Promise.all([
      db.collection("resource_inventory").countDocuments(),
      db.collection("active_missions").countDocuments(),
      db.collection("hazard_perimeters").countDocuments(),
      db.collection("audit_logs").countDocuments()
    ]);

    res.json({
      success: true,
      engine: "MongoDB Atlas / 8.3 Replica Set",
      replicaSet: isMaster.setName,
      isPrimary: isMaster.isWritablePrimary,
      daemonActive: hazardDaemon?.isRunning ?? false,
      stats: { depotsCount, missionsCount, hazardsCount, auditsCount }
    });
  } catch (err) {
    res.status(500).json({ success: false, error: err.message });
  }
});

// 2. Full State Aggregation
app.get("/api/state", async (req, res) => {
  try {
    const db = getDb();
    const [depots, missions, hazards, audits, telemetry, synonyms, incidents] = await Promise.all([
      db.collection("resource_inventory").find({}).toArray(),
      db.collection("active_missions").find({}).toArray(),
      db.collection("hazard_perimeters").find({}).toArray(),
      db.collection("audit_logs").find({}).sort({ timestamp: -1 }).limit(15).toArray(),
      db.collection("sensor_telemetry").find({}).sort({ timestamp: -1 }).limit(10).toArray(),
      db.collection("synonym_mappings").find({}).toArray(),
      db.collection("living_incidents").find({}).toArray()
    ]);

    res.json({ success: true, depots, missions, hazards, audits, telemetry, synonyms, incidents });
  } catch (err) {
    res.status(500).json({ success: false, error: err.message });
  }
});

// 3. Stage 1 & 2: 4-R Adaptive Retrieval (Synonyms + Vector + 2dsphere + RRF)
app.post("/api/retrieve", async (req, res) => {
  try {
    const { query, coordinates, simulateTimeout, maxCandidates = 5 } = req.body;
    const coords = coordinates || [80.2680, 13.0810];
    const result = await retrievalService.retrieveCandidates(query || "blood", coords, {
      simulateApiTimeout: simulateTimeout ?? false,
      maxCandidates
    });
    res.json({ success: true, ...result });
  } catch (err) {
    res.status(500).json({ success: false, error: err.message });
  }
});

// 4. Stage 3: Atomic OCC Allocation (Single-Document CAS)
app.post("/api/allocate", async (req, res) => {
  try {
    const { incidentId, targetDepotId, requestedQty } = req.body;
    const db = getDb();
    const target = await db.collection("resource_inventory").findOne({ _id: targetDepotId });
    if (!target) return res.status(404).json({ success: false, error: "Target Depot not found" });

    const candidates = await db.collection("resource_inventory").find({ status: "available" }).toArray();
    const result = await allocationWorker.claimResourceWithRematch(
      incidentId || "INC-DISPATCHER",
      target,
      candidates,
      requestedQty || 4,
      3
    );

    broadcast("ALLOCATION_COMMITTED", result);
    res.json({ success: true, result });
  } catch (err) {
    res.status(500).json({ success: false, error: err.message });
  }
});

// 5. High-Contention Concurrency Stress Race (Configurable N Dispatchers)
app.post("/api/demo/race", async (req, res) => {
  try {
    const db = getDb();
    const { count = 2, targetDepotId = "DEPOT-001", demand = 4 } = req.body;
    const candidates = await db.collection("resource_inventory").find({ status: "available" }).toArray();
    const target = await db.collection("resource_inventory").findOne({ _id: targetDepotId });

    if (!target) return res.status(404).json({ success: false, error: "Target depot not found" });

    broadcast("RACE_ENGAGED", { depotId: target._id, initialStock: target.availableQuantity, count });

    // Spawn N concurrent claims with slight microsecond offsets
    const promises = Array.from({ length: count }).map((_, idx) => {
      return (async () => {
        if (idx > 0) await new Promise(r => setTimeout(r, idx * 3));
        const incidentCode = `INC-RACE-AGENT-${idx + 1}`;
        return allocationWorker.claimResourceWithRematch(incidentCode, target, candidates, demand, 3);
      })();
    });

    const results = await Promise.all(promises);

    const winners = results.filter(r => r.success && r.allocatedDepotId === targetDepotId);
    const rematches = results.filter(r => r.success && r.allocatedDepotId !== targetDepotId);
    const exhausted = results.filter(r => !r.success);

    broadcast("RACE_RESOLVED", {
      total: count,
      targetDepotId,
      winnersCount: winners.length,
      rematchesCount: rematches.length,
      exhaustedCount: exhausted.length,
      results
    });

    res.json({ success: true, total: count, results, winners, rematches, exhausted });
  } catch (err) {
    res.status(500).json({ success: false, error: err.message });
  }
});

// 6. Stage 4: Trigger Flood Breach & River Gauge Spike
app.post("/api/demo/flood", async (req, res) => {
  try {
    const { level = 4.8, sensorId = "RIVER-GAUGE-RG04" } = req.body;
    broadcast("TELEMETRY_SPIKE", { sensorId, level });

    const breachResult = await telemetryWorker.ingestTelemetryReading(sensorId, level);
    res.json({ success: true, breachResult });
  } catch (err) {
    res.status(500).json({ success: false, error: err.message });
  }
});

// 7. Restock Depots
app.post("/api/depots/restock", async (req, res) => {
  try {
    const db = getDb();
    const { depotId, amount = 10 } = req.body;
    const filter = depotId ? { _id: depotId } : {};
    
    await db.collection("resource_inventory").updateMany(
      filter,
      {
        $inc: { availableQuantity: amount, __v: 1 },
        $set: { status: "available", updatedAt: new Date() }
      }
    );

    broadcast("DEPOTS_RESTOCKED", { depotId: depotId || "ALL", amount });
    res.json({ success: true, message: `Restocked depots (+${amount} units)` });
  } catch (err) {
    res.status(500).json({ success: false, error: err.message });
  }
});

// 8. Reseed Entire Ground Truth
app.post("/api/reset", async (req, res) => {
  try {
    await seedData();
    broadcast("STATE_RESET", { message: "Database reseeded to authoritative ground truth baseline." });
    res.json({ success: true, message: "State successfully reseeded." });
  } catch (err) {
    res.status(500).json({ success: false, error: err.message });
  }
});

// 9. Voice Audio Emergency Ingestion (Whisper AI Simulation + Vernacular Mapping)
app.post("/api/voice/ingest", async (req, res) => {
  try {
    const { audioText = "bhaiya bypass pe paani bhar gaya khoon aur dawa chahiye", coordinates = [80.2680, 13.0810] } = req.body;
    
    // Simulates Whisper multilingual transcription & normalized dialect extraction
    const transcription = {
      rawTranscribedText: audioText,
      detectedLanguage: "hi-IN (Hindi Dialect)",
      confidence: 0.96,
      extractedSKUs: ["BLOOD-O-NEG", "MEDICINE-SURGICAL"],
      inferredUrgency: "CRITICAL"
    };

    broadcast("VOICE_INGESTED", transcription);

    // Pipe directly into 4-R Adaptive Retrieval
    const retrievalResult = await retrievalService.retrieveCandidates(audioText, coordinates, {
      simulateApiTimeout: false,
      maxCandidates: 5
    });

    res.json({
      success: true,
      transcription,
      retrieval: retrievalResult
    });
  } catch (err) {
    res.status(500).json({ success: false, error: err.message });
  }
});

// 10. Vehicle Live Waypoint Movement Simulation
app.post("/api/missions/simulate-movement", async (req, res) => {
  try {
    const { missionId = "MISSION-104", stepIndex = 0 } = req.body;
    const db = getDb();
    const mission = await db.collection("active_missions").findOne({ _id: missionId });
    if (!mission) return res.status(404).json({ success: false, error: "Mission not found" });

    const coordinates = mission.route.geometry.coordinates;
    const targetCoord = coordinates[Math.min(stepIndex, coordinates.length - 1)];

    broadcast("VEHICLE_MOVED", {
      missionId,
      stepIndex,
      coordinates: targetCoord,
      status: mission.status
    });

    res.json({ success: true, missionId, targetCoord, stepIndex });
  } catch (err) {
    res.status(500).json({ success: false, error: err.message });
  }
});

// Start Server & Daemon
const PORT = process.env.PORT || 3000;

async function startServer() {
  await connectToDatabase();
  await bootstrapDatabase();

  retrievalService = new AdaptiveRetrievalService();
  allocationWorker = new AllocationWorker();
  hazardDaemon = new HazardStreamDaemon();
  telemetryWorker = new TelemetryStreamWorker();

  // Pipe Change Stream events into WebSockets
  hazardDaemon.on("hazard_updated", data => broadcast("HAZARD_UPDATED", data));
  hazardDaemon.on("spatial_delta_computed", data => broadcast("SPATIAL_DELTA_COMPUTED", data));
  hazardDaemon.on("route_compromised", data => broadcast("ROUTE_COMPROMISED", data));
  hazardDaemon.on("mission_rerouted", data => broadcast("MISSION_REROUTED", data));

  await hazardDaemon.startDaemon();

  server.listen(PORT, () => {
    console.log(`\n================================================================================`);
    console.log(` RELIEFMESH ENTERPRISE OPERATIONAL ENGINE IS LIVE`);
    console.log(` HTTP API:       http://localhost:${PORT}`);
    console.log(` WEB CONSOLE:    http://localhost:${PORT}`);
    console.log(` WEBSOCKET FEED: ws://localhost:${PORT}`);
    console.log(` MONGODB CORE:   Replica Set rs0 on mongodb://127.0.0.1:27018`);
    console.log(`================================================================================\n`);
  });
}

startServer().catch(err => {
  console.error("[FATAL] Server launch failure:", err);
  process.exit(1);
});
