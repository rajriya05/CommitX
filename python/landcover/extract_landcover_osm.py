import geopandas as gpd
import rasterio
import pandas as pd

# Files
osm_file = r"C:\Users\hp\Documents\SIH_Industrial_Fire_Project\data\cleaned\osm_industrial_clean.geojson"

landcover_file = r"C:\Users\hp\Documents\SIH_Industrial_Fire_Project\data\cleaned\LandCover\jamshedpur_landcover.tif"

output_file = r"C:\Users\hp\Documents\SIH_Industrial_Fire_Project\data\cleaned\osm_industrial_landcover.geojson"

# Read OSM points
osm = gpd.read_file(osm_file)

# Open Land Cover raster
with rasterio.open(landcover_file) as src:

    # Make CRS same as raster
    osm = osm.to_crs(src.crs)

    # Get coordinates of each OSM point
    coordinates = [(point.x, point.y) for point in osm.geometry]

    # Extract land-cover value at each point
    values = [value[0] for value in src.sample(coordinates)]

# Add land-cover class
osm["landcover_class"] = values

# Add readable land-cover names
landcover_names = {
    10: "Tree cover",
    20: "Shrubland",
    30: "Grassland",
    40: "Cropland",
    50: "Built-up",
    60: "Bare/sparse vegetation",
    70: "Snow/ice",
    80: "Water",
    90: "Wetland",
    95: "Mangroves",
    100: "Moss/lichen"
}

osm["landcover_name"] = osm["landcover_class"].map(landcover_names)

# Save combined data
osm.to_file(output_file, driver="GeoJSON")

print("OSM + Land Cover combined successfully!")
print("Features:", len(osm))
print("Saved to:", output_file)

print("\nLand Cover classes at industrial locations:")
print(osm["landcover_name"].value_counts())