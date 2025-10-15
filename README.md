# KarabukWildfire2025

Uzaktan algılama ile orman yangını etkisi analizi (Sentinel-2, NDVI/NBR, dNDVI/dNBR).

## İçerik
- `src/`: GEE tabanlı analiz kodları (pipeline, görselleştirme, yardımcılar)
- `paper/`: Çalışma raporu (LaTeX)
- `results/`: Üretilen harita/istatistik çıktıları (git tarafından yok sayılır)

## Kurulum
```bash
python -m venv .venv
. .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

Earth Engine kimlik doğrulaması:
```bash
earthengine authenticate
```

Opsiyonel ortam değişkenleri (servis hesabı kullanacaksanız):
- `EE_SERVICE_ACCOUNT`, `EE_PRIVATE_KEY_FILE`
- `EE_PROJECT` (veya `EARTHENGINE_PROJECT`)

## Çalıştırma (CLI)
```bash
python -m src.cli \
  --pre-start 2025-07-10 --pre-end 2025-07-25 \
  --post-start 2025-07-26 --post-end 2025-08-10 \
  --aoi data/aoi.geojson \
  --out results
```
Üretilenler: HTML haritalar (pre/post RGB, NDVI, NBR; dNDVI, dNBR; severity) ve `results/summary_stats.csv`.

## Analiz Hattı
`src/pipeline.py` içindeki `run_pipeline` fonksiyonu şu adımları yürütür:
1. EE başlatma ve AOI yükleme
2. Öncesi/sonrası median kompozit üretimi (QA60 maskeleme)
3. NDVI/NBR ekleme ve dNDVI/dNBR hesaplama
4. dNBR şiddet sınıflandırması (0–4)
5. Haritaların ve özet istatistiklerin kaydı

Detaylar raporda (paper/main.tex) “Yöntem → Analiz Hattı (pipeline.py)” bölümünde açıklanmıştır.
