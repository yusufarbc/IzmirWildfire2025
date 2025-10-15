"""İndeks hesaplama yardımcıları (NDVI, NBR)

Bu modül, Sentinel‑2 bantlarından NDVI ve NBR indekslerini hesaplayıp
girdi görüntüsüne yeni bantlar olarak ekler.
"""

import ee


def add_ndvi(img: ee.Image) -> ee.Image:
    """NDVI bandını (B8,B4) hesaplar ve görüntüye ekler."""
    ndvi = img.normalizedDifference(["B8", "B4"]).rename("NDVI")
    return img.addBands(ndvi)


def add_nbr(img: ee.Image) -> ee.Image:
    """NBR bandını (B8,B12) hesaplar ve görüntüye ekler."""
    nbr = img.normalizedDifference(["B8", "B12"]).rename("NBR")
    return img.addBands(nbr)


def with_indices(img: ee.Image) -> ee.Image:
    """NDVI ve NBR bantlarını eklenmiş bir görüntü döndürür."""
    return add_nbr(add_ndvi(img))
