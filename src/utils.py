"""Genel yardımcılar ve GEE başlatma (initialize) işlevleri.

- ee_init: Kimlik doğrulama bilgileriyle GEE başlatır (kullanıcı/servis hesabı)
- ensure_dir: Klasör yoksa oluşturur
- load_aoi_geojson: GeoJSON dosyasını ee.Geometry olarak yükler
"""

import os
import json
from typing import Optional

import ee


def _resolve_project(explicit: Optional[str] = None) -> Optional[str]:
    """GEE proje kimliğini (ID) belirler.

    Öncelik: fonksiyon argümanı > EE_PROJECT/EARTHENGINE_PROJECT >
    GOOGLE_CLOUD_PROJECT/GCLOUD_PROJECT
    """
    return (
        explicit
        or os.getenv("EE_PROJECT")
        or os.getenv("EARTHENGINE_PROJECT")
        or os.getenv("GOOGLE_CLOUD_PROJECT")
        or os.getenv("GCLOUD_PROJECT")
    )


def ee_init(project: Optional[str] = None) -> None:
    """Earth Engine'i kullanıcı veya servis hesabıyla başlatır.

    Ortam değişkenleri (opsiyonel):
      - EE_SERVICE_ACCOUNT: Servis hesabı e‑posta adresi
      - EE_PRIVATE_KEY_FILE: JSON anahtar dosya yolu
      - EE_PROJECT / EARTHENGINE_PROJECT / GOOGLE_CLOUD_PROJECT / GCLOUD_PROJECT: Proje ID
    """
    sa = os.getenv("EE_SERVICE_ACCOUNT")
    key_file = os.getenv("EE_PRIVATE_KEY_FILE")
    project_id = _resolve_project(project)
    try:
        if sa and key_file and os.path.exists(key_file):
            credentials = ee.ServiceAccountCredentials(sa, key_file)
            ee.Initialize(credentials=credentials, project=project_id)
        else:
            try:
                # Falls back to stored user credentials (earthengine authenticate)
                ee.Initialize(project=project_id)
            except Exception:
                # Interactive browser auth if not already authenticated
                ee.Authenticate()
                ee.Initialize(project=project_id)
    except Exception as e:
        hint = "; set EE_PROJECT env var or pass project=" if not project_id else ""
        raise RuntimeError(f"Earth Engine init failed{hint}: {e}")


def ensure_dir(path: str) -> None:
    """Verilen yolu (varsa üstleriyle birlikte) oluşturur."""
    os.makedirs(path, exist_ok=True)


def load_aoi_geojson(path: str) -> Optional[ee.Geometry]:
    """GeoJSON dosyasından AOI'yi `ee.Geometry` olarak yükler.

    Feature veya (Multi)Polygon geometri desteklenir.
    """
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
