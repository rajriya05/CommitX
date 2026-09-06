import pandas as pd
from pathlib import Path

# Input file
input_file = Path("data/cleaned/FIRMS/jamshedpur_firms.csv")

# Output folder
output_folder = Path("data/cleaned/FIRMS")
output_folder.mkdir(parents=True, exist_ok=True)

# Output file
output_file = output_folder / "jamshedpur_firms_clean.csv"

print("Reading Jamshedpur FIRMS data...")

df = pd.read_csv(input_file)

print(f"Original records: {len(df)}")


# ---------------------------------------------------------
# 1. Remove missing coordinates
# ---------------------------------------------------------

df = df.dropna(subset=["latitude", "longitude"])


# ---------------------------------------------------------
# 2. Remove invalid coordinates
# ---------------------------------------------------------

df = df[
    (df["latitude"] >= 22.70) &
    (df["latitude"] <= 22.90) &
    (df["longitude"] >= 86.10) &
    (df["longitude"] <= 86.35)
]


# ---------------------------------------------------------
# 3. Remove duplicate records
# ---------------------------------------------------------

df = df.drop_duplicates()


# ---------------------------------------------------------
# 4. Convert date
# ---------------------------------------------------------

df["acq_date"] = pd.to_datetime(
    df["acq_date"],
    errors="coerce"
)


# ---------------------------------------------------------
# 5. Remove records with invalid dates
# ---------------------------------------------------------

df = df.dropna(subset=["acq_date"])


# ---------------------------------------------------------
# 6. Save cleaned data
# ---------------------------------------------------------

df.to_csv(output_file, index=False)

print("\n======================================")
print("FIRMS CLEANING COMPLETE")
print("======================================")

print(f"Clean records : {len(df)}")
print(f"Output file   : {output_file}")

print("\nColumns:")
print(df.columns.tolist())

print("\nDone!")