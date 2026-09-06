import geopandas as gpd
from shapely.geometry import box

# Jamshedpur study area
min_lon, min_lat = 86.10, 22.70
max_lon, max_lat = 86.35, 22.90

boundary = gpd.GeoDataFrame(
    {"name": ["Jamshedpur Study Area"]},
    geometry=[box(min_lon, min_lat, max_lon, max_lat)],
    crs="EPSG:4326"
)

output = r"C:\Users\hp\Documents\SIH_Industrial_Fire_Project\data\raw\Boundary\jamshedpur_study_area.geojson"

boundary.to_file(output, driver="GeoJSON")

print("Boundary created successfully!")
print("Saved to:", output)
print("Bounds:", boundary.total_bounds)