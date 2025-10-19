from __future__ import annotations

import ee


def _mask_s2_sr(image: ee.Image) -> ee.Image:
    """Simple cloud/cirrus mask for Sentinel-2 SR (QA60 bits 10/11)."""
    qa = image.select("QA60")
    cloud_bit = 1 << 10
    cirrus_bit = 1 << 11
    mask = qa.bitwiseAnd(cloud_bit).eq(0).And(qa.bitwiseAnd(cirrus_bit).eq(0))
    return image.updateMask(mask)


def prepare_composite(aoi: ee.Geometry, start: str, end: str) -> ee.Image:
    """Prepare median Sentinel-2 SR composite clipped to AOI for date range."""
    col = (
        ee.ImageCollection("COPERNICUS/S2_SR_HARMONIZED")
        .filterDate(start, end)
        .filterBounds(aoi)
        .map(_mask_s2_sr)
    )
    img = col.median().clip(aoi)
    return img

