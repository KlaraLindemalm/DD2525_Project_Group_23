
import java.util.concurrent.*;
import java.util.regex.Pattern;
import java.util.regex.Matcher;
import java.io.FileWriter;
import java.io.IOException;

public class Bench {

    static class PatternTest {
        String pattern;
        String baseInput;

        PatternTest(String pattern, String baseInput) {
            this.pattern = pattern;
            this.baseInput = baseInput;
        }
    }

    static final int MAX_SIZE = 200;
    static final int STEP = 5;
    static final int TIMEOUT = 10; // seconds

    static PatternTest[] evilPatterns = new PatternTest[] {
        new PatternTest("(a+)+$", "a"),
        new PatternTest("(a|aa)+$", "a"),
        new PatternTest("(.*a){5}", "a"),
        new PatternTest("(a|b|ab)*$", "ab"),
    };

    public static void main(String[] args) {
        for (PatternTest test : evilPatterns) {
            System.out.println("\nTesting pattern: " + test.pattern);
            for (int size = 5; size <= MAX_SIZE; size += STEP) {
                StringBuilder sb = new StringBuilder();
                sb.append(test.baseInput.repeat(size)).append("X");
                String testInput = sb.toString();

                String result = timeRegex(test.pattern, testInput);
                System.out.printf("  Input size: %3d | Time: %s%n", testInput.length(), result);

                // Write to CSV
                try (FileWriter writer = new FileWriter("java_results.csv", true)) {
                    writer.write(String.format("Java | %s | %d | %s\n", test.pattern, testInput.length(), result));
                } catch (IOException e) {
                    e.printStackTrace();
                }

                if ("TIMEOUT".equals(result)) break;
            }
        }
    }

    static String timeRegex(String pattern, String input) {
        ExecutorService executor = Executors.newSingleThreadExecutor();
        Callable<Long> task = () -> {
            long start = System.nanoTime();
            Pattern p = Pattern.compile(pattern);
            Matcher m = p.matcher(input);
            m.matches();  // full match
            return System.nanoTime() - start;
        };

        Future<Long> future = executor.submit(task);
        try {
            long durationNs = future.get(TIMEOUT, TimeUnit.SECONDS);
            return String.format("%.4f", durationNs / 1e9);  // seconds
        } catch (TimeoutException e) {
            future.cancel(true);
            return "TIMEOUT";
        } catch (Exception e) {
            return e.toString();
        } finally {
            executor.shutdownNow();
        }
    }
}
