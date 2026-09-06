import pandas as pd
import geopandas as gpd
from pathlib import Path

# ---------------------------------------------------------
# 1. File paths
# ---------------------------------------------------------

firms_file = Path("data/cleaned/FIRMS/jamshedpur_firms_clean.csv")
osm_file = Path("data/cleaned/osm_industrial_clean.geojson")

output_file = Path("data/cleaned/FIRMS/firms_osm_matched.csv")

# ---------------------------------------------------------
# 2. Read FIRMS data
# ---------------------------------------------------------

print("Reading FIRMS data...")
firms = pd.read_csv(firms_file)

print(f"FIRMS records: {len(firms)}")

# Convert FIRMS points into GeoDataFrame
firms_gdf = gpd.GeoDataFrame(
    firms,
    geometry=gpd.points_from_xy(
        firms["longitude"],
        firms["latitude"]
    ),
    crs="EPSG:4326"
)

# ---------------------------------------------------------
# 3. Read OSM industrial data
# ---------------------------------------------------------

print("Reading OSM industrial data...")

osm = gpd.read_file(osm_file)

print(f"OSM industrial features: {len(osm)}")

# Make sure OSM uses same CRS
osm = osm.to_crs("EPSG:4326")

# ---------------------------------------------------------
# 4. Create a projected CRS for distance
# ---------------------------------------------------------

# UTM Zone 45N is suitable for Jamshedpur
firms_projected = firms_gdf.to_crs("EPSG:32645")
osm_projected = osm.to_crs("EPSG:32645")

# ---------------------------------------------------------
# 5. Find nearest industrial location
# ---------------------------------------------------------

print("Finding nearest industrial locations...")

matched = gpd.sjoin_nearest(
    firms_projected,
    osm_projected,
    how="left",
    distance_col="distance_m"
)

# ---------------------------------------------------------
# 6. Rename useful columns
# ---------------------------------------------------------

matched = matched.rename(
    columns={
        "distance_m": "distance_to_industry_m"
    }
)

# ---------------------------------------------------------
# 7. Create near-industry flag
# ---------------------------------------------------------

# 1 = within 1 km of an industrial location
# 0 = farther than 1 km

matched["near_industry"] = (
    matched["distance_to_industry_m"] <= 1000
).astype(int)

# ---------------------------------------------------------
# 8. Convert back to latitude/longitude
# ---------------------------------------------------------

matched = matched.to_crs("EPSG:4326")

# ---------------------------------------------------------
# 9. Remove geometry before saving CSV
# ---------------------------------------------------------

matched = pd.DataFrame(matched.drop(columns="geometry"))

# ---------------------------------------------------------
# 10. Save result
# ---------------------------------------------------------

matched.to_csv(output_file, index=False)

print("\n======================================")
print("FIRMS + OSM MATCHING COMPLETE")
print("======================================")

print(f"FIRMS records : {len(firms)}")
print(f"Matched records: {len(matched)}")
print(f"Output file   : {output_file}")

print("\nNear industry:")
print(matched["near_industry"].value_counts())

print("\nDistance statistics:")
print(matched["distance_to_industry_m"].describe())

print("\nDone!")