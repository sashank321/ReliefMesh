# ReliefMesh: Operational Crisis Coordination Engine

> **Track 1:** Disaster Relief Coordination Platform · **Target Platform:** MongoDB Atlas (MongoDB 8.1+ Core Engine, 8.2+ GA)  
> **Engineering Invariant:** *The Freshness Invariant — No operational allocation may outlive its physical ground truth.*

$$\mathbf{The\ Freshness\ Invariant:}\quad \forall a \in \mathcal{A}_{\text{active}},\; \Delta t(a) \le t_{\text{oplog\_propagation}} + t_{\text{spatial\_eval}} + t_{\text{worker\_commit}}$$

---

## 🌪️ The Problem: Operational State Drift

Disaster coordination platforms do not collapse due to lack of inbound data. They collapse due to **Operational State Drift**:
* **The Phantom Resource:** Two ambulances race toward a single depot with 5 blood bags left. Both dispatchers see "available." Both drive. One gets the blood; the other arrives to an empty shelf and a dead patient.
* **Stale Routing:** Supply convoys are dispatched on routes that were safe an hour ago, but are now submerged by upstream dam breaches.
* **The Distributed Sprawl Collapse:** Traditional systems attempt to duct-tape 5 distributed engines (*PostgreSQL + PostGIS + pgvector + Debezium + Kafka*). When cyclones knock out power and cell backhauls drop 80% of packets, distributed quorum fails.

ReliefMesh replaces this brittle stack with **one single MongoDB Atlas Operational Core**.

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
- Node.js v20+ (Tested on Node v25.6)
- MongoDB 8.x Replica Set (`rs0` active on port 27018)

### Running the Live System

```bash
# 1. Install dependencies
npm install

# 2. Bootstrap database schemas, 2dsphere indexes, and pre/post-images
npm run bootstrap

# 3. Seed authoritative test scenario ground truth
npm run seed

# 4. Run the complete automated demo evaluation suite (Demo A & Demo B)
npm run demo:all

# 5. Start the Live Operational Server & Dispatcher Web Console
npm start
# Opens interactive Mission Control Console on http://localhost:3000
```

---

## 🔬 Core Database Primitives Implemented

### 1. Stage 1 & 2: Relevant & Reachable (`src/services/adaptiveRetrievalService.mjs`)
* **Vernacular Synonym Normalization:** Maps dialect terms (*"khoon"* → blood, *"dawa"* → medicine, *"paani"* → flood) natively using the `synonym_mappings` collection without cloud LLM latency.
* **Recall Probe (`$searchMeta`):** Metadata-only query over Lucene postings. Automatically widens search radius from 50km to 100km if matches `< 3`.
* **Adaptive Circuit Breaker:** Wraps vector embedding APIs in a strict 3,000ms timeout. Gracefully degrades from `FULL_HYBRID` to `DEGRADED_LEXICAL_GEO` mode during field network outages.
* **Uniform Reciprocal Rank Fusion (`$rankFusion` / RRF):** Fuses lexical BM25 and geospatial proximity into a single authoritative candidate ranking:
  $$RRF(d) = \sum_{b \in \text{branches}} \frac{1}{60 + r_b(d)}$$

### 2. Stage 3: Reserved (`src/services/allocationWorker.mjs`)
* **Single-Document Optimistic Concurrency Control (OCC):**
  ```javascript
  db.resource_inventory.updateOne(
    { _id: targetDepotId, __v: version, availableQuantity: { $gte: requestedQty }, status: "available" },
    {
      $inc: { availableQuantity: -requestedQty, __v: 1 },
      $push: { allocations: { $each: [{ incidentId, qty: requestedQty, at: new Date() }], $slice: -10 } }
    }
  );
  ```
* **Bounded Allocation History:** Enforces `$slice: -10` on the embedded allocation history array to prevent document bloat and memory fragmentation under high contention.
* **Cheap Failed Predicate:** Contention surfaces as `modifiedCount: 0` in `<5ms` without expensive multi-row lock waits or distributed locks.
* **Thundering Herd Defense:** Applies **Exponential Backoff with Full Jitter** and selects randomly across a **Randomized Candidate Window** (top-3 candidates) so competing dispatchers don't crash into the same fallback depot.

### 3. Stage 4: Resilient (`src/services/hazardStreamDaemon.mjs` - The Hero Feature)
* **Change Streams with Pre- and Post-Images:**
  ```javascript
  db.command({ collMod: "hazard_perimeters", changeStreamPreAndPostImages: { enabled: true } });
  ```
* **Geometric Spatial Delta ($\Delta \Omega$):**
  $$\Delta \Omega = \Omega_{\text{post}} \setminus \Omega_{\text{pre}}$$
  Evaluates **only** the newly flooded expansion difference rather than scanning the entire historical map.
* **Delta-Scoped Invalidation:** Executes `$geoIntersects` exclusively on the spatial delta geometry against active `in_transit` missions.
* **Automated Detour Rerouting:** Automatically flags compromised missions (`route_compromised`) and generates safe bypass trajectories (`rerouted_in_transit`).
* **Cold-Start Resync Protocol:** Detects `ChangeStreamHistoryLost` (code 286), falls back to a full active scan, and re-establishes the Change Stream cursor.

---

## 📊 Honest Architecture Audit: PostgreSQL vs. MongoDB Atlas

| Dimension | PostgreSQL (+PostGIS/pgvector) + Debezium + Kafka | MongoDB Atlas (8.1+) | Production Verdict |
|---|---|---|---|
| **Road Network Routing** | **WINNER**: Native `pgRouting` computes shortest paths (Dijkstra/A*). | Externalized to OSRM sidecar. `$graphLookup` is inadequate for weighted road networks. | **Concession**: MongoDB does not do road routing; OSRM owns road topologies, MongoDB owns spatial hazard barriers. |
| **Relational Integrity** | **WINNER**: Declarative foreign keys across heavily normalized schemas. | Document model + schema validation via `$and: [ { $jsonSchema }, { $expr } ]`. | PostgreSQL excels at fragmented relational graphs; MongoDB excels at cohesive operational aggregates. |
| **Single-Row CAS Contention** | **PARITY**: Under default READ COMMITTED, concurrent UPDATEs re-evaluate the WHERE clause → returns 0 rows. | **PARITY**: Single-document CAS (`$inc: { __v: 1 }`) returns `modifiedCount: 0`. | **Honest Audit**: Both engines handle single-row CAS with cheap failed predicates. MongoDB's edge is the reactive loop, not the CAS. |
| **Reactive CDC Infrastructure** | Requires external Debezium workers + Kafka cluster + replication slots. | **WINNER**: Native Resumable Change Streams backed by the oplog with pre/post-images. | **Core Differentiator**: MongoDB eliminates Kafka and Debezium for this bounded loop. |
| **Operational Control Plane** | 3 independent distributed systems to deploy, monitor, and sync. | **WINNER**: 1 managed data control plane (Vector + Geo + Transactions + Streams). | Restarting ONE process after a hurricane power cut saves lives. |

---

## 🖥️ Interactive Web Console (`http://localhost:3000`)

* **Interactive Leaflet Slippy Map:** Visualizes Sector 7 depots, pulsing convoy markers along Highway 16, and expanding flood hazard polygons in real time.
* **4-R Operational Spine Inspector:**
  * **Gate 1:** Dialect Search box testing vernacular queries (*"need khoon o-neg"*) with AI outage simulation.
  * **Gate 2:** Spatial Gating and hazard exclusion.
  * **Gate 3:** Concurrency Stress tester (2 to 5 dispatchers) displaying CAS commit and Full Jitter distribution.
  * **Gate 4:** River Gauge surge simulator (4.8m) triggering delta invalidation and detour polyline rendering.
* **Live MongoDB Oplog Change Stream Feed:** Streams real-time oplog push notifications directly from the MongoDB Replica Set.

---

## 📁 Repository Structure

```
.
├── docs/
│   ├── SPECIFICATION.md                         # Definitive 82KB Architecture Blueprint
│   ├── ReliefMesh_MongoDB_Hackathon_Deck.pptx   # Master Hackathon Submission Presentation
│   ├── ReliefMesh_MongoDB_Executive_Deck.pptx   # Executive Summary Deck
│   └── presentation.html                        # Standalone HTML Slides Viewer
├── src/
│   ├── config/
│   │   └── db.mjs                               # MongoDB 8.3 Replica Set Connection Pool
│   ├── database/
│   │   ├── bootstrapDatabase.mjs                # Collections, 2dsphere Indexes, Pre/Post-Images
│   │   └── seedData.mjs                         # Crisis Scenario Ground Truth & Vernacular Synonyms
│   ├── services/
│   │   ├── adaptiveRetrievalService.mjs         # Stage 1 & 2: Hybrid RRF & Spatial Hazard Gating
│   │   ├── allocationWorker.mjs                 # Stage 3: Atomic OCC CAS & Jittered Rematch
│   │   ├── hazardStreamDaemon.mjs               # Stage 4: Delta Change Stream & Detour Rerouting
│   │   └── telemetryStreamWorker.mjs            # ASP Windowed Rate-of-Rise ($derivative) Simulator
│   ├── demos/
│   │   ├── demoRaceReplay.mjs                   # Standalone Demo A: Race Replay Runner
│   │   ├── demoDeltaInvalidation.mjs            # Standalone Demo B: Delta Invalidation Runner
│   │   └── runAllDemos.mjs                      # Master Evaluation Test Suite
│   └── server.js                                # Express REST API + WebSocket Broadcaster
├── public/
│   └── index.html                               # Dispatcher Incident Console (Leaflet + WebSocket)
├── final_s1.png ... final_s6.png                # High-Resolution 6-Slide Master Presentations
├── package.json                                 # ESM Configuration & npm Scripts
└── SPECIFICATION.md                             # Architectural Blueprint
```
