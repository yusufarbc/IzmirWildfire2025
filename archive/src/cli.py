import argparse

from src.pipeline import run_pipeline


def parse_args():
    p = argparse.ArgumentParser(
        description="KarabukWildfire2025 – Sentinel-2 NDVI/NBR dNDVI/dNBR analizi"
    )
    p.add_argument("--pre-start", required=True, help="Öncesi başlangıç tarihi (YYYY-MM-DD)")
    p.add_argument("--pre-end", required=True, help="Öncesi bitiş tarihi (YYYY-MM-DD)")
    p.add_argument("--post-start", required=True, help="Sonrası başlangıç tarihi (YYYY-MM-DD)")
    p.add_argument("--post-end", required=True, help="Sonrası bitiş tarihi (YYYY-MM-DD)")
    p.add_argument("--aoi", default="data/aoi.geojson", help="AOI GeoJSON dosyası (opsiyonel)")
    p.add_argument("--out", default="results", help="Çıktı klasörü")
    return p.parse_args()


def main():
    args = parse_args()
    outs = run_pipeline(
        pre_start=args.pre_start,
        pre_end=args.pre_end,
        post_start=args.post_start,
        post_end=args.post_end,
        aoi_geojson=args.aoi,
        out_dir=args.out,
    )
    print("Üretilen çıktılar:")
    for k, v in outs.items():
        print(f"- {k}: {v}")


if __name__ == "__main__":
    main()

