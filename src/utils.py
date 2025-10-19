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

    Tercih sırası:
      1) Servis hesabı (EE_SERVICE_ACCOUNT + EE_PRIVATE_KEY_FILE)
      2) Kullanıcı kimliği (earthengine authenticate)

    Proje ID belirleme:
      - project argümanı veya ortam değişkenleri (EE_PROJECT / EARTHENGINE_PROJECT / GOOGLE_CLOUD_PROJECT / GCLOUD_PROJECT)
      - Proje ID bulunamazsa, Initialize() proje parametresi olmadan denenir (kısmi kullanım için yeterli olabilir).
    """
    sa = os.getenv("EE_SERVICE_ACCOUNT")
    key_file = os.getenv("EE_PRIVATE_KEY_FILE")
    print(f"[ee_init] requested project arg: {project!r}")
    # Project must be a string Project ID (name), not a numeric project number.
    if project is not None:
        if not isinstance(project, str):
            raise ValueError("ee_init: 'project' must be a string Project ID (e.g., 'karabukwildfire2025'), not a numeric project number.")
        if project.isdigit():
            raise ValueError("ee_init: received a numeric-looking value. Pass the Project ID (e.g., 'karabukwildfire2025'), not the project number.")
    project_id = _resolve_project(project)
    print(f"[ee_init] resolved project_id: {project_id!r}")

    def _init_with(creds=None):
        if project_id:
            ee.Initialize(credentials=creds, project=project_id)
        else:
            # Son çare: projeyi belirtmeden başlat (bazı okuma işlemleri için yeterli olabilir)
            ee.Initialize(credentials=creds)

    try:
        if sa and key_file and os.path.exists(key_file):
            print("[ee_init] using service account credentials")
            credentials = ee.ServiceAccountCredentials(sa, key_file)
            _init_with(credentials)
        else:
            try:
                _init_with()
            except Exception:
                print("[ee_init] user OAuth required; calling ee.Authenticate()")
                ee.Authenticate()
                _init_with()
    except Exception as e:
        if not project_id:
            raise RuntimeError(
                "Earth Engine init failed: Proje ID bulunamadı. EE_PROJECT veya EARTHENGINE_PROJECT ortam değişkenini ayarlayın ya da 'project' parametresi geçin. Orijinal hata: "
                + str(e)
            )
        raise RuntimeError(f"Earth Engine init failed for project '{project_id}': {e}")


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
