# KarabukWildfire2025: Orman Yangını Etkisi Analizi

Sentinel-2 uydu görüntüleri kullanılarak 2025 Karabük yangınının etkilerini (yanma şiddeti, hasar) değerlendirmeye yönelik Google Earth Engine (GEE) tabanlı analiz projesi. Normalized Difference Vegetation Index (NDVI), Normalized Burn Ratio (NBR) ve bu indekslerin değişimleri (dNDVI, dNBR) hesaplanmıştır.

## 🚀 Proje İçeriği ve Yapısı

| Klasör/Dosya | Açıklama |
| :--- | :--- |
| `src/` | **Analiz Kodları:** GEE tabanlı analiz hattı (`pipeline.py`), CLI arayüzü (`cli.py`), yardımcı fonksiyonlar ve görselleştirme araçları. |
| `paper/` | **Çalışma Raporu:** Projenin metodolojisini, sonuçlarını ve değerlendirmesini içeren bilimsel rapor (LaTeX formatında). |
| `results/` | **Çıktılar:** Üretilen haritalar, özet istatistikler ve diğer analiz sonuçları. **(**`*.gitignore`\*\* ile git takibinden çıkarılmıştır.)\*\* |
| `data/` | **Girdiler:** Analiz Alanı (AOI) GeoJSON dosyası (`aoi.geojson`). |
| `requirements.txt` | Proje için gerekli Python kütüphaneleri. |

## ⚙️ Kurulum

Proje, Google Earth Engine (GEE) API'sine erişim gerektirir.

### 1\. Ortamın Hazırlanması

Proje bağımlılıklarını izole etmek için bir sanal ortam oluşturun ve gerekli kütüphaneleri kurun:

```bash
# Sanal ortam oluşturma
python -m venv .venv

# Sanal ortamı etkinleştirme
. .venv/bin/activate  # Linux/macOS
# .venv\Scripts\activate  # Windows

# Gerekli Python kütüphanelerini kurma
pip install -r requirements.txt
```

### 2\. Earth Engine Kimlik Doğrulaması

GEE API'sine erişim için kimlik doğrulamanızı yapın:

```bash
earthengine authenticate
```

### 3\. Opsiyonel Ortam Değişkenleri (Servis Hesabı Kullanımı)

Kurumsal veya otomasyon amaçlı servis hesabı kullanacaksanız, gerekli ortam değişkenlerini ayarlayın:

| Değişken | Açıklama |
| :--- | :--- |
| `EE_SERVICE_ACCOUNT` | GEE Servis Hesabı E-posta Adresi. |
| `EE_PRIVATE_KEY_FILE` | Servis hesabı özel anahtar dosyası yolu (`.json`). |
| `EE_PROJECT` veya `EARTHENGINE_PROJECT` | GEE Cloud Proje Kimliği (zorunlu olabilir). |

## 🔬 Analiz Hattı

`src/pipeline.py` içerisindeki ana fonksiyon `run_pipeline`, yangın sonrası etki analizi için aşağıdaki adımları sırasıyla yürütür:

1.  **Başlatma:** GEE oturumunu başlatır ve Analiz Alanını (AOI) yükler.
2.  **Görüntü Kompozitleri:** Yangın **öncesi** ve **sonrası** dönemler için bulut/gölge maskeleme (QA60) uygulanmış Sentinel-2 median kompozitleri üretir.
3.  **İndeks Hesaplamaları:** Üretilen kompozitler üzerinden **NDVI** ve **NBR** haritalarını hesaplar.
4.  **Değişim Hesaplamaları:** Yangın etkisini ölçmek için **dNDVI** ve **dNBR** (Normalized Burn Ratio Değişimi) haritalarını hesaplar.
5.  **Şiddet Sınıflandırması:** dNBR değerlerine göre yangın şiddeti sınıflandırması yapar (standart 0 - 4 arası sınıflar).
6.  **Çıktı Kaydı:** Üretilen haritaları (HTML formatında) ve **özet istatistikleri** (`results/summary_stats.csv`) kaydeder.

> ℹ️ **Detaylı Bilgi:** Bu süreç, `paper/main.tex` raporunun "Yöntem → Analiz Hattı (`pipeline.py`)" bölümünde detaylı olarak açıklanmıştır.

## 🏃 Çalıştırma (Komut Satırı Arayüzü)

Analiz, CLI üzerinden belirlenen tarihler ve AOI ile başlatılır. Aşağıdaki örnek, Karabük yangını varsayılan tarihlerini kullanır:

```bash
python -m src.cli \
  --pre-start 2025-07-10 --pre-end 2025-07-25 \
  --post-start 2025-07-26 --post-end 2025-08-10 \
  --aoi data/aoi.geojson \
  --out results
```

| Argüman | Açıklama |
| :--- | :--- |
| `--pre-start`, `--pre-end` | Yangın öncesi dönemin başlangıç ve bitiş tarihleri (YYYY-MM-DD). |
| `--post-start`, `--post-end` | Yangın sonrası dönemin başlangıç ve bitiş tarihleri (YYYY-MM-DD). |
| `--aoi` | Analiz Alanı sınırlarını içeren GeoJSON dosyasının yolu. |
| `--out` | Üretilen çıktıların (`.html` haritalar ve `.csv` istatistikler) kaydedileceği klasör. |

### Örnek Çıktılar

Başarılı bir çalıştırmanın ardından `results/` klasöründe aşağıdaki dosyalar oluşacaktır:

  - `pre_rgb.html`, `post_rgb.html` (Öncesi/Sonrası Gerçek Renkli Görüntüler)
  - `ndvi.html`, `nbr.html`
  - `d_ndvi.html`, `d_nbr.html`
  - `severity_map.html` (Yanma Şiddeti Sınıflandırması)
  - `summary_stats.csv` (Yanma sınıfı alanları ve istatistikler)

## 📝 Lisans

Bu proje MIT lisansı altındadır. Detaylar için `LICENSE` dosyasına bakınız.
