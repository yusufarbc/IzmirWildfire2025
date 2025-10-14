from typing import Dict
import os

import ee

from src.utils import ee_init, ensure_dir
from src.gee.aoi import get_aoi
from src.gee.preprocess import prepare_composite
from src.gee.indices import with_indices
from src.gee.change import compute_diffs, classify_dnbr
from src.visualize import vis_params, save_folium, reduce_mean, write_summary_csv


def run_pipeline(
    pre_start: str,
    pre_end: str,
    post_start: str,
    post_end: str,
    aoi_geojson: str = "data/aoi.geojson",
    out_dir: str = "results",
) -> Dict[str, str]:
    ee_init()
    aoi = get_aoi(aoi_geojson)

    # Prepare median composites and indices
    pre = with_indices(prepare_composite(aoi, pre_start, pre_end))
    post = with_indices(prepare_composite(aoi, post_start, post_end))

    diffs = compute_diffs(pre, post)
    severity = classify_dnbr(diffs["dNBR"])  # 0..4

    vp = vis_params()
    ensure_dir(out_dir)

    outputs = {}
    # Maps
    outputs["pre_ndvi_map"] = os.path.join(out_dir, "pre_NDVI.html")
    save_folium(pre.select("NDVI"), aoi, vp["NDVI"], "Pre NDVI", outputs["pre_ndvi_map"])

    outputs["post_ndvi_map"] = os.path.join(out_dir, "post_NDVI.html")
    save_folium(post.select("NDVI"), aoi, vp["NDVI"], "Post NDVI", outputs["post_ndvi_map"])

    outputs["pre_nbr_map"] = os.path.join(out_dir, "pre_NBR.html")
    save_folium(pre.select("NBR"), aoi, vp["NBR"], "Pre NBR", outputs["pre_nbr_map"])

    outputs["post_nbr_map"] = os.path.join(out_dir, "post_NBR.html")
    save_folium(post.select("NBR"), aoi, vp["NBR"], "Post NBR", outputs["post_nbr_map"])

    outputs["dndvi_map"] = os.path.join(out_dir, "dNDVI.html")
    save_folium(diffs["dNDVI"], aoi, vp["dNDVI"], "dNDVI", outputs["dndvi_map"])

    outputs["dnbr_map"] = os.path.join(out_dir, "dNBR.html")
    save_folium(diffs["dNBR"], aoi, vp["dNBR"], "dNBR", outputs["dnbr_map"])

    outputs["severity_map"] = os.path.join(out_dir, "severity.html")
    save_folium(severity, aoi, vp["severity"], "dNBR Severity", outputs["severity_map"])

    # Summary stats
    summary = {
        "pre_mean_NDVI": reduce_mean(pre, aoi, "NDVI"),
        "post_mean_NDVI": reduce_mean(post, aoi, "NDVI"),
        "mean_dNDVI": reduce_mean(diffs["dNDVI"], aoi, "dNDVI"),
        "mean_dNBR": reduce_mean(diffs["dNBR"], aoi, "dNBR"),
    }
    outputs["summary_csv"] = os.path.join(out_dir, "summary_stats.csv")
    write_summary_csv(outputs["summary_csv"], summary)

    return outputs

