# IzmirWildfire2025: Orman Yangını Etkisi Analizi

Sentinel‑2 uydu görüntüleri kullanılarak 2025 İzmir yangınının etkilerini (yanma şiddeti, hasar) değerlendirmeye yönelik Google Earth Engine (GEE) tabanlı analiz projesi. NDVI, NBR ve fark indeksleri (dNDVI, dNBR) üretilir; dNBR eşikleriyle şiddet sınıflandırması yapılır.

## Canlı Demo ve Sonuçlar

Interaktif haritalar ve çıktı listesi:

➡️ [GitHub Pages — Proje Sonuçları](https://yusufarbc.github.io/IzmirWildfire2025/)

Yerelde görüntüleme: Depo kökündeki `index.html` dosyasını tarayıcıda açın (tüm haritalar ve CSV/PNG bağlantıları `results/` altına işaret eder).

---

## Proje Yapısı

| Klasör/Dosya | Açıklama |
| :--- | :--- |
| `gee/` | Analiz kodları: `pipeline.py` (uçtan uca akış), `preprocess.py`, `indices.py`, `change.py` (dNBR sınıfları), `visualize.py`, `utils.py`, `aoi.py` ve `aoi.geojson`. |
| `results/` | Üretilen haritalar (HTML/PNG) ve özet istatistikler (`summary_stats.csv`, `severity_areas.csv`). |
| `paper/` | LaTeX raporu (`paper/main.tex`). |
| `analysis.ipynb` | Jupyter defteri; adım adım analiz ve görselleştirme. |
| `index.html` | Web sonuç sayfası (kart tabanlı, responsive). |
| `requirements.txt` | Gerekli Python kütüphaneleri. |

## Kurulum

Önkoşul: Google Earth Engine (GEE) API erişimi.

1) Sanal ortam ve bağımlılıklar

```bash
python -m venv .venv
# Linux/macOS
source .venv/bin/activate
# Windows
.\.venv\Scripts\activate

pip install -r requirements.txt
```

2) Earth Engine kimlik doğrulama

```bash
earthengine authenticate
```

## Çalıştırma

İki tip kullanım desteklenir: Jupyter defteri veya doğrudan Python çağrısı.

1) Jupyter Notebook (önerilen)

```bash
jupyter notebook analysis.ipynb
```

2) Python ile doğrudan çalıştırma (örnek)

```python
from gee.utils import ee_init
from gee.pipeline import run_pipeline

ee_init()  # gerekirse ee_init(project="<GCP_PROJECT_ID>")

outputs = run_pipeline(
    pre_start="2025-06-01", pre_end="2025-06-10",
    post_start="2025-08-20", post_end="2025-08-30",  # Sonrası için 20–30 Ağustos
    aoi_geojson="gee/aoi.geojson",
    out_dir="results",
    # Opsiyonel: AOI'ye göre dNBR eşiklerini özelleştir
    dnbr_thresholds=(0.08, 0.22, 0.40, 0.60),
    # Opsiyonel: Kıyı tamponu (metre) ve minimum yama alanı (hektar)
    coastline_buffer_m=100,
    min_patch_ha=0.5,
)

print(outputs)
```

Başarılı çalıştırma sonrası `results/` klasöründe interaktif haritalar (HTML) ve statik görseller (PNG) oluşur. Hızlı göz atmak için depo kökündeki `index.html` sayfasını açın.

Not: Bu çalışmada sonrası (post) dönem için 20–30 Ağustos aralığı baz alınmıştır. Farklı sahne/meteorolojik koşullarda bu aralığı yakın tarihlerle değiştirerek tekrar üretim yapabilirsiniz.

## Rapor (LaTeX)

`paper/main.tex` derlemek için:

```bash
pdflatex paper/main.tex
pdflatex paper/main.tex
```

Türkçe karakterler ve yer imleri için dosyada `babel` Türkçe ana dil ve `hyperref[unicode]` yapılandırması etkindir.

## Lisans

Bu proje MIT lisansı altındadır. Ayrıntılar için `LICENSE` dosyasına bakınız.

---

## Ek: NDVI/NBR ve Neden Bu Seçimler?

- NDVI = (NIR - Kirmizi) / (NIR + Kirmizi)
  - Yesil/saglikli ortu NIR'de yuksek, kirmizida dusuk yansitir; NDVI buyudukce yesillik/yoğunluk artar (0.2-0.5 orta; >0.5 yogun).
- NBR = (NIR - SWIR2) / (NIR + SWIR2)
  - Yanik yuzeylerde NIR azalir, SWIR artar; yangin oncesi NBR daha yuksek, sonrasi daha dusuktur.
- Farklar
  - dNDVI = Sonra - Once (negatifse yesil ortu kaybi)
  - dNBR  = Once - Sonra (pozitifse yaniklik artisi)

Neden boyle?

- Sentinel-2 ve median kompozit: 10-20 m cozunurluk; median tekil bulut/duman artiklarini bastirir.
- Maskeleme: QA60 + SCL (su) + NDWI/MNDWI; kyi icin 100 m tampon ile su/kiyi yalanci sinyalleri dislandi.
- Yanici yuzey filtresi: NDVIpre > 0.25 ile ciplak/yapay yuzeyler elenir; analiz yanabilir ortuye odaklanir.
- Fark tanimi: dNBR=pre-post (pozitif=yaniklik artisi), dNDVI=post-once (negatif=yesil kaybi) sezgiseldir.
- Donemler: Sonrasi 20-30 Agustos; Oncesi 1-10 Haziran.
- Esikler: USGS-benzeri sabit esikler kolay yorumlanir ve sahaya gore ayarlanabilir.
