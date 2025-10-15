# KarabukWildfire2025 - Jupyter Analiz Rehberi

Bu rehber, etkileşimli analiz akışını özetler. Artık tek defter kök dizinde: `analysis.ipynb`.

## Ortam ve Bağlantı
```bash
python -m venv .venv311
. .venv311/Scripts/activate   # Windows
pip install -r requirements.txt
earthengine authenticate
```

## Örnek Akış
1. AOI tanımla: `data/aoi.geojson` (Polygon veya MultiPolygon)
2. Tarih aralıkları: `pre/post` dönemleri belirle
3. NDVI/NBR hesapla; dNDVI/dNBR üret
4. Haritaları incele ve sonuçları yorumla

Aynı işlemleri CLI ile de yapabilirsiniz:
```bash
python -m src.cli \
  --pre-start 2025-07-10 --pre-end 2025-07-25 \
  --post-start 2025-07-26 --post-end 2025-08-10
```

