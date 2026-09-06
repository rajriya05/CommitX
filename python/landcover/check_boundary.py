import geopandas as gpd

file = r"C:\Users\hp\Documents\SIH_Industrial_Fire_Project\data\raw\Boundary\jamshedpur_study_area.geojson"

boundary = gpd.read_file(file)

print("Number of features:", len(boundary))
print("CRS:", boundary.crs)
print("Geometry types:")
print(boundary.geom_type.value_counts())
print("Bounds:", boundary.total_bounds)