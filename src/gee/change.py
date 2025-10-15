"""Değişim analizi (dNDVI/dNBR) ve dNBR şiddet sınıflandırması.

Hesap tanımları:
- dNDVI = post.NDVI - pre.NDVI (negatif → azalma)
- dNBR  = pre.NBR  - post.NBR  (pozitif → yanıklık artışı)
"""

from typing import Dict, Sequence

import ee


def compute_diffs(pre: ee.Image, post: ee.Image) -> Dict[str, ee.Image]:
    """dNDVI ve dNBR görüntülerini üretir.

    Args:
        pre: Ön dönem (NDVI/NBR eklenmiş) görüntü
        post: Sonraki dönem (NDVI/NBR eklenmiş) görüntü
    Returns:
        {"dNBR": ee.Image, "dNDVI": ee.Image}
    """
    dnbr = pre.select("NBR").subtract(post.select("NBR")).rename("dNBR")
    dndvi = post.select("NDVI").subtract(pre.select("NDVI")).rename("dNDVI")
    return {"dNBR": dnbr, "dNDVI": dndvi}


def default_dnbr_thresholds() -> Sequence[float]:
    """dNBR şiddeti için varsayılan eşikler (USGS’a yakın değerler)."""
    return (0.10, 0.27, 0.44, 0.66)


def classify_by_thresholds(image: ee.Image, thresholds: Sequence[float], name: str = "class") -> ee.Image:
    """Artan eşiklere göre 0..N sınıf üretir.

    Mantık: sum(image.gt(t) for t in thresholds)
    Örn. 4 eşik → 0..4 arası tamsayı sınıf kodu.
    """
    cls = ee.Image(0)
    for t in thresholds:
        cls = cls.add(image.gt(t))
    return cls.rename(name).toInt()


def classify_dnbr(dnbr: ee.Image, thresholds: Sequence[float] | None = None) -> ee.Image:
    """dNBR'ı yanık şiddeti sınıflarına ayırır (0–4).

    Eşikler: (0.10, 0.27, 0.44, 0.66) varsayılan. İhtiyaca göre verilebilir.
    """
    th = thresholds or default_dnbr_thresholds()
    return classify_by_thresholds(dnbr, th, name="dNBR_severity")


def severity_legend(thresholds: Sequence[float] | None = None) -> Dict:
    """Şiddet sınıfları için etiket/palet aralığı bilgisi döndürür.

    Returns:
        {
          'classes': [
            {'code': 0, 'label': 'Unburned/Low', 'min': None, 'max': 0.10, 'color': '#1a9850'}, ...
          ]
        }
    """
    th = list(thresholds or default_dnbr_thresholds())
    labels = ["Unburned/Low", "Low", "Moderate-Low", "Moderate-High", "High"]
    colors = ["#1a9850", "#a6d96a", "#fee08b", "#f46d43", "#a50026"]
    bounds = [None] + th + [None]
    classes = []
    for i in range(5):
        min_v = bounds[i]
        max_v = bounds[i + 1]
        classes.append({
            "code": i,
            "label": labels[i],
            "min": min_v,
            "max": max_v,
            "color": colors[i],
        })
    return {"classes": classes}
