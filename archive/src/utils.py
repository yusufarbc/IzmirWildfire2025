import os
import json
from typing import Optional

import ee


def ee_init() -> None:
    """Initialize Earth Engine using user auth or service account if provided.

    Env vars (optional):
      - EE_SERVICE_ACCOUNT: service account email
      - EE_PRIVATE_KEY_FILE: path to JSON key file
    """
    sa = os.getenv("EE_SERVICE_ACCOUNT")
    key_file = os.getenv("EE_PRIVATE_KEY_FILE")
    if sa and key_file and os.path.exists(key_file):
        credentials = ee.ServiceAccountCredentials(sa, key_file)
        ee.Initialize(credentials)
    else:
        # Falls back to stored user credentials (earthengine authenticate)
        ee.Initialize()


def ensure_dir(path: str) -> None:
    os.makedirs(path, exist_ok=True)


def load_aoi_geojson(path: str) -> Optional[ee.Geometry]:
    """Load AOI from a GeoJSON file into ee.Geometry if file exists."""
    if not os.path.exists(path):
        return None
    with open(path, "r", encoding="utf-8") as f:
        gj = json.load(f)
    # Works with Polygon/MultiPolygon or Feature(Geometry)
    if gj.get("type") == "Feature":
        geom = gj.get("geometry")
    else:
        geom = gj
    return ee.Geometry(geom)

