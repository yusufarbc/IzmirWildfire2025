"""AOI (Area of Interest) yardımcıları.

GeoJSON varsa dosyadan yükler; yoksa İzmir çevresi için varsayılan
yaklaşık bir bbox döndürür.
"""

import ee
from src.utils import load_aoi_geojson


def get_aoi(geojson_path: str = "src/aoi.geojson") -> ee.Geometry:
    """AOI geometrisini döndürür.

    Args:
        geojson_path: AOI GeoJSON dosya yolu
    Returns:
        ee.Geometry (GeoJSON yoksa varsayılan bbox)
    """
    geom = load_aoi_geojson(geojson_path)
    if geom is not None:
        return geom
    # Varsayılan bbox: [minLon, minLat, maxLon, maxLat]
    return ee.Geometry.Rectangle([26.0, 38.0, 27.6, 39.4])


