from __future__ import annotations

import ee


def compute_diffs(pre: ee.Image, post: ee.Image) -> dict:
    """Compute difference images for NDVI and NBR (post - pre)."""
    dndvi = post.select("NDVI").subtract(pre.select("NDVI")).rename("dNDVI")
    dnbr = post.select("NBR").subtract(pre.select("NBR")).rename("dNBR")
    return {"dNDVI": dndvi, "dNBR": dnbr}


def classify_dnbr(dnbr: ee.Image) -> ee.Image:
    """Classify dNBR into severity classes 0..4 (unburned→high).

    Thresholds (approx USGS):
      < 0.10: 0 (Unburned/Low)
      0.10–0.27: 1 (Low)
      0.27–0.44: 2 (Moderate-Low)
      0.44–0.66: 3 (Moderate-High)
      > 0.66: 4 (High)
    """
    t0 = 0.10
    t1 = 0.27
    t2 = 0.44
    t3 = 0.66

    c0 = dnbr.lt(t0)
    c1 = dnbr.gte(t0).And(dnbr.lt(t1))
    c2 = dnbr.gte(t1).And(dnbr.lt(t2))
    c3 = dnbr.gte(t2).And(dnbr.lt(t3))
    c4 = dnbr.gte(t3)

    classified = (
        c0.multiply(0)
        .add(c1.multiply(1))
        .add(c2.multiply(2))
        .add(c3.multiply(3))
        .add(c4.multiply(4))
        .rename("severity")
        .toUint8()
    )
    return classified

