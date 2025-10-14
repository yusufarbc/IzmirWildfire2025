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

