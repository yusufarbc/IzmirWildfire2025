"""Uçtan uca analiz hattı (pipeline)

Bu modül, tarih aralıkları ve AOI verildiğinde:
1) Sentinel‑2 median kompozitleri hazırlar
2) NDVI/NBR ve farkları (dNDVI/dNBR) hesaplar
3) dNBR şiddet sınıflarını üretir
4) Folium haritalarını HTML olarak kaydeder
5) Özet istatistikleri CSV olarak yazar
"""

from typing import Dict, Optional
import os

import ee

from src.utils import ee_init, ensure_dir
from src.gee.aoi import get_aoi
from src.gee.preprocess import prepare_composite
from src.gee.indices import with_indices
from src.gee.change import compute_diffs, classify_dnbr
from src.visualize import (
    vis_params,
    save_folium,
    reduce_mean,
    write_summary_csv,
    compute_severity_areas,
    write_kv_csv,
)


def run_pipeline(
    pre_start: str,
    pre_end: str,
    post_start: str,
    post_end: str,
    aoi_geojson: str = "src/aoi.geojson",
    out_dir: str = "results",
    project: Optional[str] = None,
    area_scale: int = 10,
) -> Dict[str, str]:
    """Analizi çalıştırır ve çıktı dosya yollarını döndürür.

    Args:
        pre_start: Ön dönem başlangıç tarihi (YYYY-MM-DD)
        pre_end: Ön dönem bitiş tarihi (YYYY-MM-DD)
        post_start: Sonraki dönem başlangıç tarihi
        post_end: Sonraki dönem bitiş tarihi
        aoi_geojson: AOI GeoJSON yolu (yoksa varsayılan bbox kullanılır)
        out_dir: Çıktı klasörü
        project: (opsiyonel) GEE proje ID
    Returns:
        Üretilen haritalar ve CSV’nin dosya yolları.
    """
    ee_init(project)
    aoi = get_aoi(aoi_geojson)

    # Prepare median composites and indices
    pre = with_indices(prepare_composite(aoi, pre_start, pre_end))
    post = with_indices(prepare_composite(aoi, post_start, post_end))

    diffs = compute_diffs(pre, post)
    severity = classify_dnbr(diffs["dNBR"])  # 0..4

    vp = vis_params()
    ensure_dir(out_dir)

    outputs = {}
    # Date range labels
    pre_label = f"{pre_start}–{pre_end}"
    post_label = f"{post_start}–{post_end}"
    # Maps
    # True color (RGB)
    outputs["pre_rgb_map"] = os.path.join(out_dir, f"pre_RGB_{pre_start}_{pre_end}.html")
    save_folium(pre, aoi, vp["RGB"], f"Pre RGB {pre_label}", outputs["pre_rgb_map"])

    outputs["post_rgb_map"] = os.path.join(out_dir, f"post_RGB_{post_start}_{post_end}.html")
    save_folium(post, aoi, vp["RGB"], f"Post RGB {post_label}", outputs["post_rgb_map"])
    outputs["pre_ndvi_map"] = os.path.join(out_dir, "pre_NDVI.html")
    save_folium(pre.select("NDVI"), aoi, vp["NDVI"], f"Pre NDVI {pre_label}", outputs["pre_ndvi_map"])

    outputs["post_ndvi_map"] = os.path.join(out_dir, "post_NDVI.html")
    save_folium(post.select("NDVI"), aoi, vp["NDVI"], f"Post NDVI {post_label}", outputs["post_ndvi_map"])

    outputs["pre_nbr_map"] = os.path.join(out_dir, "pre_NBR.html")
    save_folium(pre.select("NBR"), aoi, vp["NBR"], f"Pre NBR {pre_label}", outputs["pre_nbr_map"])

    outputs["post_nbr_map"] = os.path.join(out_dir, "post_NBR.html")
    save_folium(post.select("NBR"), aoi, vp["NBR"], f"Post NBR {post_label}", outputs["post_nbr_map"])

    outputs["dndvi_map"] = os.path.join(out_dir, "dNDVI.html")
    save_folium(diffs["dNDVI"], aoi, vp["dNDVI"], f"dNDVI {pre_label}→{post_label}", outputs["dndvi_map"])

    outputs["dnbr_map"] = os.path.join(out_dir, "dNBR.html")
    save_folium(diffs["dNBR"], aoi, vp["dNBR"], f"dNBR {pre_label}→{post_label}", outputs["dnbr_map"])

    outputs["severity_map"] = os.path.join(out_dir, "severity.html")
    save_folium(severity, aoi, vp["severity"], f"dNBR Severity {pre_label}→{post_label}", outputs["severity_map"])

    # Summary stats
    summary = {
        "pre_mean_NDVI": reduce_mean(pre, aoi, "NDVI"),
        "post_mean_NDVI": reduce_mean(post, aoi, "NDVI"),
        "mean_dNDVI": reduce_mean(diffs["dNDVI"], aoi, "dNDVI"),
        "mean_dNBR": reduce_mean(diffs["dNBR"], aoi, "dNBR"),
    }
    outputs["summary_csv"] = os.path.join(out_dir, "summary_stats.csv")
    write_summary_csv(outputs["summary_csv"], summary)

    # Severity alan istatistikleri (EE pixelArea) ve toplam yanmış alan
    areas = compute_severity_areas(severity, aoi, scale=area_scale)
    outputs["severity_areas_csv"] = os.path.join(out_dir, "severity_areas.csv")
    write_kv_csv(outputs["severity_areas_csv"], areas)

    return outputs

