import { getDb } from "../config/db.mjs";
import EventEmitter from "events";

export class AgentHeartbeatWorker extends EventEmitter {
  constructor(db = null) {
    super();
    this.db = db;
    this.intervalId = null;
    this.simulatedDeadAgents = new Set();
  }

  getDatabase() {
    return this.db || getDb();
  }

  /**
   * Starts periodic heartbeat pulse for all registered edge agents
   */
  startHeartbeats(intervalMs = 5000) {
    if (this.intervalId) return;

    this.intervalId = setInterval(async () => {
      try {
        await this.pulseHeartbeats();
        const consensus = await this.evaluateFleetConsensus();
        this.emit("consensus_updated", consensus);
      } catch (err) {
        console.error("[HEARTBEAT WORKER ERROR]:", err.message);
      }
    }, intervalMs);

    console.log(`[CONSENSUS ENGINE] Agent Heartbeat Worker started (Pulse interval: ${intervalMs}ms)`);
  }

  stopHeartbeats() {
    if (this.intervalId) {
      clearInterval(this.intervalId);
      this.intervalId = null;
    }
  }

  /**
   * Pulses heartbeats for active agents (unless marked dead by chaos test)
   */
  async pulseHeartbeats() {
    const db = this.getDatabase();
    const agents = [
      { agentId: "AGENT-ALPHA-DISPATCHER", role: "TACTICAL_DISPATCHER", coords: [80.2680, 13.0810] },
      { agentId: "AGENT-BRAVO-MEDIC", role: "CRITICAL_CARE_LOGISTICS", coords: [80.2921, 13.0955] },
      { agentId: "AGENT-CHARLIE-DRONE", role: "SURVEILLANCE_RECON", coords: [80.2300, 13.0500] }
    ];

    for (const a of agents) {
      if (this.simulatedDeadAgents.has(a.agentId)) {
        // Suppress heartbeat so MongoDB TTL index will expire it
        continue;
      }

      await db.collection("agent_registry").updateOne(
        { agentId: a.agentId },
        {
          $set: {
            agentId: a.agentId,
            role: a.role,
            lastHeartbeat: new Date(),
            lastSeenCoordinates: a.coords,
            status: "ACTIVE_CONSENSUS"
          },
          $setOnInsert: { epoch: 1 }
        },
        { upsert: true }
      );
    }
  }

  /**
   * Evaluates fleet health and consensus state
   */
  async evaluateFleetConsensus() {
    const db = this.getDatabase();
    const now = Date.now();
    const activeAgents = await db.collection("agent_registry").find({}).toArray();

    let healthyCount = 0;
    let staleCount = 0;

    const fleetStatus = activeAgents.map(agent => {
      const ageMs = now - new Date(agent.lastHeartbeat).getTime();
      const isAlive = ageMs < 12000;
      if (isAlive) healthyCount++;
      else staleCount++;

      return {
        agentId: agent.agentId,
        role: agent.role,
        ageMs,
        isAlive,
        lastHeartbeat: agent.lastHeartbeat
      };
    });

    let consensusStatus = "QUORUM_HEALTHY";
    if (activeAgents.length === 0) consensusStatus = "TOTAL_PARTITION";
    else if (healthyCount < 2) consensusStatus = "QUORUM_DEGRADED";

    return {
      consensusStatus,
      totalRegistered: activeAgents.length,
      healthyCount,
      staleCount,
      fleetStatus,
      evaluatedAt: new Date()
    };
  }

  /**
   * Chaos trigger: Simulate agent node death / partition
   */
  simulateAgentPartition(agentId) {
    this.simulatedDeadAgents.add(agentId);
    console.warn(`[CHAOS SIMULATOR] Agent ${agentId} heartbeats suppressed. Awaiting MongoDB TTL expiration.`);
  }

  /**
   * Recover agent node
   */
  recoverAgent(agentId) {
    this.simulatedDeadAgents.delete(agentId);
    console.log(`[CHAOS SIMULATOR] Agent ${agentId} network connection restored. Heartbeats resumed.`);
  }
}
