import pandas as pd
import matplotlib.pyplot as plt

# Load your actual CSV file
df = pd.read_csv("data/evil4.csv")

# Convert "TIMEOUT" or blank strings to NaN
df.replace("TIMEOUT", pd.NA, inplace=True)
df = df.apply(pd.to_numeric, errors='coerce')  # ensures NaN is properly recognized

# Plotting
plt.figure(figsize=(10, 6))
for col in ["Python", "Java", "Js Experimental", "Js Original"]:
    plt.plot(df["Input"], df[col], marker='o', label=col)  # lines will stop at NaNs

#plt.title("Regex Performance for (a+)+$ Pattern")
#plt.title("Regex Performance for (a|aa)+$ Pattern")
#plt.title("Regex Performance for (.*a){5} Pattern")
plt.title("Regex Performance for (a|b|ab)*$ Pattern")
plt.xlabel("Input Size")
plt.ylabel("Runtime (seconds)")
plt.grid(True)
plt.legend()
plt.tight_layout()
plt.savefig("regex_benchmark_from_csv.png", dpi=300)
plt.show()
