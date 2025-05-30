// regex_worker.js
const [,, pattern, input] = process.argv;

try {
  const re = new RegExp(`^${pattern}`);
  re.test(input);  // May hang if pattern is catastrophic
  process.exit(0); // Successful execution (match or no match)
} catch (err) {
  process.exit(1); // If something goes wrong (bad pattern)
}
