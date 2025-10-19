# izmirwildfire2025: Orman Yangını Etkisi Analizi

Sentinel-2 uydu görüntüleri kullanılarak 2025 İzmir yangınının etkilerini (yanma şiddeti, hasar) değerlendirmeye yönelik Google Earth Engine (GEE) tabanlı analiz projesi. Normalized Difference Vegetation Index (NDVI), Normalized Burn Ratio (NBR) ve bu indekslerin değişimleri (dNDVI, dNBR) hesaplanmıştır.

## 🔗 Canlı Demo ve Sonuçlar

Analiz çıktılarına ve interaktif haritalara aşağıdaki linkten ulaşabilirsiniz:

➡️ **[PROJE SONUÇLARI (GITHUB PAGES)](https://yusufarbc.github.io/izmirwildfire2025/)**
➡️ **[ANA GİTHUB DEPOSU](https://github.com/yusufarbc/izmirwildfire2025)**

-----

## 🚀 Proje İçeriği ve Yapısı

| Klasör/Dosya | Açıklama |
| :--- | :--- |
| `src/` | **Analiz Kodları:** GEE tabanlı analiz hattı (`pipeline.py`), CLI arayüzü (`cli.py`), yardımcı fonksiyonlar ve görselleştirme araçları. (AOI dosyası (`aoi.geojson`) buradadır.) |
| `paper/` | **Çalışma Raporu:** Projenin metodolojisini, sonuçlarını ve değerlendirmesini içeren bilimsel rapor (LaTeX formatında). |
| `results/` | **Çıktılar:** Üretilen haritalar, özet istatistikler ve diğer analiz sonuçları. |
| `analysis.ipynb` | **Ana Çalışma Dosyası:** Proje sürecinin Jupyter Notebook üzerinden interaktif olarak yürütüldüğü dosya. |
| `requirements.txt` | Proje için gerekli Python kütüphaneleri. |

## ⚙️ Kurulum

Proje, Google Earth Engine (GEE) API'sine erişim gerektirir.

### 1\. Ortamın Hazırlanması

Proje bağımlılıklarını izole etmek için bir sanal ortam oluşturun ve gerekli kütüphaneleri kurun (Jupyter dahil):

```bash
# Sanal ortam oluşturma
python -m venv .venv

# Sanal ortamı etkinleştirme
. .venv/bin/activate  # Linux/macOS
# .venv\Scripts\activate  # Windows

# Gerekli Python kütüphanelerini kurma
pip install -r requirements.txt
```

### 2\. Earth Engine Kimlik Doğrulaması

GEE API'sine erişim için kimlik doğrulamanızı yapın:

```bash
earthengine authenticate
```

## 🏃 Çalıştırma

Proje, analiz adımlarını interaktif olarak takip etme imkanı sunan Jupyter Notebook veya otomasyon amaçlı Komut Satırı Arayüzü (CLI) ile çalıştırılabilir.

### 1\. Jupyter Notebook ile Çalıştırma (Önerilen)

Tüm analiz süreci, görselleştirmelerle birlikte **`analysis.ipynb`** dosyasında adım adım yürütülmüştür. Notebook'u başlatmak için:

```bash
# Sanal ortamı etkinleştirdiğinizden emin olun
jupyter notebook analysis.ipynb
```

### 2\. Komut Satırı Arayüzü (CLI) ile Çalıştırma (Alternatif)

Analizi doğrudan CLI üzerinden çalıştırmak için **(AOI yolu güncellenmiştir)**:

```bash
python -m src.cli \
  --pre-start 2025-08-15 --pre-end 2025-08-31 \
  --post-start 2025-09-01 --post-end 2025-09-20 \
  --aoi src/aoi.geojson \
  --out results
```

| Argüman | Açıklama |
| :--- | :--- |
| `--pre-start`, `--pre-end` | Yangın öncesi dönemin başlangıç ve bitiş tarihleri (YYYY-MM-DD). |
| `--post-start`, `--post-end` | Yangın sonrası dönemin başlangıç ve bitiş tarihleri (YYYY-MM-DD). |
| `--aoi` | Analiz Alanı sınırlarını içeren GeoJSON dosyasının yolu. (`src/aoi.geojson`) |
| `--out` | Üretilen çıktıların (`.html` haritalar ve `.csv` istatistikler) kaydedileceği klasör. |

### Örnek Çıktılar

Başarılı bir çalıştırmanın ardından `results/` klasöründe HTML haritalar (pre/post RGB, NDVI, NBR; dNDVI, dNBR; severity) ve `results/summary_stats.csv` dosyaları oluşur. Bu çıktılara yerel olarak erişmek için `results/index.html` dosyasını kullanabilirsiniz.

## 📝 Lisans

Bu proje [Lisans Türü - Örn: MIT] lisansı altındadır. Detaylar için `LICENSE` dosyasına bakınız.



