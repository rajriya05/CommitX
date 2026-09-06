import pandas as pd
import matplotlib.pyplot as plt

# Read cleaned FIRMS data
file = "data/cleaned/FIRMS/jamshedpur_firms_clean.csv"

df = pd.read_csv(file)

print("FIRMS records:", len(df))

# Create map
plt.figure(figsize=(10, 8))

plt.scatter(
    df["longitude"],
    df["latitude"],
    s=8,
    alpha=0.6
)

plt.xlabel("Longitude")
plt.ylabel("Latitude")
plt.title("NASA FIRMS Thermal Anomalies - Jamshedpur")

plt.grid(True)

# Save map
output = "data/cleaned/FIRMS/jamshedpur_firms_map.png"

plt.savefig(output, dpi=300, bbox_inches="tight")

plt.show()

print("\nMap saved successfully!")
print("Output:", output)