"""Genel yardımcılar ve GEE başlatma (initialize) işlevleri.

- ee_init: Google Earth Engine oturumu açar (kullanıcı OAuth)
- ensure_dir: Klasör yoksa oluşturur
- load_aoi_geojson: GeoJSON dosyasını ee.Geometry olarak yükler
"""

from __future__ import annotations

import os
import json
from typing import Optional

import ee


def ee_init(project: Optional[str] = None) -> None:
    """Earth Engine'i kullanıcı OAuth ile başlat.

    Parametre olarak yalnızca Project ID kabul edilir (örn: "your-gcp-project").
    Servis hesabı ve ortam değişkenleri bu basit yordamda kullanılmaz.
    """
    project_id = project
    if project_id is not None:
        if not isinstance(project_id, str):
            raise ValueError("ee_init: 'project' must be a string Project ID, not a number.")
        if project_id.isdigit():
            raise ValueError("ee_init: received a numeric-looking value. Pass Project ID, not project number.")

    def _init() -> None:
        if project_id:
            ee.Initialize(project=project_id)
        else:
            ee.Initialize()

    try:
        try:
            _init()
        except Exception:
            ee.Authenticate()
            _init()
    except Exception as e:  # pragma: no cover - environment dependent
        if not project_id:
            raise RuntimeError(
                "Earth Engine init failed: Proje ID yok. 'project' parametresi geçin. Orijinal hata: "
                + str(e)
            )
        raise RuntimeError(f"Earth Engine init failed for project '{project_id}': {e}")


def ensure_dir(path: str) -> None:
    """Verilen yolu (varsa üstleriyle birlikte) oluşturur."""
    if path:
        os.makedirs(path, exist_ok=True)


def load_aoi_geojson(path: str) -> Optional[ee.Geometry]:
    """GeoJSON dosyasından AOI'yi `ee.Geometry` olarak yükler.

    Feature veya (Multi)Polygon geometri desteklenir.
    Dosya bulunamazsa None döner.
    """
    if not path or not os.path.exists(path):
        return None
    with open(path, "r", encoding="utf-8") as f:
        gj = json.load(f)
    # Works with Polygon/MultiPolygon or Feature(Geometry)
    if isinstance(gj, dict) and gj.get("type") == "Feature":
        geom = gj.get("geometry")
    else:
        geom = gj
    return ee.Geometry(geom)

