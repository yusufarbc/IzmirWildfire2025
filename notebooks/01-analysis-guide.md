# KarabukWildfire2025 – Jupyter Analiz Rehberi

Bu klasör, etkileşimli analiz için Jupyter defterlerini barındırır. Hızlı başlangıç:

## Ortam ve Bağlantı
```bash
python -m venv .venv
. .venv/Scripts/activate   # Windows
pip install -r requirements.txt
earthengine authenticate
```

## Örnek Akış
1. AOI tanımla: `data/aoi.geojson` (Polygon veya MultiPolygon)
2. Tarih aralıkları: `pre/post` dönemleri belirle
3. NDVI/NBR hesapla; dNDVI/dNBR üret
4. Haritaları incele ve sonuçları yorumla

CLI ile aynı işlemleri notebook içinde modülleri kullanarak çalıştırabilirsiniz:
```python
from src.utils import ee_init
from src.gee.aoi import get_aoi
from src.gee.preprocess import prepare_composite
from src.gee.indices import with_indices
from src.gee.change import compute_diffs, classify_dnbr

ee_init()
aoi = get_aoi("data/aoi.geojson")
pre = with_indices(prepare_composite(aoi, '2025-07-10', '2025-07-25'))
post = with_indices(prepare_composite(aoi, '2025-07-26', '2025-08-10'))
diffs = compute_diffs(pre, post)
sev = classify_dnbr(diffs['dNBR'])
```

