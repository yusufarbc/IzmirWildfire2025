# KarabukWildfire2025

Karabük 2025 orman yangını etkisinin Sentinel-2 verileri ile NDVI ve NBR indeksleri üzerinden analiz edilmesi için Python + Google Earth Engine (GEE) tabanlı bir çalışma alanı.

**Proje Amacı**
- 10 Temmuz – 10 Ağustos 2025 aralığında yangın öncesi/sonrası bitki örtüsü değişimini sayısal ve mekansal olarak değerlendirmek (NDVI, NBR, dNDVI, dNBR).

**Teknik Bileşenler**
- Veri: Sentinel-2 Level-2A, 10 m
- Platform: Google Earth Engine (GEE) Python API
- Alan: Karabük ve çevresi (yangın bölgesi)
- Filtreler: `CLOUDY_PIXEL_PERCENTAGE < 20`, bulut maskeleme (QA60)

**Analiz Aşamaları**
- Ön işleme: tarih/alan/bulut filtresi, median kompozit
- İndeksler: NDVI (B8, B4), NBR (B8, B12)
- Farklar: dNDVI, dNBR; sınıflandırma ile hasar şiddeti
- Görselleştirme: folium tabanlı haritalar (HTML), özet istatistikler (CSV)

**Dosya Yapısı**
```
KarabukWildfire2025/
├── data/                  # AOI/yardımcı veriler (örn. aoi.geojson)
├── notebooks/             # Jupyter analiz rehberi/defterleri
├── src/                   # Python kodları (GEE pipeline)
├── results/               # Haritalar ve çıktı dosyaları
├── docs/                  # Raporlar ve ek doküman
├── README.md              # Proje tanıtımı ve kullanım
├── requirements.txt       # Kütüphaneler
└── LICENSE                # Lisans (MIT varsayılan)
```

**Kurulum**
- Python 3.10+ önerilir.
- Sanal ortam:
  - venv: `python -m venv .venv && . .venv/Scripts/activate` (Windows) veya `. .venv/bin/activate`
  - kurulum: `pip install -r requirements.txt`
- GEE yetkilendirme:
  - `earthengine authenticate` komutu ile oturum açın (tarayıcı ile). Alternatif olarak servis hesabı kullanabilirsiniz (bkz. `src/utils.py`).

**Kullanım (CLI)**
```
python -m src.cli \
  --pre-start 2025-07-10 --pre-end 2025-07-25 \
  --post-start 2025-07-26 --post-end 2025-08-10
```
- AOI varsayılanı Karabük çevresi için yaklaşık bir bbox’tır. Kendi alanınızı `data/aoi.geojson` ile sağlayabilirsiniz.
- Çıktılar `results/` klasörüne HTML haritalar ve CSV özet olarak yazılır.

**Notlar**
- dNBR şiddet sınıfları literatürde farklı eşiklerle kullanılabilir; `src/gee/change.py` içinde özelleştirilebilir.
- Tarih aralıklarını saha bilgisini yansıtacak şekilde güncellemeniz önerilir.

**Lisans**
- MIT (bkz. `LICENSE`).

