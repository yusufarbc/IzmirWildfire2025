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

