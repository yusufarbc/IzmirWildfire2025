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
├── src/                   # Python kodları (GEE pipeline)
├── results/               # Haritalar ve çıktı dosyaları
├── docs/                  # Raporlar ve ek doküman
├── analysis.ipynb         # Tek Jupyter defteri (kök dizinde)
├── README.md              # Proje tanıtımı ve kullanım
├── requirements.txt       # Kütüphaneler
├── LICENSE                # Lisans (MIT varsayılan)
```

**Kurulum**
- Python 3.10+ önerilir (3.11 uyumlu).
- Sanal ortam (Windows):
  - `python -m venv .venv311 && . .venv311/Scripts/activate`
  - `pip install -r requirements.txt`
- GEE yetkilendirme:
  - `earthengine authenticate` komutu ile oturum açın (tarayıcı ile). Alternatif olarak servis hesabı kullanabilirsiniz (bkz. `src/utils.py`).

**Kullanım (Notebook)**
- `analysis.ipynb` defterini açın.
- Gerekirse tarih aralıklarını ve `data/aoi.geojson` yolunu güncelleyin.
- Hücreleri sırayla çalıştırın; çıktılar `results/` klasörüne yazılır ve defter içinde gömülü önizleme bulunur.

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

# KarabukWildfire2025 – Teknik Planlama Özeti

## Amaç
Karabük 2025 yangınının bitki örtüsüne etkisini Sentinel-2 ile analiz etmek; yangın öncesi/sonrası NDVI ve NBR farklarından dNDVI ve dNBR üretip hasar şiddetini sınıflandırmak.

## Bileşenler
- Veri/Platform: Sentinel-2 L2A, GEE Python API
- Aralık: 10 Temmuz – 10 Ağustos 2025 (özelleştirilebilir)
- Alan: Karabük ve çevresi (AOI: `data/aoi.geojson` veya varsayılan bbox)

## İş Akışı
1) Ön İşleme
   - Tarih/alan filtresi, `CLOUDY_PIXEL_PERCENTAGE < 20`
   - QA60 bulut/cirrus maskesi, median kompozit
2) İndeksler
   - NDVI: (B8 - B4) / (B8 + B4)
   - NBR:  (B8 - B12) / (B8 + B12)
3) Fark Analizi
   - dNDVI = NDVI_post - NDVI_pre
   - dNBR  = NBR_pre - NBR_post
4) Sınıflandırma (dNBR)
   - 0: Unburned/Low, 1: Low, 2: Mod-Low, 3: Mod-High, 4: High
   - Eşikler özelleştirilebilir (`src/gee/change.py`)
5) Görselleştirme/Çıktılar
   - Folium HTML haritaları: pre/post NDVI/NBR, dNDVI, dNBR, şiddet
   - Özet istatistikler (CSV): ortalama NDVI/dNDVI/dNBR

## Çalıştırma
```bash
python -m src.cli \
  --pre-start 2025-07-10 --pre-end 2025-07-25 \
  --post-start 2025-07-26 --post-end 2025-08-10
```

## Notlar
- Tarih aralıklarını saha bilgisi ile kesinleştirin.
- AOI için hassas sınırlar kullanılmalıdır (GeoJSON).
- Harita paletleri ve sınıflar rapor ihtiyaçlarına göre değiştirilebilir.

# KarabukWildfire2025 – Yapılanlar Özeti

- Proje yapısı oluşturuldu: `data/`, `notebooks/`, `src/`, `results/`, `docs/`.
- README güncellendi; teknik plan `docs/plan.md`, Jupyter rehberi `notebooks/01-analysis-guide.md` eklendi.
- GEE analiz modülleri yazıldı:
  - `src/utils.py`: Earth Engine başlatma (`ee_init`), yardımcılar.
  - `src/gee/aoi.py`: AOI GeoJSON yükleme, yoksa Karabük bbox.
  - `src/gee/preprocess.py`: Sentinel‑2 L2A filtreleme, QA60 bulut maskesi, median kompozit.
  - `src/gee/indices.py`: NDVI, NBR bantları.
  - `src/gee/change.py`: dNDVI, dNBR ve dNBR şiddet sınıflaması.
  - `src/visualize.py`: Folium haritaları ve özet istatistik üretimi.
  - `src/pipeline.py`: uçtan uca akış.
  - `src/cli.py`: komut satırı arayüzü.
- `requirements.txt` ve `LICENSE` eklendi; sanal ortamda bağımlılıklar kuruldu.

## Çalıştırma
- GEE yetkilendirme: `earthengine authenticate`
- Örnek: `python -m src.cli --pre-start 2025-07-10 --pre-end 2025-07-25 --post-start 2025-07-26 --post-end 2025-08-10`
- Çıktılar: `results/` altında HTML haritalar ve `summary_stats.csv`.

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

