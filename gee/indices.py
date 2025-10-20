from __future__ import annotations

import ee


def with_indices(image: ee.Image) -> ee.Image:
    """Return image with NDVI, NBR and water indices (NDWI/MNDWI) added.

    Uses bands: B8 (NIR), B4 (Red), B12 (SWIR2), B3 (Green), B11 (SWIR1)
    """
    nir = image.select("B8")
    red = image.select("B4")
    green = image.select("B3")
    swir1 = image.select("B11")
    swir2 = image.select("B12")

    ndvi = nir.subtract(red).divide(nir.add(red)).rename("NDVI")
    nbr = nir.subtract(swir2).divide(nir.add(swir2)).rename("NBR")

    # Water indices
    ndwi = green.subtract(nir).divide(green.add(nir)).rename("NDWI")
    mndwi = green.subtract(swir1).divide(green.add(swir1)).rename("MNDWI")

    return image.addBands([ndvi, nbr, ndwi, mndwi])
