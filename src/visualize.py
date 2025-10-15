"""Görselleştirme ve özet istatistik yardımcıları

Bu modül, GEE `ee.Image` çıktılarından folium tabanlı haritalar üretir ve
AOI üzerinde basit özet istatistikleri (ortalama) hesaplayıp CSV’e yazar.

Best‑practice dokunuşları:
- Earth Engine tile URL alma mantığı yeni/legacy sürümlerle uyumlu.
- İsteğe bağlı açıklamalar/legend ekleyebilmek için yardımcılar mevcut.

Fonksiyonlar:
- vis_params: Harita katmanları için görselleştirme parametreleri
- save_folium: Verilen görüntüyü folium haritası olarak HTML’e kaydeder
- reduce_mean: AOI üzerinde seçili bandın ortalamasını hesaplar
- write_summary_csv: Anahtar/değer özetlerini CSV’e yazar
"""

from typing import Dict, Optional, Sequence
import os
import csv

import ee
import folium
from branca.colormap import LinearColormap

from src.utils import ensure_dir


def _center_of(aoi: ee.Geometry):
    """AOI geometrisinin merkezini (lat, lon) döndürür.

    Args:
        aoi: ee.Geometry çalışma alanı
    Returns:
        [enlem, boylam] listesi
    """
    c = aoi.centroid(10).coordinates().getInfo()
    return [c[1], c[0]]  # lat, lon


def vis_params() -> Dict[str, dict]:
    """Harita katmanları için varsayılan görselleştirme parametreleri.

    Returns:
        Her katman adı için min/max ve palette değerleri içeren sözlük.
    """
    return {
        "NDVI": {"min": -0.2, "max": 0.9, "palette": ["#440154", "#3b528b", "#21908d", "#5dc963", "#fde725"]},
        "NBR": {"min": -0.5, "max": 1.0, "palette": ["#8b0000", "#ff8c00", "#ffff00", "#00ff00", "#006400"]},
        "dNDVI": {"min": -0.6, "max": 0.6, "palette": ["#8b0000", "#ff8c00", "#ffffbf", "#a6d96a", "#1a9850"]},
        "dNBR": {"min": -0.2, "max": 1.0, "palette": ["#2b83ba", "#abdda4", "#ffffbf", "#fdae61", "#d7191c"]},
        "severity": {"min": 0, "max": 4, "palette": ["#1a9850", "#a6d96a", "#fee08b", "#f46d43", "#a50026"]},
    }


def _ee_tile_url(image: ee.Image, vis: dict) -> str:
    """GEE tile URL’sini güvenli şekilde elde et.

    Yeni sürümlerde `tile_fetcher.url_format` bulunur. Legacy’de
    `tile_url_template` ya da `mapid`/`token` ile kurulur.
    """
    info = image.getMapId(vis)
    if isinstance(info, dict):
        tf = info.get("tile_fetcher")
        if tf is not None and hasattr(tf, "url_format"):
            return tf.url_format
        if "tile_url_template" in info:
            return info["tile_url_template"]
        # Legacy explicit URL (vis mapid içinde gömülüdür; query eklemeyiz)
        if "mapid" in info and "token" in info:
            return f"https://earthengine.googleapis.com/map/{info['mapid']}/{{z}}/{{x}}/{{y}}?token={info['token']}"
    raise RuntimeError("Unable to retrieve EE tiles URL.")


def _add_ee_tile(m: folium.Map, image: ee.Image, vis: dict, name: str, opacity: float = 1.0):
    """Folium haritasına GEE görüntüsünü döşeme (tile) katmanı olarak ekler."""
    tiles_url = _ee_tile_url(image, vis)
    folium.raster_layers.TileLayer(
        tiles=tiles_url,
        attr="Google Earth Engine",
        name=name,
        overlay=True,
        control=True,
        show=True,
        opacity=opacity,
    ).add_to(m)


def _add_continuous_legend(m: folium.Map, title: str, palette: Sequence[str], vmin: float, vmax: float) -> None:
    """Sürekli renk skalası için legend (branca) ekler."""
    cmap = LinearColormap(colors=list(palette), vmin=vmin, vmax=vmax)
    cmap.caption = title
    m.add_child(cmap)


def _add_severity_legend(m: folium.Map) -> None:
    """dNBR Severity için basit ayrık legend ekler."""
    labels = ["Unburned/Low", "Low", "Moderate-Low", "Moderate-High", "High"]
    colors = ["#1a9850", "#a6d96a", "#fee08b", "#f46d43", "#a50026"]
    html = [
        '<div style="position: fixed; bottom: 25px; left: 10px; z-index: 9999; \
         background: white; padding: 10px; border: 2px solid #bbb; \
         font-size: 12px; line-height: 14px;">',
        '<b>dNBR Severity</b><br/>',
    ]
    for c, lab in zip(colors, labels):
        html.append(f'<i style="background:{c};width:12px;height:12px;display:inline-block;margin-right:6px;"></i>{lab}<br/>')
    html.append('</div>')
    folium.map.Marker(
        location=[0, 0],  # görünmez; sadece HTML eklemek için
        icon=folium.DivIcon(html=''.join(html)),
    ).add_to(m)


def save_folium(image: ee.Image, aoi: ee.Geometry, vis: dict, name: str, out_html: str):
    """GEE görüntüsünü folium haritası olarak HTML dosyasına kaydeder.

    Best‑practice eklemeler:
    - EE tile URL elde etme: yeni/legacy API uyumlu.
    - Sürekli katmanlar için otomatik legend (NDVI/NBR/d*). Severity için ayrık legend.
      (Heuristik: adı 'Severity' içerirse ayrık legend; aksi halde palette+min/max ile sürekli.)
    """
    ensure_dir(os.path.dirname(out_html))
    m = folium.Map(location=_center_of(aoi), zoom_start=9, control_scale=True)
    _add_ee_tile(m, image, vis, name)
    folium.LayerControl().add_to(m)
    try:
        if "Severity" in name:
            _add_severity_legend(m)
        elif all(k in vis for k in ("palette", "min", "max")):
            _add_continuous_legend(m, name, vis["palette"], float(vis["min"]), float(vis["max"]))
    except Exception:
        # Legend eklenemese de haritayı kaydetmeye devam et
        pass
    m.save(out_html)


def reduce_mean(image: ee.Image, aoi: ee.Geometry, band: str, scale: int = 20) -> float:
    """AOI üzerinde belirtilen bandın ortalamasını döndürür.

    Args:
        image: ee.Image
        aoi: ee.Geometry çalışma alanı
        band: Hesaplanacak band adı
        scale: Metre cinsinden çözünürlük
    Returns:
        Ortalama değer (float) veya NaN
    """
    stats = image.select(band).reduceRegion(
        reducer=ee.Reducer.mean(), geometry=aoi, scale=scale, maxPixels=1e13
    )
    val = stats.get(band).getInfo()
    return float(val) if val is not None else float("nan")


def write_summary_csv(path: str, rows: Dict[str, float]):
    """Anahtar/değer özetlerini CSV dosyasına yazar.

    Args:
        path: Çıktı CSV yolu
        rows: {metrik: değer} sözlüğü
    """
    ensure_dir(os.path.dirname(path))
    with open(path, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["metric", "value"])
        for k, v in rows.items():
            w.writerow([k, v])
