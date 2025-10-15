import ee


def compute_diffs(pre: ee.Image, post: ee.Image) -> dict:
    """Compute dNDVI and dNBR images.

    dNDVI = post - pre (negative values → azalış)
    dNBR  = pre - post (pozitif → yanıklık artışı)
    """
    dnbr = pre.select("NBR").subtract(post.select("NBR")).rename("dNBR")
    dndvi = post.select("NDVI").subtract(pre.select("NDVI")).rename("dNDVI")
    return {"dNBR": dnbr, "dNDVI": dndvi}


def classify_dnbr(dnbr: ee.Image) -> ee.Image:
    """Classify dNBR into burn severity classes.

    Classes (code → description):
      0 → Unburned/Low
      1 → Low
      2 → Moderate-Low
      3 → Moderate-High
      4 → High
    Thresholds are indicative and can be adjusted.
    """
    sev = ee.Image(0)
    sev = sev.where(dnbr.gt(0.10).And(dnbr.lte(0.27)), 1)
    sev = sev.where(dnbr.gt(0.27).And(dnbr.lte(0.44)), 2)
    sev = sev.where(dnbr.gt(0.44).And(dnbr.lte(0.66)), 3)
    sev = sev.where(dnbr.gt(0.66), 4)
    return sev.rename("dNBR_severity").toInt()

