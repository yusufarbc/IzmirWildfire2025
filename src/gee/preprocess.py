"""Sentinel‑2 ön işleme yardımcıları

Bu modül, Sentinel‑2 L2A koleksiyonunu tarih/alan/bulut ile filtreler,
QA60 bandına göre bulut/ciros maskesi uygular ve median kompozit üretir.

Fonksiyonlar:
- s2_sr_collection: Koleksiyonu alan/tarih/bulut eşiği ile filtreler
- mask_s2_clouds: QA60 üzerinden bulut/ciros maskesi uygular
- composite_median: Maske sonrası median kompozit hesaplar
- prepare_composite: Tüm adımları birleştiren yardımcı
"""

import ee


def s2_sr_collection(aoi: ee.Geometry, start_date: str, end_date: str, cloud_pct: int = 20) -> ee.ImageCollection:
    """Sentinel‑2 L2A koleksiyonunu filtreler.

    Args:
        aoi: ee.Geometry çalışma alanı
        start_date: Başlangıç tarihi (YYYY-MM-DD)
        end_date: Bitiş tarihi (YYYY-MM-DD)
        cloud_pct: Maks. bulut yüzdesi filtresi
    Returns:
        ee.ImageCollection
    """
    col = (
        ee.ImageCollection("COPERNICUS/S2_SR_HARMONIZED")
        .filterBounds(aoi)
        .filterDate(start_date, end_date)
        .filter(ee.Filter.lt("CLOUDY_PIXEL_PERCENTAGE", cloud_pct))
    )
    return col


def mask_s2_clouds(image: ee.Image) -> ee.Image:
    """QA60 bandından bulut ve sirrus bitlerini maskeleyerek kaliteyi artırır."""
    qa = image.select("QA60")
    cloud_bit_mask = 1 << 10
    cirrus_bit_mask = 1 << 11
    mask = (
        qa.bitwiseAnd(cloud_bit_mask).eq(0)
        .And(qa.bitwiseAnd(cirrus_bit_mask).eq(0))
    )
    return image.updateMask(mask).copyProperties(image, image.propertyNames())


def composite_median(ic: ee.ImageCollection) -> ee.Image:
    """Maske uygulanmış koleksiyondan median kompozit üretir."""
    return ic.map(mask_s2_clouds).median()


def prepare_composite(aoi: ee.Geometry, start_date: str, end_date: str, cloud_pct: int = 20) -> ee.Image:
    """Filtrele → Maskele → Median adımlarını tek çağrıda uygular."""
    ic = s2_sr_collection(aoi, start_date, end_date, cloud_pct)
    comp = composite_median(ic)
    return comp
