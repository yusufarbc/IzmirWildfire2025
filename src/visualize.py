from typing import Dict
import os
import csv

import ee
import folium

from src.utils import ensure_dir


def _center_of(aoi: ee.Geometry):
    c = aoi.centroid(10).coordinates().getInfo()
    return [c[1], c[0]]  # lat, lon


def vis_params() -> Dict[str, dict]:
    return {
        "NDVI": {"min": -0.2, "max": 0.9, "palette": ["#440154", "#3b528b", "#21908d", "#5dc963", "#fde725"]},
        "NBR": {"min": -0.5, "max": 1.0, "palette": ["#8b0000", "#ff8c00", "#ffff00", "#00ff00", "#006400"]},
        "dNDVI": {"min": -0.6, "max": 0.6, "palette": ["#8b0000", "#ff8c00", "#ffffbf", "#a6d96a", "#1a9850"]},
        "dNBR": {"min": -0.2, "max": 1.0, "palette": ["#2b83ba", "#abdda4", "#ffffbf", "#fdae61", "#d7191c"]},
        "severity": {"min": 0, "max": 4, "palette": ["#1a9850", "#a6d96a", "#fee08b", "#f46d43", "#a50026"]},
    }


def _add_ee_tile(m: folium.Map, image: ee.Image, vis: dict, name: str):
    m.set_options = True
    map_id = image.getMapId(vis)
    # Newer earthengine-api exposes tile_fetcher, fallback to legacy keys
    tiles_url = None
    if isinstance(map_id, dict):
        tf = map_id.get("tile_fetcher")
        if tf is not None and hasattr(tf, "url_format"):
            tiles_url = tf.url_format
        elif "tile_url_template" in map_id:
            tiles_url = map_id["tile_url_template"]
        elif "mapid" in map_id and "token" in map_id:
            tiles_url = (f"https://earthengine.googleapis.com/map/{map_id['mapid']}/{map_id['token']}/{{z}}/{{x}}/{{y}}?vis={vis}")
    if not tiles_url:
        raise RuntimeError("Unable to retrieve EE tiles URL.")
    folium.raster_layers.TileLayer(
        tiles=tiles_url,
        attr="Google Earth Engine",
        name=name,
        overlay=True,
        control=True,
        show=True,
    ).add_to(m)


def save_folium(image: ee.Image, aoi: ee.Geometry, vis: dict, name: str, out_html: str):
    ensure_dir(os.path.dirname(out_html))
    m = folium.Map(location=_center_of(aoi), zoom_start=9, control_scale=True)
    _add_ee_tile(m, image, vis, name)
    folium.LayerControl().add_to(m)
    m.save(out_html)


def reduce_mean(image: ee.Image, aoi: ee.Geometry, band: str, scale: int = 20) -> float:
    stats = image.select(band).reduceRegion(
        reducer=ee.Reducer.mean(), geometry=aoi, scale=scale, maxPixels=1e13
    )
    val = stats.get(band).getInfo()
    return float(val) if val is not None else float("nan")


def write_summary_csv(path: str, rows: Dict[str, float]):
    ensure_dir(os.path.dirname(path))
    with open(path, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["metric", "value"])
        for k, v in rows.items():
            w.writerow([k, v])

