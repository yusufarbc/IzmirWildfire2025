import ee


def add_ndvi(img: ee.Image) -> ee.Image:
    ndvi = img.normalizedDifference(["B8", "B4"]).rename("NDVI")
    return img.addBands(ndvi)


def add_nbr(img: ee.Image) -> ee.Image:
    nbr = img.normalizedDifference(["B8", "B12"]).rename("NBR")
    return img.addBands(nbr)


def with_indices(img: ee.Image) -> ee.Image:
    return add_nbr(add_ndvi(img))

