import ee
from src.utils import load_aoi_geojson


def get_aoi(geojson_path: str = "data/aoi.geojson") -> ee.Geometry:
    """Return AOI geometry. If GeoJSON exists, use it; else fallback to Karabük bbox.

    Default bbox roughly covers Karabük and vicinity.
    """
    geom = load_aoi_geojson(geojson_path)
    if geom is not None:
        return geom
    # Fallback bbox: [minLon, minLat, maxLon, maxLat]
    return ee.Geometry.Rectangle([32.3, 41.0, 33.0, 41.5])

