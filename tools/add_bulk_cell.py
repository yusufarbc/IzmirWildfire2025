import json
from pathlib import Path


CELL_MARKER = "# Toplu çıktı üret ve göster"


def build_cell_source() -> list[str]:
    header = CELL_MARKER + "\n"
    body = """
from IPython.display import HTML, Image, display, IFrame
import os, base64, pandas as pd

# Parametreler (tanımlı değilse varsayılana düş)
try:
    pre_start
    pre_end
    post_start
    post_end
    aoi_path
    out_dir
except NameError:
    pre_start, pre_end = '2025-07-10', '2025-07-25'
    post_start, post_end = '2025-07-26', '2025-08-10'
    aoi_path = 'src/aoi.geojson'
    out_dir = 'results'

from src.pipeline import run_pipeline
from src.gee.aoi import get_aoi
from src.gee.preprocess import prepare_composite
from src.gee.indices import with_indices
from src.gee.change import compute_diffs, classify_dnbr
from src.visualize import export_report_pngs, export_truecolor_pngs

# 1) Pipeline çalıştır (HTML haritalar + summary CSV)
outputs = run_pipeline(
    pre_start=pre_start, pre_end=pre_end,
    post_start=post_start, post_end=post_end,
    aoi_geojson=aoi_path, out_dir=out_dir,
)
display(HTML('<b>Üretilen dosyalar</b>'))
for key, val in list(outputs.items()):
    display(HTML(f"- {key}: <code>{val}</code>"))

# 2) PNG çıktıları üret (rapor ve doğal renk)
aoi = get_aoi(aoi_path)
pre = with_indices(prepare_composite(aoi, pre_start, pre_end))
post = with_indices(prepare_composite(aoi, post_start, post_end))
diffs = compute_diffs(pre, post)
severity = classify_dnbr(diffs['dNBR'])

pngs = export_report_pngs(pre=pre, post=post, diffs=diffs, severity=severity, aoi=aoi, out_dir=out_dir)
rgbs = export_truecolor_pngs(pre=pre, post=post, aoi=aoi, out_dir=out_dir)

order = [
  ('Pre RGB', rgbs.get('pre_rgb_png')),
  ('Post RGB', rgbs.get('post_rgb_png')),
  ('Pre NDVI', pngs.get('pre_ndvi_png')),
  ('Post NDVI', pngs.get('post_ndvi_png')),
  ('dNDVI', pngs.get('dndvi_png')),
  ('dNBR', pngs.get('dnbr_png')),
  ('Severity', pngs.get('severity_png')),
]

def show_image(path: str):
    try:
        display(Image(filename=path))
    except Exception:
        try:
            with open(path,'rb') as f:
                data = base64.b64encode(f.read()).decode('ascii')
            display(HTML(f"<img src='data:image/png;base64,{data}' style='max-width:100%;height:auto;'/>"))
        except Exception as e:
            display(HTML(f"<div style='color:#a00'>Unable to display {path}: {e}</div>"))

display(HTML('<hr/><b>PNG Görseller</b>'))
for title, p in order:
    if not p or not os.path.exists(p):
        continue
    display(HTML(f"<h4 style='margin:8px 0'>{title}</h4>"))
    show_image(p)

# 3) Özet istatistikleri göster
try:
    df = pd.read_csv(outputs['summary_csv'])
    display(HTML('<b>Özet İstatistikler</b>'))
    display(df)
except Exception:
    pass

# 4) İsteğe bağlı: HTML haritalar (IFrame + fallback render)
def show_html(path, height=600):
    try:
        display(IFrame(src=path, width='100%', height=height))
    except Exception:
        try:
            with open(path, 'r', encoding='utf-8') as f:
                html = f.read()
            display(HTML(html))
        except Exception as e:
            display(HTML(f"<div style='color:#a00'>Unable to display {path}: {e}</div>"))

display(HTML('<hr/><b>Haritalar (HTML)</b>'))
for key in ['pre_ndvi_map','post_ndvi_map','pre_nbr_map','post_nbr_map','dnbr_map','severity_map']:
    p = outputs.get(key)
    if p and os.path.exists(p):
        show_html(p, height=600 if 'nbr' in key else 480)
"""
    src = header + body.lstrip("\n")
    return [line + ("\n" if not line.endswith("\n") else "") for line in src.splitlines()]


def main():
    p = Path('analysis.ipynb')
    nb = json.loads(p.read_text(encoding='utf-8'))
    # Check if the cell already exists
    for cell in nb.get('cells', []):
        if cell.get('cell_type') == 'code' and any(CELL_MARKER in (s or '') for s in cell.get('source', [])):
            print('Bulk cell already exists; skipping')
            break
    else:
        cell = {
            'cell_type': 'code',
            'metadata': {},
            'source': build_cell_source(),
            'outputs': [],
            'execution_count': None,
        }
        nb.setdefault('cells', []).append(cell)
        p.write_text(json.dumps(nb, ensure_ascii=False, indent=1), encoding='utf-8')
        print('Bulk cell added')


if __name__ == '__main__':
    main()
