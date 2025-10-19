from __future__ import annotations

import ee


def with_indices(image: ee.Image) -> ee.Image:
    """Return image with NDVI and NBR bands added.

    Uses bands: B8 (NIR), B4 (Red), B12 (SWIR2)
    """
    nir = image.select("B8")
    red = image.select("B4")
    swir2 = image.select("B12")
    ndvi = nir.subtract(red).divide(nir.add(red)).rename("NDVI")
    nbr = nir.subtract(swir2).divide(nir.add(swir2)).rename("NBR")
    return image.addBands([ndvi, nbr])

