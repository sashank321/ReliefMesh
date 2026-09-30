import { getDb } from "../config/db.mjs";

export class TelemetryStreamWorker {
  constructor(db = null) {
    this.db = db;
  }

  getDatabase() {
    return this.db || getDb();
  }

  /**
   * Ingests a new river gauge telemetry ping and simulates Atlas Stream Processing (ASP) windowed derivative
   */
  async ingestTelemetryReading(sensorId, waterLevelMeters) {
    const db = this.getDatabase();
    const now = new Date();

    // 1. Record telemetry reading
    await db.collection("sensor_telemetry").insertOne({
      sensorId,
      waterLevelMeters,
      timestamp: now
    });

    // 2. Fetch previous reading within 2-minute sliding window to compute derivative ($derivative simulation)
    const previous = await db.collection("sensor_telemetry")
      .find({ sensorId, timestamp: { $lt: now } })
      .sort({ timestamp: -1 })
      .limit(1)
      .toArray();

    let rateOfRiseCmMin = 0;
    if (previous.length > 0) {
      const prevDoc = previous[0];
      const deltaMinutes = (now.getTime() - prevDoc.timestamp.getTime()) / 60000;
      if (deltaMinutes > 0) {
        const deltaMeters = waterLevelMeters - prevDoc.waterLevelMeters;
        rateOfRiseCmMin = (deltaMeters * 100) / deltaMinutes;
      }
    }

    console.log(`[TELEMETRY ASP] Gauge: ${sensorId} | Level: ${waterLevelMeters}m | Rate-of-Rise: ${rateOfRiseCmMin.toFixed(1)} cm/min`);

    // 3. Threshold Check: If rate-of-rise >= 35 cm/min or level >= 4.5m -> BREACH DETECTED!
    const BREACH_THRESHOLD_CM_MIN = 35.0;
    const CRITICAL_LEVEL_METERS = 4.2;

    if (rateOfRiseCmMin >= BREACH_THRESHOLD_CM_MIN || waterLevelMeters >= CRITICAL_LEVEL_METERS) {
      console.warn(`🚨 [ASP ALERT] Upstream Embankment Breach Detected at Gauge ${sensorId}! Triggering Hydraulic Flood Model Sidecar...`);
      return await this.triggerHydraulicFloodExpansion(sensorId, waterLevelMeters, rateOfRiseCmMin);
    }

    return { breachTriggered: false, rateOfRiseCmMin };
  }

  /**
   * Simulates the external Hydraulic Model (HEC-RAS / Hydro-ML Sidecar)
   * Writes the expanded inundation polygon to MongoDB hazard_perimeters!
   */
  async triggerHydraulicFloodExpansion(sensorId, waterLevelMeters, rateOfRiseCmMin) {
    const db = this.getDatabase();

    // The EXPANDED flood polygon that covers Highway 16 near [80.2350, 13.0600]
    const expandedFloodPolygon = {
      type: "Polygon",
      coordinates: [[
        [80.2200, 13.0350],
        [80.2500, 13.0350],
        [80.2500, 13.0750], // Stretches north across Highway 16 corridor!
        [80.2200, 13.0750],
        [80.2200, 13.0350]
      ]]
    };

    const hazardId = "HAZARD-RIVER-BASIN-01";

    // Update hazard_perimeters (Triggers native Change Stream with Pre- and Post-Images!)
    const updateResult = await db.collection("hazard_perimeters").updateOne(
      { _id: hazardId },
      {
        $set: {
          polygon: expandedFloodPolygon,
          severity: "catastrophic",
          waterLevelMeters,
          rateOfRiseCmMin,
          breachAlert: true,
          updatedAt: new Date()
        },
        $inc: { __v: 1 }
      }
    );

    console.log(`✓ [HYDRAULIC SIDECAR] Updated hazard_perimeters (${hazardId}) with expanded inundation polygon (Modified: ${updateResult.modifiedCount})`);

    return {
      breachTriggered: true,
      hazardId,
      waterLevelMeters,
      rateOfRiseCmMin,
      expandedPolygon: expandedFloodPolygon
    };
  }
}
