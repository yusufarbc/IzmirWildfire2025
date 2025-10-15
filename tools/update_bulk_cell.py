import json
from pathlib import Path

MARK = "# Toplu çıktı üret ve göster"

EXTRA = """
# --- Yanmış alan (EE pixelArea) metrikleri ---
import pandas as pd
try:
    areas_df = pd.read_csv(outs['severity_areas_csv'])
    vals = dict(zip(areas_df['metric'], areas_df['value']))
    burned_ha = vals.get('burned_area_ha')
    aoi_ha = vals.get('aoi_area_ha')
    pct = 100.0 * burned_ha / aoi_ha if burned_ha and aoi_ha else None
    display(HTML(f"<b>Yanmış alan (EE):</b> ~{burned_ha:,.1f} ha ({pct:.2f}%)"))
except Exception as e:
    display(HTML(f"<div style='color:#a00'>Yanmış alan okunamadı: {e}</div>"))
"""


def main():
    p = Path('analysis.ipynb')
    nb = json.loads(p.read_text(encoding='utf-8'))
    changed = False
    for cell in nb.get('cells', []):
        if cell.get('cell_type') != 'code':
            continue
        src = ''.join(cell.get('source', []))
        if MARK in src and 'severity_areas_csv' not in src:
            new_src = src.rstrip() + '\n' + EXTRA
            cell['source'] = [line + ('\n' if not line.endswith('\n') else '') for line in new_src.splitlines()]
            changed = True
            break
    if changed:
        p.write_text(json.dumps(nb, ensure_ascii=False, indent=1), encoding='utf-8')
        print('Bulk cell updated with severity areas display')
    else:
        print('No changes applied')


if __name__ == '__main__':
    main()

