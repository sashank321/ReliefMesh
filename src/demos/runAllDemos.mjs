import { runDemoRaceReplay } from "./demoRaceReplay.mjs";
import { runDemoDeltaInvalidation } from "./demoDeltaInvalidation.mjs";
import { closeDatabase } from "../config/db.mjs";

async function main() {
  console.log("\n################################################################################");
  console.log(" RELIEFMESH: MASTER EVALUATION & LIVE VERIFICATION SUITE");
  console.log(" Target: MongoDB 8.3 Replica Set Engine");
  console.log(" Invariant: No operational allocation may outlive its physical ground truth.");
  console.log("################################################################################\n");

  const t0 = Date.now();

  console.log(">>> EXECUTING TEST SUITE 1: DETERMINISTIC RACE REPLAY <<<");
  await runDemoRaceReplay();

  console.log("\n>>> EXECUTING TEST SUITE 2: DELTA-SCOPED ENVIRONMENTAL INVALIDATION <<<");
  await runDemoDeltaInvalidation();

  const totalTime = ((Date.now() - t0) / 1000).toFixed(2);
  console.log("################################################################################");
  console.log(` ALL RELIEFMESH DEMOS EXECUTED SUCCESSFULLY IN ${totalTime}s!`);
  console.log(" ALL DATABASE INVARIANTS RIGOROUSLY VERIFIED.");
  console.log("################################################################################\n");

  await closeDatabase();
}

main().catch(err => {
  console.error("[FATAL] Evaluation suite crashed:", err);
  process.exit(1);
});
