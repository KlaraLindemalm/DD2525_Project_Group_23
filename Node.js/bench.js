const { spawn } = require("child_process");
const fs = require("fs");

const patterns = [
  ["(a+)+$", "a"],
  ["(a|aa)+$", "a"],
  ["(.*a){5}", "a"],
  ["(a|b|ab)*$", "ab"],
];

const MAX_SIZE = 200;
const STEP = 5;
const TIMEOUT = 10_000; // milliseconds

function runRegexWithTimeout(pattern, input) {
  return new Promise((resolve) => {
    const child = spawn("node", ["regex_worker.js", pattern, input]);

    const startTime = Date.now();
    const timeout = setTimeout(() => {
      child.kill(); // Kill runaway regex
      resolve("TIMEOUT");
    }, TIMEOUT);

    child.on("exit", (code) => {
      clearTimeout(timeout);
      const elapsed = (Date.now() - startTime) / 1000;
      if (code === 0) {
        resolve(`${elapsed.toFixed(4)}s`);
      } else {
        resolve("ERROR");
      }
    });
  });
}

async function testPattern(pattern, baseInput) {
  console.log(`\nTesting pattern: ${pattern}`);
  for (let size = 5; size <= MAX_SIZE; size += STEP) {
    const testStr = baseInput.repeat(size) + "X"; // Ensure it doesn't match
    const result = await runRegexWithTimeout(pattern, testStr);
    console.log(`  Input size: ${testStr.length} | Time: ${result}`);
    fs.appendFileSync("js_results.csv", `NodeJS | ${pattern} | ${testStr.length} | ${result}\n`);
    if (result === "TIMEOUT" || result === "ERROR") break;
  }
}

(async () => {
  for (const [pattern, baseInput] of patterns) {
    await testPattern(pattern, baseInput);
  }
})();
