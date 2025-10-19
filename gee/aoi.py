from __future__ import annotations

from typing import Optional

import ee

from .utils import load_aoi_geojson


def get_aoi(path: Optional[str] = None) -> ee.Geometry:
    """AOI geometriyi döndür.

    - `path` verilirse ve mevcutsa GeoJSON okunur.
    - Aksi halde İzmir bölgesi için makul bir bbox döndürülür.
    """
    g = load_aoi_geojson(path) if path else None
    if g is not None:
        return g
    # Fallback: approx İzmir bbox
    return ee.Geometry.BBox(26.0, 38.0, 27.5, 39.5)

