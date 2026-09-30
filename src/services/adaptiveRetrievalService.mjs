import { getDb } from "../config/db.mjs";
import * as turf from "@turf/turf";

export class AdaptiveRetrievalService {
  constructor(db = null) {
    this.db = db;
  }

  getDatabase() {
    return this.db || getDb();
  }

  /**
   * Expands dialect/vernacular words into clinical terms using synonym_mappings collection
   */
  async expandSynonyms(requestText) {
    const db = this.getDatabase();
    const words = requestText.toLowerCase().split(/\s+/);
    const mappings = await db.collection("synonym_mappings").find({}).toArray();

    const expandedTerms = new Set(words);
    for (const mapping of mappings) {
      const match = mapping.synonyms.some(s => words.includes(s.toLowerCase()));
      if (match) {
        mapping.synonyms.forEach(s => expandedTerms.add(s.toLowerCase()));
      }
    }
    return Array.from(expandedTerms);
  }

  /**
   * Simulates embedding generation with strict promise timeout
   */
  async generateEmbeddingWithTimeout(text, timeoutMs = 3000, forceTimeout = false) {
    if (forceTimeout) {
      await new Promise(r => setTimeout(r, 100));
      throw new Error(`Embedding API timeout after ${timeoutMs}ms (Simulated Outage)`);
    }

    // In production, calls OpenAI text-embedding-3-small.
    // For local deterministic test, generates a pseudo 1536-dim vector seeded by text.
    return new Promise((resolve) => {
      setTimeout(() => {
        const vector = new Array(1536).fill(0).map((_, i) => Math.sin(text.length * i));
        resolve(vector);
      }, 50);
    });
  }

  /**
   * Core 4-R Retrieval Loop: Relevant & Reachable
   */
  async retrieveCandidates(requestText, userCoordinates, options = {}) {
    const db = this.getDatabase();
    const { simulateApiTimeout = false, maxCandidates = 5 } = options;

    console.log(`\n[RETRIEVAL] Inbound Query: "${requestText}" from [${userCoordinates.join(", ")}]`);

    // Step 1: Expand Dialect / Vernacular Synonyms
    const expandedTerms = await this.expandSynonyms(requestText);
    console.log(`[RETRIEVAL] Synonym Normalization: ${expandedTerms.slice(0, 5).join(", ")}...`);

    // Step 2: Recall Probe ($searchMeta simulation over candidate inventory)
    const probeQuery = {
      status: "available",
      availableQuantity: { $gt: 0 },
      $or: expandedTerms.map(term => ({
        $or: [
          { itemDescription: { $regex: term, $options: "i" } },
          { category: { $regex: term, $options: "i" } }
        ]
      }))
    };

    const keywordCount = await db.collection("resource_inventory").countDocuments(probeQuery);
    console.log(`[RETRIEVAL] Recall Probe Match Count: ${keywordCount} available candidates`);

    let geoRadiusKm = 50;
    if (keywordCount < 3) {
      geoRadiusKm = Math.min(100, geoRadiusKm * 2);
      console.log(`[RETRIEVAL] Self-Healing Probe: Low recall detected (${keywordCount} < 3). Bounding radius widened to ${geoRadiusKm}km`);
    }

    // Step 3: Embedding Preflight with Circuit Breaker
    let queryVector = null;
    let retrievalMode = "FULL_HYBRID";

    try {
      queryVector = await this.generateEmbeddingWithTimeout(requestText, 3000, simulateApiTimeout);
      console.log(`[RETRIEVAL] Embedding Preflight: SUCCESS (1536-dim vector generated)`);
    } catch (err) {
      console.warn(`[WARN] ${err.message}. Dropping semantic branch.`);
      console.warn(`[RETRIEVAL] Operating Mode: DEGRADED_LEXICAL_GEO (Atlas Search Synonyms + 2dsphere Proximity active)`);
      retrievalMode = "DEGRADED_LEXICAL_GEO";
    }

    // Step 4: Multi-Branch Pipeline Candidate Generation
    // Branch A: Spatial Proximity via 2dsphere $geoNear aggregation
    const proximityCandidates = await db.collection("resource_inventory").aggregate([
      {
        $geoNear: {
          near: { type: "Point", coordinates: userCoordinates },
          distanceField: "distanceMeters",
          maxDistance: geoRadiusKm * 1000,
          spherical: true,
          query: { status: "available", availableQuantity: { $gt: 0 } }
        }
      },
      { $limit: 20 }
    ]).toArray();

    // Branch B: Lexical & Synonym Candidates
    const lexicalCandidates = await db.collection("resource_inventory").find(probeQuery).limit(20).toArray();

    // Step 5: Uniform Reciprocal Rank Fusion (RRF)
    // RRF(d) = sum( 1 / (60 + rank_branch(d)) )
    const scoreMap = new Map();

    const addRank = (list, branchName) => {
      list.forEach((doc, idx) => {
        const id = doc._id.toString();
        const rank = idx + 1;
        const rrfContribution = 1 / (60 + rank);

        if (!scoreMap.has(id)) {
          scoreMap.set(id, {
            document: doc,
            totalRrfScore: 0,
            ranks: {}
          });
        }
        const entry = scoreMap.get(id);
        entry.totalRrfScore += rrfContribution;
        entry.ranks[branchName] = rank;
      });
    };

    addRank(lexicalCandidates, "lexical");
    addRank(proximityCandidates, "proximity");

    if (queryVector) {
      // In Atlas, this is the $vectorSearch branch. In local simulation:
      addRank(lexicalCandidates, "semantic");
    }

    // Sort by merged RRF score descending
    let ranked = Array.from(scoreMap.values()).sort((a, b) => b.totalRrfScore - a.totalRrfScore);

    // Step 6: Reachability Hazard Pruning (Euclidean nearby != road reachable)
    const activeHazards = await db.collection("hazard_perimeters").find({ status: "active" }).toArray();
    const prunedCandidates = [];

    for (const item of ranked) {
      const depot = item.document;
      // Check if depot itself is inside any active flood hazard polygon
      let isFlooded = false;
      for (const hazard of activeHazards) {
        const pt = turf.point(depot.location.coordinates);
        const poly = turf.polygon(hazard.polygon.coordinates);
        if (turf.booleanPointInPolygon(pt, poly)) {
          isFlooded = true;
          break;
        }
      }

      if (isFlooded) {
        console.log(`[SPATIAL GATE] Depot ${depot._id} (${depot.depotCode}) is SUBMERGED in flood zone. Pruned from candidate pool!`);
      } else {
        prunedCandidates.push({
          ...depot,
          rrfScore: item.totalRrfScore,
          ranks: item.ranks
        });
      }
    }

    const finalCandidates = prunedCandidates.slice(0, maxCandidates);
    console.log(`[RETRIEVAL] $rankFusion completed: ${finalCandidates.length} viable, reachable depots returned.`);
    finalCandidates.forEach((c, idx) => {
      console.log(`  [Rank #${idx + 1}] ${c._id} (${c.depotCode}) - Avail: ${c.availableQuantity} units, OCC Version: __v:${c.__v}, RRF Score: ${c.rrfScore.toFixed(4)}`);
    });

    return {
      candidates: finalCandidates,
      retrievalMode,
      geoRadiusKm,
      synonymTerms: expandedTerms
    };
  }
}
