import pandas as pd
from pathlib import Path

# ---------------------------------------------------------
# 1. File paths
# ---------------------------------------------------------

input_file = Path(
    "data/cleaned/FIRMS/firms_osm_landcover.csv"
)

output_file = Path(
    "data/cleaned/FIRMS/firms_osm_landcover_clean.csv"
)

# ---------------------------------------------------------
# 2. Read merged dataset
# ---------------------------------------------------------

print("Reading merged FIRMS + OSM + Land Cover data...")

df = pd.read_csv(input_file)

print(f"Original records: {len(df)}")
print(f"Original columns: {len(df.columns)}")

# ---------------------------------------------------------
# 3. Rename FIRMS coordinates
# ---------------------------------------------------------

df = df.rename(
    columns={
        "latitude_left": "latitude",
        "longitude_left": "longitude"
    }
)

# ---------------------------------------------------------
# 4. Remove unnecessary technical columns
# ---------------------------------------------------------

columns_to_remove = [
    "index_right",
    "longitude_right",
    "latitude_right"
]

df = df.drop(
    columns=columns_to_remove,
    errors="ignore"
)

# ---------------------------------------------------------
# 5. Remove duplicate FIRMS observations
# ---------------------------------------------------------

df = df.drop_duplicates(
    subset=[
        "latitude",
        "longitude",
        "acq_date",
        "acq_time",
        "frp"
    ]
)

# ---------------------------------------------------------
# 6. Check required numerical columns
# ---------------------------------------------------------

numeric_columns = [
    "latitude",
    "longitude",
    "brightness",
    "scan",
    "track",
    "bright_t31",
    "frp",
    "distance_to_industry_m"
]

for column in numeric_columns:
    df[column] = pd.to_numeric(
        df[column],
        errors="coerce"
    )

# ---------------------------------------------------------
# 7. Remove records with missing important values
# ---------------------------------------------------------

required_columns = [
    "latitude",
    "longitude",
    "brightness",
    "frp",
    "distance_to_industry_m",
    "landcover_class",
    "landcover_name"
]

df = df.dropna(
    subset=required_columns
)

# ---------------------------------------------------------
# 8. Validate FIRMS coordinates
# ---------------------------------------------------------

df = df[
    (df["latitude"] >= 22.70) &
    (df["latitude"] <= 22.90) &
    (df["longitude"] >= 86.10) &
    (df["longitude"] <= 86.35)
]

# ---------------------------------------------------------
# 9. Create useful distance features
# ---------------------------------------------------------

df["near_industry_500m"] = (
    df["distance_to_industry_m"] <= 500
).astype(int)

df["near_industry_1km"] = (
    df["distance_to_industry_m"] <= 1000
).astype(int)

df["near_industry_2km"] = (
    df["distance_to_industry_m"] <= 2000
).astype(int)

# ---------------------------------------------------------
# 10. Save final clean dataset
# ---------------------------------------------------------

df.to_csv(
    output_file,
    index=False
)

# ---------------------------------------------------------
# 11. Print results
# ---------------------------------------------------------

print("\n======================================")
print("FINAL MERGED DATA CLEANING COMPLETE")
print("======================================")

print(f"Final records : {len(df)}")
print(f"Final columns : {len(df.columns)}")

print("\nColumns:")
print(df.columns.tolist())

print("\nMissing values:")
print(df.isnull().sum())

print("\nLand Cover:")
print(df["landcover_name"].value_counts())

print("\nIndustry distance:")
print(df["distance_to_industry_m"].describe())

print("\nOutput file:")
print(output_file)

print("\nDone!")