import geopandas as gpd
import rasterio
from rasterio.mask import mask

# Input files
raster_file = r"C:\Users\hp\Documents\SIH_Industrial_Fire_Project\data\raw\terrascope_download_20260906_141204\WORLDCOVER\ESA_WORLDCOVER_10M_2021_V200\MAP\ESA_WorldCover_10m_2021_v200_N21E084_Map\ESA_WorldCover_10m_2021_v200_N21E084_Map.tif"

boundary_file = r"C:\Users\hp\Documents\SIH_Industrial_Fire_Project\data\raw\Boundary\jamshedpur_study_area.geojson"

output_file = r"C:\Users\hp\Documents\SIH_Industrial_Fire_Project\data\cleaned\LandCover\jamshedpur_landcover.tif"

# Read boundary
boundary = gpd.read_file(boundary_file)

# Open WorldCover raster
with rasterio.open(raster_file) as src:

    # Make sure boundary uses same CRS as raster
    boundary = boundary.to_crs(src.crs)

    # Clip raster
    clipped, transform = mask(
        src,
        boundary.geometry,
        crop=True
    )

    # Update raster metadata
    metadata = src.meta.copy()
    metadata.update({
        "height": clipped.shape[1],
        "width": clipped.shape[2],
        "transform": transform
    })

    # Save clipped raster
    with rasterio.open(output_file, "w", **metadata) as dst:
        dst.write(clipped)

print("Land Cover clipped successfully!")
print("Saved to:")
print(output_file)