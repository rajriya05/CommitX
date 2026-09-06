import geopandas as gpd
import pandas as pd

osm = gpd.read_file("../data/raw/export - Copy.geojson")

print(osm.head())
print(osm.columns)
print(osm.shape)


# Remove completely empty columns
osm = osm.dropna(axis=1, how="all")

# Check missing values
print("\nMissing values:")
print(osm.isnull().sum())



# Keep useful columns for our project
useful_columns = [
    "id",
    "name",
    "operator",
    "landuse",
    "plant:method",
    "plant:output:electricity",
    "plant:source",
    "power",
    "start_date",
    "geometry"
]

osm_clean = osm[useful_columns].copy()

print("\nCleaned data:")
print(osm_clean.head())
print("\nShape:", osm_clean.shape)

# Add latitude and longitude
osm_clean = osm_clean.to_crs("EPSG:4326")

osm_clean["longitude"] = osm_clean.geometry.x
osm_clean["latitude"] = osm_clean.geometry.y

print("\nCoordinates:")
print(osm_clean[["name", "latitude", "longitude"]].head())


# Save cleaned data as CSV
osm_clean.drop(columns="geometry").to_csv(
    "../data/cleaned/osm_industrial_clean.csv",
    index=False
)

# Save cleaned data as GeoJSON
osm_clean.to_file(
    "../data/cleaned/osm_industrial_clean.geojson",
    driver="GeoJSON"
)

print("\nCleaned files saved successfully!")
