import ee


def s2_sr_collection(aoi: ee.Geometry, start_date: str, end_date: str, cloud_pct: int = 20) -> ee.ImageCollection:
    col = (
        ee.ImageCollection("COPERNICUS/S2_SR_HARMONIZED")
        .filterBounds(aoi)
        .filterDate(start_date, end_date)
        .filter(ee.Filter.lt("CLOUDY_PIXEL_PERCENTAGE", cloud_pct))
    )
    return col


def mask_s2_clouds(image: ee.Image) -> ee.Image:
    qa = image.select("QA60")
    cloud_bit_mask = 1 << 10
    cirrus_bit_mask = 1 << 11
    mask = (
        qa.bitwiseAnd(cloud_bit_mask).eq(0)
        .And(qa.bitwiseAnd(cirrus_bit_mask).eq(0))
    )
    return image.updateMask(mask).copyProperties(image, image.propertyNames())


def composite_median(ic: ee.ImageCollection) -> ee.Image:
    return ic.map(mask_s2_clouds).median()


def prepare_composite(aoi: ee.Geometry, start_date: str, end_date: str, cloud_pct: int = 20) -> ee.Image:
    ic = s2_sr_collection(aoi, start_date, end_date, cloud_pct)
    comp = composite_median(ic)
    return comp

