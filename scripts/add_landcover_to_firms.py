import pandas as pd
import geopandas as gpd
import rasterio
from pathlib import Path

# ---------------------------------------------------------
# 1. File paths
# ---------------------------------------------------------

firms_file = Path(
    "data/cleaned/FIRMS/firms_osm_matched.csv"
)

landcover_file = Path(
    "data/cleaned/LandCover/jamshedpur_landcover.tif"
)

output_file = Path(
    "data/cleaned/FIRMS/firms_osm_landcover.csv"
)

# ---------------------------------------------------------
# 2. Read FIRMS + OSM data
# ---------------------------------------------------------

print("Reading FIRMS + OSM data...")

df = pd.read_csv(firms_file)

print(f"Records: {len(df)}")

# ---------------------------------------------------------
# 3. Create FIRMS points
# ---------------------------------------------------------

points = gpd.GeoDataFrame(
    df,
    geometry=gpd.points_from_xy(
        df["longitude_left"],
        df["latitude_left"]
    ),
    crs="EPSG:4326"
)

# ---------------------------------------------------------
# 4. Open Land Cover raster
# ---------------------------------------------------------

print("Reading Land Cover raster...")

with rasterio.open(landcover_file) as src:

    # Convert FIRMS points to raster CRS
    points = points.to_crs(src.crs)

    # Coordinates of FIRMS points
    coordinates = [
        (point.x, point.y)
        for point in points.geometry
    ]

    # Extract land-cover value
    values = list(src.sample(coordinates))

# ---------------------------------------------------------
# 5. Add land-cover class
# ---------------------------------------------------------

points["landcover_class"] = [
    int(value[0]) for value in values
]

# ---------------------------------------------------------
# 6. ESA WorldCover class names
# ---------------------------------------------------------

worldcover_classes = {
    10: "Tree cover",
    20: "Shrubland",
    30: "Grassland",
    40: "Cropland",
    50: "Built-up",
    60: "Bare / sparse vegetation",
    70: "Snow and ice",
    80: "Permanent water bodies",
    90: "Herbaceous wetland",
    95: "Mangroves",
    100: "Moss and lichen"
}

points["landcover_name"] = points["landcover_class"].map(
    worldcover_classes
)

# ---------------------------------------------------------
# 7. Convert back to WGS84
# ---------------------------------------------------------

points = points.to_crs("EPSG:4326")

# ---------------------------------------------------------
# 8. Remove geometry
# ---------------------------------------------------------

points = pd.DataFrame(
    points.drop(columns="geometry")
)

# ---------------------------------------------------------
# 9. Save output
# ---------------------------------------------------------

points.to_csv(output_file, index=False)

# ---------------------------------------------------------
# 10. Results
# ---------------------------------------------------------

print("\n======================================")
print("LAND COVER EXTRACTION COMPLETE")
print("======================================")

print(f"Records: {len(points)}")

print("\nLand Cover classes:")
print(
    points["landcover_name"]
    .value_counts(dropna=False)
)

print("\nOutput file:")
print(output_file)

print("\nDone!")