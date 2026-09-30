import { connectToDatabase, closeDatabase } from "../config/db.mjs";

export function generate768DimVector(seedText) {
  let hash = 0;
  for (let i = 0; i < seedText.length; i++) {
    hash = ((hash << 5) - hash) + seedText.charCodeAt(i);
    hash |= 0;
  }
  const vec = new Array(768);
  let norm = 0;
  for (let i = 0; i < 768; i++) {
    const val = Math.sin((hash + 1) * (i + 1));
    vec[i] = val;
    norm += val * val;
  }
  const mag = Math.sqrt(norm) || 1;
  return vec.map(v => Number((v / mag).toFixed(6)));
}

export async function seedData() {
  const { db } = await connectToDatabase();
  console.log("================================================================================");
  console.log(" RELIEFMESH: SEEDING OPERATIONAL TEST SCENARIOS & CRISIS GROUND TRUTH");
  console.log("================================================================================");

  // 1. Synonym Mappings
  console.log("\n[SEED] Populating Vernacular Crisis Synonyms...");
  await db.collection("synonym_mappings").deleteMany({});
  await db.collection("synonym_mappings").insertMany([
    {
      mappingType: "equivalent",
      category: "blood_products",
      synonyms: [
        "khoon",
        "blood",
        "rakt",
        "lahu",
        "pediatric o-negative whole blood",
        "o-neg",
        "o neg",
        "o-negative",
        "pediatric blood"
      ]
    },
    {
      mappingType: "equivalent",
      category: "pharmaceuticals",
      synonyms: [
        "dawa",
        "medicine",
        "marham",
        "pharmaceuticals",
        "antibiotics",
        "first aid",
        "dawaai"
      ]
    },
    {
      mappingType: "equivalent",
      category: "flood_inundation",
      synonyms: [
        "paani",
        "flood",
        "baadh",
        "waterlogging",
        "inundation",
        "submerged",
        "water level"
      ]
    },
    {
      mappingType: "equivalent",
      category: "water_purification",
      synonyms: [
        "water purification",
        "purifier",
        "dewatering pumps",
        "mobile pumps",
        "saaf paani",
        "drinking water"
      ]
    },
    {
      mappingType: "equivalent",
      category: "shelter",
      synonyms: [
        "tents",
        "shelter",
        "tarpaulin",
        "plastic sheets",
        "chhat",
        "tripal"
      ]
    }
  ]);
  console.log("  ✓ Seeded 5 vernacular dialect synonym dictionaries");

  // 2. Resource Inventory (The High-Contention Crisis Depots with Native 768-dim Embeddings)
  console.log("\n[SEED] Seeding Resource Inventory Aggregates (768-dim Embeddings)...");
  await db.collection("resource_inventory").deleteMany({});
  await db.collection("resource_inventory").insertMany([
    {
      _id: "DEPOT-001",
      depotCode: "DEPOT-SEC7-TRAUMA",
      itemDescription: "Pediatric O-Negative Whole Blood (Cold-Chain Bounded)",
      category: "blood_products",
      availableQuantity: 5, // The exact 5 units contested in Demo A!
      totalCapacity: 50,
      location: {
        type: "Point",
        coordinates: [80.2707, 13.0827]
      },
      embedding: generate768DimVector("Pediatric O-Negative Whole Blood Cold Chain Trauma"),
      status: "available",
      __v: 3, // Initial OCC version tag from spec
      allocations: [
        { incidentId: "INC-PREV-HIST", qty: 5, at: new Date(Date.now() - 3600000) }
      ],
      updatedAt: new Date()
    },
    {
      _id: "DEPOT-002",
      depotCode: "DEPOT-HARBOR-RESERVE",
      itemDescription: "Pediatric O-Negative Whole Blood Units",
      category: "blood_products",
      availableQuantity: 8, // Candidate #2 for automated rematch
      totalCapacity: 40,
      location: {
        type: "Point",
        coordinates: [80.2921, 13.0955]
      },
      embedding: generate768DimVector("Pediatric O-Negative Whole Blood Harbor Reserve"),
      status: "available",
      __v: 1,
      allocations: [],
      updatedAt: new Date()
    },
    {
      _id: "DEPOT-003",
      depotCode: "DEPOT-CENTRAL-ANNEX",
      itemDescription: "O-Negative Whole Blood Reserve Pack",
      category: "blood_products",
      availableQuantity: 12, // Candidate #3 for randomized window
      totalCapacity: 100,
      location: {
        type: "Point",
        coordinates: [80.2450, 13.0510]
      },
      embedding: generate768DimVector("O-Negative Whole Blood Central Annex Pack"),
      status: "available",
      __v: 1,
      allocations: [],
      updatedAt: new Date()
    },
    {
      _id: "DEPOT-004",
      depotCode: "DEPOT-WEST-LOGISTICS",
      itemDescription: "Mobile Dewatering Water Purification Units",
      category: "water_purification",
      availableQuantity: 15,
      totalCapacity: 30,
      location: {
        type: "Point",
        coordinates: [80.2100, 13.0150]
      },
      embedding: generate768DimVector("Mobile Dewatering Water Purification Filter"),
      status: "available",
      __v: 1,
      allocations: [],
      updatedAt: new Date()
    },
    {
      _id: "DEPOT-005",
      depotCode: "DEPOT-CIVIL-DEFENSE",
      itemDescription: "Emergency High-Calorie Ready-to-Eat Rations",
      category: "shelter",
      availableQuantity: 5000,
      totalCapacity: 10000,
      location: {
        type: "Point",
        coordinates: [80.2050, 13.0300]
      },
      embedding: generate768DimVector("Emergency High Calorie Meals Food Rations"),
      status: "available",
      __v: 1,
      allocations: [],
      updatedAt: new Date()
    }
  ]);
  console.log("  ✓ Seeded 5 resource depots (including contested DEPOT-001 with 768-dim embeddings)");

  // 3. Active Missions (Convoy Alpha on Highway 16)
  console.log("\n[SEED] Seeding Active In-Transit Missions...");
  await db.collection("active_missions").deleteMany({});
  await db.collection("active_missions").insertMany([
    {
      _id: "MISSION-104",
      missionCode: "CONVOY-ALPHA-HWY16",
      title: "Supply Convoy Alpha (3 High-Clearance Trucks)",
      priority: "high",
      status: "in_transit",
      cargo: [
        { itemCode: "PURIFIER-01", qty: 4 },
        { itemCode: "RATIONS-01", qty: 2000 }
      ],
      assignedVehicle: "TRUCK-CONVOY-03",
      origin: {
        type: "Point",
        coordinates: [80.2000, 13.0000]
      },
      destination: {
        type: "Point",
        coordinates: [80.2600, 13.1200]
      },
      // Highway 16 route LineString crossing coordinate [80.2350, 13.0600]
      route: {
        geometry: {
          type: "LineString",
          coordinates: [
            [80.2000, 13.0000],
            [80.2100, 13.0200],
            [80.2220, 13.0410],
            [80.2350, 13.0600], // This segment intersects the expanded flood!
            [80.2480, 13.0850],
            [80.2600, 13.1200]
          ]
        },
        distanceKm: 18.4,
        etaMinutes: 32
      },
      __v: 0,
      dispatchedAt: new Date()
    },
    {
      _id: "MISSION-105",
      missionCode: "AMB-14-TRAUMA",
      title: "Ambulance 14 Pediatric Transport",
      priority: "critical",
      status: "in_transit",
      assignedVehicle: "AMB-14",
      origin: {
        type: "Point",
        coordinates: [80.2650, 13.0780]
      },
      destination: {
        type: "Point",
        coordinates: [80.2720, 13.0850]
      },
      route: {
        geometry: {
          type: "LineString",
          coordinates: [
            [80.2650, 13.0780],
            [80.2680, 13.0800],
            [80.2720, 13.0850]
          ]
        },
        distanceKm: 1.2,
        etaMinutes: 4
      },
      __v: 0,
      dispatchedAt: new Date()
    }
  ]);
  console.log("  ✓ Seeded active missions (CONVOY-ALPHA-HWY16 and AMB-14)");

  // 4. Hazard Perimeters (Initial River Basin Polygon - Safe Baseline)
  console.log("\n[SEED] Seeding Baseline Hazard Perimeters...");
  await db.collection("hazard_perimeters").deleteMany({});
  await db.collection("hazard_perimeters").insertMany([
    {
      _id: "HAZARD-RIVER-BASIN-01",
      hazardCode: "FLOOD-BASIN-SEC4",
      hazardType: "flood_inundation",
      source: "RIVER-GAUGE-RG04",
      status: "active",
      severity: "moderate",
      // Narrow baseline polygon that does NOT intersect Highway 16 (Convoy Alpha is currently safe)
      polygon: {
        type: "Polygon",
        coordinates: [[
          [80.2280, 13.0450],
          [80.2320, 13.0450],
          [80.2320, 13.0530],
          [80.2280, 13.0530],
          [80.2280, 13.0450]
        ]]
      },
      waterLevelMeters: 2.1,
      rateOfRiseCmMin: 2.0,
      __v: 1,
      createdAt: new Date(),
      updatedAt: new Date()
    }
  ]);
  console.log("  ✓ Seeded initial hazard perimeter HAZARD-RIVER-BASIN-01");

  // 5. Living Incident Twin
  console.log("\n[SEED] Seeding Living Incident Twin Aggregates...");
  await db.collection("living_incidents").deleteMany({});
  await db.collection("living_incidents").insertMany([
    {
      _id: "INC-2026-904",
      incidentCode: "INC-2026-904",
      title: "Sector 7 Pediatric Trauma Center Crisis",
      severity: "critical",
      status: "coordinating",
      location: {
        type: "Point",
        coordinates: [80.2680, 13.0810]
      },
      demands: [
        { itemCode: "BLOOD-O-NEG", quantityRequested: 4, quantityFulfilled: 0 }
      ],
      activeAllocations: [],
      __v: 0,
      createdAt: new Date()
    }
  ]);
  console.log("  ✓ Seeded living incident INC-2026-904");

  // 6. Sensor Telemetry Baseline
  console.log("\n[SEED] Seeding Sensor Telemetry...");
  await db.collection("sensor_telemetry").deleteMany({});
  await db.collection("sensor_telemetry").insertMany([
    {
      sensorId: "RIVER-GAUGE-RG04",
      sensorType: "water_level_ultrasonic",
      location: { type: "Point", coordinates: [80.2300, 13.0500] },
      waterLevelMeters: 2.1,
      timestamp: new Date(Date.now() - 60000)
    },
    {
      sensorId: "RIVER-GAUGE-RG04",
      sensorType: "water_level_ultrasonic",
      location: { type: "Point", coordinates: [80.2300, 13.0500] },
      waterLevelMeters: 2.15,
      timestamp: new Date()
    }
  ]);
  console.log("  ✓ Seeded sensor telemetry baseline");

  // 7. Active Edge Autonomous Responder Agents (TTL Heartbeat Consensus)
  console.log("\n[SEED] Seeding Agent Fleet Registry with TTL Heartbeats...");
  await db.collection("agent_registry").deleteMany({});
  await db.collection("agent_registry").insertMany([
    {
      agentId: "AGENT-ALPHA-DISPATCHER",
      role: "TACTICAL_DISPATCHER",
      zone: "SECTOR-7",
      status: "ACTIVE_CONSENSUS",
      lastHeartbeat: new Date(),
      lastSeenCoordinates: [80.2680, 13.0810],
      pendingAllocations: 0,
      epoch: 14
    },
    {
      agentId: "AGENT-BRAVO-MEDIC",
      role: "CRITICAL_CARE_LOGISTICS",
      zone: "HARBOR-SECTOR",
      status: "ACTIVE_CONSENSUS",
      lastHeartbeat: new Date(),
      lastSeenCoordinates: [80.2921, 13.0955],
      pendingAllocations: 0,
      epoch: 14
    },
    {
      agentId: "AGENT-CHARLIE-DRONE",
      role: "SURVEILLANCE_RECON",
      zone: "RIVER-BASIN",
      status: "ACTIVE_CONSENSUS",
      lastHeartbeat: new Date(),
      lastSeenCoordinates: [80.2300, 13.0500],
      pendingAllocations: 0,
      epoch: 14
    }
  ]);
  console.log("  ✓ Seeded 3 autonomous agents with active TTL heartbeats");

  console.log("\n================================================================================");
  console.log(" RELIEFMESH DATABASE SEEDING COMPLETED");
  console.log(" Authoritative state initialized for deterministic race and delta testing.");
  console.log("================================================================================");
}

if (process.argv[1]?.endsWith("seedData.mjs")) {
  seedData()
    .then(() => closeDatabase())
    .catch((err) => {
      console.error("[FATAL] Seeding failed:", err);
      process.exit(1);
    });
}
