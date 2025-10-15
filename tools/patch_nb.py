import json
from pathlib import Path

def main():
    p = Path('analysis.ipynb')
    nb = json.loads(p.read_text(encoding='utf-8'))
    changed = False

    for cell in nb.get('cells', []):
        if cell.get('cell_type') != 'code':
            continue
        src = ''.join(cell.get('source', []))
        if 'Haritaları defter içinde görüntüle' in src:
            new = """# Haritaları defter içinde görüntüle (opsiyonel)
from IPython.display import HTML

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

show_html(outputs['pre_ndvi_map'], height=480)
show_html(outputs['post_ndvi_map'], height=480)
show_html(outputs['pre_nbr_map'], height=480)
show_html(outputs['post_nbr_map'], height=480)
show_html(outputs['dnbr_map'], height=600)
show_html(outputs['severity_map'], height=600)
"""
            cell['source'] = [line + ("\n" if not line.endswith("\n") else '') for line in new.splitlines()]
            changed = True
        if "Rapor PNG'leri (analiz katmanları + doğal renk)" in src:
            new = """# Rapor PNG'leri (analiz katmanları + doğal renk)
from src.gee.aoi import get_aoi
from src.gee.preprocess import prepare_composite
from src.gee.indices import with_indices
from src.gee.change import compute_diffs, classify_dnbr
from src.visualize import export_report_pngs, export_truecolor_pngs
from IPython.display import Image, HTML, display
import os, base64

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
  ('dNBR', pngs.get('dnbr_png')),
  ('Severity', pngs.get('severity_png')),
]

def show_image(path):
    try:
        display(Image(filename=path))
    except Exception:
        try:
            with open(path,'rb') as f:
                data = base64.b64encode(f.read()).decode('ascii')
            display(HTML(f"<img src='data:image/png;base64,{data}' style='max-width:100%;height:auto;'/>"))
        except Exception as e:
            display(HTML(f"<div style='color:#a00'>Unable to display {path}: {e}</div>"))

for title, p in order:
    if not p or not os.path.exists(p):
        continue
    display(HTML(f"<h4 style='margin:8px 0'>{title}</h4>"))
    show_image(p)
"""
            cell['source'] = [line + ("\n" if not line.endswith("\n") else '') for line in new.splitlines()]
            changed = True

    if changed:
        p.write_text(json.dumps(nb, ensure_ascii=False, indent=1), encoding='utf-8')
        print('Notebook updated')
    else:
        print('No changes applied')

if __name__ == '__main__':
    main()

