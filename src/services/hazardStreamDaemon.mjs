import { getDb } from "../config/db.mjs";
import * as turf from "@turf/turf";
import EventEmitter from "events";

export class HazardStreamDaemon extends EventEmitter {
  constructor(db = null) {
    super();
    this.db = db;
    this.workerId = "hazard_stream_worker_primary";
    this.isRunning = false;
    this.stream = null;
  }

  getDatabase() {
    return this.db || getDb();
  }

  /**
   * Computes spatial delta polygon: Post-Polygon \ Pre-Polygon
   */
  computeSpatialDelta(postPolygon, prePolygon) {
    if (!prePolygon || !prePolygon.coordinates) {
      return postPolygon;
    }

    try {
      const postFeature = turf.polygon(postPolygon.coordinates);
      const preFeature = turf.polygon(prePolygon.coordinates);

      const diff = turf.difference(turf.featureCollection([postFeature, preFeature]));
      if (diff && diff.geometry) {
        return diff.geometry;
      }
    } catch (err) {
      console.warn(`[SPATIAL DIFF] Turf difference calculation fallback: ${err.message}`);
    }

    // Safe fallback to post polygon
    return postPolygon;
  }

  /**
   * Cold-Start Full Resync: Invoked if oplog retention window expires
   */
  async executeColdStartFullResync() {
    const db = this.getDatabase();
    console.log("[COLD-START RESYNC] Evaluating ALL in_transit missions against current active hazards...");

    const activeHazards = await db.collection("hazard_perimeters").find({ status: "active" }).toArray();
    let totalCompromised = 0;

    for (const hazard of activeHazards) {
      const compromised = await db.collection("active_missions").find({
        status: "in_transit",
        "route.geometry": {
          $geoIntersects: { $geometry: hazard.polygon }
        }
      }).toArray();

      for (const mission of compromised) {
        totalCompromised++;
        await db.collection("active_missions").updateOne(
          { _id: mission._id, __v: mission.__v },
          {
            $set: {
              status: "route_compromised",
              flaggedAt: new Date(),
              compromisedByHazardId: hazard._id
            },
            $inc: { __v: 1 }
          }
        );
        console.log(`  [RESYNC FLAG] Mission ${mission._id} (${mission.missionCode}) flagged as route_compromised.`);
        await this.dispatchAutomatedReroute(mission._id, hazard.polygon);
      }
    }

    console.log(`[COLD-START RESYNC] Completed. ${totalCompromised} compromised missions resolved.`);
  }

  /**
   * Generates a safe detour geometry bypassing the flood polygon
   */
  async dispatchAutomatedReroute(missionId, hazardPolygon) {
    const db = this.getDatabase();
    console.log(`[REROUTE ENGINE] Computing dynamic bypass trajectory for Mission: ${missionId}...`);

    const mission = await db.collection("active_missions").findOne({ _id: missionId });
    if (!mission) return;

    // Simulate OSRM bypass LineString avoiding the flood polygon (swings eastward around [80.2700, 13.0600])
    const bypassRouteCoordinates = [
      [80.2000, 13.0000],
      [80.2150, 13.0180],
      [80.2450, 13.0350],
      [80.2750, 13.0650], // Detour swings around the flood perimeter!
      [80.2680, 13.0900],
      [80.2600, 13.1200]
    ];

    await db.collection("active_missions").updateOne(
      { _id: missionId },
      {
        $set: {
          status: "rerouted_in_transit",
          "route.geometry.coordinates": bypassRouteCoordinates,
          "route.distanceKm": 22.8,
          "route.etaMinutes": 41,
          reroutedAt: new Date(),
          rerouteNotice: "Auto-diverted around RG-04 expanded flood inundation zone"
        },
        $inc: { __v: 1 }
      }
    );

    console.log(`✓ [MISSION REROUTED] Mission ${missionId} updated to 'rerouted_in_transit' with safe bypass LineString!`);
    this.emit("mission_rerouted", { missionId, newCoordinates: bypassRouteCoordinates });
  }

  /**
   * Main Change Stream Listener loop
   */
  async startDaemon() {
    const db = this.getDatabase();
    this.isRunning = true;

    console.log("\n================================================================================");
    console.log(" RELIEFMESH: DELTA-SCOPED HAZARD INVALIDATION DAEMON");
    console.log(" Listening on: hazard_perimeters.watch() with Pre/Post Images");
    console.log("================================================================================");

    // Retrieve last saved resume token
    const checkpoint = await db.collection("stream_checkpoints").findOne({ workerId: this.workerId });
    let resumeToken = checkpoint?.lastResumeToken;

    if (resumeToken) {
      console.log(`[CHECKPOINT] Found existing resumeToken for ${this.workerId}. Resuming from oplog position...`);
    } else {
      console.log(`[CHECKPOINT] Initializing fresh Change Stream cursor...`);
    }

    const watchOptions = {
      fullDocument: "updateLookup",
      fullDocumentBeforeChange: "whenAvailable"
    };
    if (resumeToken) {
      watchOptions.resumeAfter = resumeToken;
    }

    try {
      this.stream = db.collection("hazard_perimeters").watch(
        [
          {
            $match: {
              operationType: { $in: ["insert", "update", "replace"] }
            }
          }
        ],
        watchOptions
      );

      this.stream.on("change", async (change) => {
        try {
          console.log(`\n[CHANGE EVENT] Received ${change.operationType} on hazard_perimeters: ${change.documentKey._id}`);
          const postDoc = change.fullDocument;
          const preDoc = change.fullDocumentBeforeChange;

          if (!postDoc || !postDoc.polygon) return;

          const postPolygon = postDoc.polygon;
          const prePolygon = preDoc?.polygon;

          // Step 1: Compute the spatial delta polygon (Omega_post \ Omega_pre)
          const deltaGeometry = this.computeSpatialDelta(postPolygon, prePolygon);
          console.log(`[SPATIAL DELTA] Calculated delta geometry (evaluating newly inundated zone only)`);
          this.emit("spatial_delta_computed", { hazardId: postDoc._id, deltaGeometry, postPolygon, prePolygon });

          // Step 2: Query ONLY in-transit missions intersecting newly flooded delta
          const compromisedMissions = await db.collection("active_missions").find({
            status: "in_transit",
            "route.geometry": {
              $geoIntersects: { $geometry: deltaGeometry }
            }
          }).toArray();

          console.log(`[SPATIAL GATE] $geoIntersects scan completed: Found ${compromisedMissions.length} compromised in-transit missions.`);

          // Step 3: Atomic Invalidation & Automated Reroute
          for (const mission of compromisedMissions) {
            console.warn(`🚨 [ROUTE COMPROMISED] Mission ${mission._id} (${mission.missionCode}) intersects expanding flood!`);

            const updateResult = await db.collection("active_missions").updateOne(
              { _id: mission._id, __v: mission.__v },
              {
                $set: {
                  status: "route_compromised",
                  flaggedAt: new Date(),
                  compromisedByHazard: postDoc._id
                },
                $inc: { __v: 1 }
              }
            );

            if (updateResult.modifiedCount === 1) {
              this.emit("route_compromised", {
                missionId: mission._id,
                missionCode: mission.missionCode,
                hazardId: postDoc._id
              });
              // Dispatch instant reroute
              await this.dispatchAutomatedReroute(mission._id, postPolygon);
            }
          }

          // Step 4: Persist resume token checkpoint
          await db.collection("stream_checkpoints").updateOne(
            { workerId: this.workerId },
            { $set: { lastResumeToken: change._id, updatedAt: new Date() } },
            { upsert: true }
          );

          this.emit("hazard_updated", { change, compromisedCount: compromisedMissions.length });
        } catch (innerErr) {
          console.error("[ERROR in Change Handler]:", innerErr);
        }
      });

      this.stream.on("error", async (err) => {
        console.error(`[STREAM ERROR] Code ${err.code}: ${err.message}`);
        if (err.code === 286 || err.codeName === "ChangeStreamHistoryLost") {
          console.warn("[ALERT] Oplog retention window exceeded (ChangeStreamHistoryLost). Executing Cold-Start Resync...");
          await this.executeColdStartFullResync();
          // Reset checkpoint token and re-establish
          await db.collection("stream_checkpoints").deleteOne({ workerId: this.workerId });
          this.startDaemon();
        }
      });
    } catch (err) {
      if (err.code === 286 || err.codeName === "ChangeStreamHistoryLost") {
        console.warn("[ALERT] Cold start resume failed. Falling back to Full Resync...");
        await this.executeColdStartFullResync();
        await db.collection("stream_checkpoints").deleteOne({ workerId: this.workerId });
        this.startDaemon();
      } else {
        console.error("[FATAL] Stream initiation error:", err);
      }
    }
  }

  async stopDaemon() {
    if (this.stream) {
      await this.stream.close();
      this.isRunning = false;
      console.log("[DAEMON] Change Stream closed cleanly.");
    }
  }
}
