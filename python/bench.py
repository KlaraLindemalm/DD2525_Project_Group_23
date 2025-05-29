import re
import time
import multiprocessing


evil_patterns = [
    ("(a+)+$", "a"),                 # classic nested quantifier
    ("(a|aa)+$", "a"),               # overlapping alternation
    ("(.*a){5}", "a"),               # greedy + quantified group
    ("(a|b|ab)*$", "ab"),            # ambiguous branching
]

MAX_SIZE = 100           # Maximum number of pattern repetitions
STEP = 5                # Increment size
TIMEOUT = 5             # Seconds

# Timeout-safe matching function
def run_regex(pattern, test_str, result_queue):
    try:
        re.compile(pattern).fullmatch(test_str)
        result_queue.put(time.time())
    except Exception as e:
        result_queue.put(e)

def time_regex(pattern, test_str, timeout=TIMEOUT):
    start_time = time.time()
    q = multiprocessing.Queue()
    p = multiprocessing.Process(target=run_regex, args=(pattern, test_str, q))
    p.start()
    p.join(timeout)
    if p.is_alive():
        p.terminate()
        return "TIMEOUT"
    end = q.get()
    if isinstance(end, Exception):
        return str(end)
    return round(end - start_time, 4)

# Benchmark loop
if __name__ == "__main__":
    for pattern, increasing_input in evil_patterns:
        print(f"\nTesting pattern: {pattern}")
        for size in range(5, MAX_SIZE + 1, STEP):
            test_input = increasing_input * size + "X"  # X Break the match at the end
            duration = time_regex(pattern, test_input)
            print(f"  Input size: {len(test_input):3d} | Time: {duration}")
            if duration == "TIMEOUT":
                break  # Stop if it's catastrophic and takes longer then TIMEOUT
