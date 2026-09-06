import pandas as pd
from pathlib import Path

# ============================================================
# 1. FILE PATHS
# ============================================================

# India-wide FIRMS CSV
input_file = Path("data/raw/FIRMS/fire_nrt_J2V-C2_799582.csv")

# Output folder
output_folder = Path("data/cleaned/FIRMS")
output_folder.mkdir(parents=True, exist_ok=True)

# Output file
output_file = output_folder / "jamshedpur_firms.csv"


# ============================================================
# 2. Jamshedpur STUDY AREA
# ============================================================

# Our current Jamshedpur study-area boundary
MIN_LON = 86.10
MAX_LON = 86.35
MIN_LAT = 22.70
MAX_LAT = 22.90


# ============================================================
# 3. READ FIRMS DATA
# ============================================================

print("Reading FIRMS India data...")

df = pd.read_csv(input_file)

print(f"Total India FIRMS records: {len(df)}")


# ============================================================
# 4. CHECK REQUIRED COLUMNS
# ============================================================

required_columns = ["latitude", "longitude"]

for column in required_columns:
    if column not in df.columns:
        raise ValueError(
            f"Required column '{column}' not found in FIRMS CSV.\n"
            f"Available columns: {list(df.columns)}"
        )


# ============================================================
# 5. EXTRACT JAMESHEDPUR DATA
# ============================================================

print("Filtering Jamshedpur FIRMS points...")

jamshedpur_df = df[
    (df["longitude"] >= MIN_LON) &
    (df["longitude"] <= MAX_LON) &
    (df["latitude"] >= MIN_LAT) &
    (df["latitude"] <= MAX_LAT)
].copy()


# ============================================================
# 6. REMOVE INVALID COORDINATES
# ============================================================

jamshedpur_df = jamshedpur_df.dropna(
    subset=["latitude", "longitude"]
)


# ============================================================
# 7. REMOVE DUPLICATES
# ============================================================

jamshedpur_df = jamshedpur_df.drop_duplicates()


# ============================================================
# 8. SAVE JAMESHEDPUR FIRMS DATA
# ============================================================

jamshedpur_df.to_csv(output_file, index=False)


# ============================================================
# 9. RESULTS
# ============================================================

print("\n======================================")
print("JAMESHEDPUR FIRMS EXTRACTION COMPLETE")
print("======================================")

print(f"India records       : {len(df)}")
print(f"Jamshedpur records  : {len(jamshedpur_df)}")
print(f"Output file         : {output_file}")

print("\nJamshedpur area:")
print(f"Longitude: {MIN_LON} to {MAX_LON}")
print(f"Latitude : {MIN_LAT} to {MAX_LAT}")

print("\nDone!")