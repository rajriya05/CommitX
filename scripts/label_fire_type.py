import pandas as pd
import os

# ---------------------------------------
# FILE PATHS
# ---------------------------------------

input_file = "data/cleaned/FIRMS/firms_osm_landcover_clean.csv"

output_file = "data/cleaned/FIRMS/firms_fire_type_labeled.csv"


# ---------------------------------------
# LOAD DATASET
# ---------------------------------------

print("Loading combined dataset...")

df = pd.read_csv(input_file)

print(f"Total records: {len(df)}")


# ---------------------------------------
# FIRE TYPE LABELING
# ---------------------------------------

def assign_fire_type(row):

    # Convert text fields to lowercase
    landuse = str(row.get("landuse", "")).lower()
    landcover_name = str(row.get("landcover_name", "")).lower()
    landcover_class = str(row.get("landcover_class", "")).lower()

    # Distance from nearest industry
    try:
        distance = float(row.get("distance_to_industry_m", 999999))
    except:
        distance = 999999

    # Proximity indicators
    try:
        near_industry = int(row.get("near_industry", 0))
    except:
        near_industry = 0

    try:
        near_500m = int(row.get("near_industry_500m", 0))
    except:
        near_500m = 0

    try:
        near_1km = int(row.get("near_industry_1km", 0))
    except:
        near_1km = 0

    try:
        near_2km = int(row.get("near_industry_2km", 0))
    except:
        near_2km = 0


    # -----------------------------------
    # 1. INDUSTRIAL FIRE
    # -----------------------------------

    if (
        "industrial" in landuse
        or "industrial" in landcover_name
        or "industrial" in landcover_class
        or near_500m == 1
        or distance <= 500
    ):
        return "Industrial"


    # -----------------------------------
    # 2. AGRICULTURAL FIRE
    # -----------------------------------

    elif (
        "cropland" in landcover_name
        or "crop" in landcover_name
        or "agriculture" in landcover_name
        or "farmland" in landcover_name
        or "cropland" in landcover_class
        or "agriculture" in landcover_class
        or "farmland" in landcover_class
    ):
        return "Agricultural"


    # -----------------------------------
    # 3. VEGETATION FIRE
    # -----------------------------------

    elif (
        "forest" in landcover_name
        or "tree" in landcover_name
        or "grass" in landcover_name
        or "shrub" in landcover_name
        or "vegetation" in landcover_name
        or "forest" in landcover_class
        or "tree" in landcover_class
        or "grass" in landcover_class
        or "shrub" in landcover_class
        or "vegetation" in landcover_class
    ):
        return "Vegetation"


    # -----------------------------------
    # 4. OTHER
    # -----------------------------------

    else:
        return "Other"


# Apply the labeling function

df["fire_type"] = df.apply(assign_fire_type, axis=1)


# ---------------------------------------
# SAVE LABELED DATASET
# ---------------------------------------

df.to_csv(output_file, index=False)


# ---------------------------------------
# DISPLAY RESULTS
# ---------------------------------------

print("\n======================================")
print("FIRE TYPE LABELING COMPLETE")
print("======================================")

print(f"Total records : {len(df)}")

print("\nFire type distribution:")
print(df["fire_type"].value_counts())

print("\nOutput file:")
print(output_file)

print("\nDone!")