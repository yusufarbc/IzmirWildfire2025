import json
from pathlib import Path


STEP0_MARK = "## 0. Önkoşullar"
STEP1_MARK = "## 1. Earth Engine Kimlik Doğrulama"


STEP0_MD = (
    "## 0. Önkoşullar\n\n"
    "Bu defteri çalıştırmadan önce aşağıdaki kurulum adımlarını uygulayın.\n\n"
    "- Python 3.10+ önerilir ve izole ortam kullanın (venv).\n"
    "- Bağımlılıkları `requirements.txt` üzerinden kurun.\n\n"
    "Örnek komutlar:\n\n"
    "```bash\n"
    "python -m venv .venv\n"
    ". .venv/bin/activate  # Windows: .venv\\\\Scripts\\\\activate\n"
    "pip install -r requirements.txt\n"
    "```\n\n"
    "Not: Bağımlılık çatışmalarını önlemek için her projede ayrı bir sanal ortam önerilir.\n"
)

STEP1_MD = (
    "## 1. Earth Engine Kimlik Doğrulama (bir kez)\n\n"
    "Google Earth Engine (GEE) API'yi kullanabilmek için önce kimlik doğrulaması yapın.\n\n"
    "- Kullanıcı hesabı ile interaktif doğrulama:\n\n"
    "```bash\n"
    "earthengine authenticate\n"
    "```\n\n"
    "- Alternatif: Servis hesabı ile çalışacaksanız ortam değişkenlerini ayarlayın:\n\n"
    "```bash\n"
    "export EE_SERVICE_ACCOUNT=\"service-account@project.iam.gserviceaccount.com\"\n"
    "export EE_PRIVATE_KEY_FILE=\"/path/to/key.json\"\n"
    "export EE_PROJECT=\"your-project-id\"\n"
    "```\n\n"
    "Ardından defterde `ee_init(project=...)` çağrısı yapılır (CLI ve pipeline buna göre çalışır).\n"
)


def insert_steps(nb: dict) -> bool:
    cells = nb.get("cells", [])
    # If steps already present, do nothing
    text = "\n".join(["".join(c.get("source", [])) for c in cells if c.get("cell_type") == "markdown"])
    if STEP0_MARK in text or STEP1_MARK in text:
        return False
    # Build new markdown cells
    def md_cell(text: str) -> dict:
        return {"cell_type": "markdown", "metadata": {}, "source": [line + ("\n" if not line.endswith("\n") else "") for line in text.splitlines()]}
    new_cells = [md_cell(STEP0_MD), md_cell(STEP1_MD)]
    # Insert after first cell if exists, else prepend
    insert_at = 1 if cells else 0
    nb["cells"] = cells[:insert_at] + new_cells + cells[insert_at:]
    return True


def main():
    p = Path("analysis.ipynb")
    nb = json.loads(p.read_text(encoding="utf-8"))
    if insert_steps(nb):
        p.write_text(json.dumps(nb, ensure_ascii=False, indent=1), encoding="utf-8")
        print("Step markdown inserted")
    else:
        print("Steps already present; no changes")


if __name__ == "__main__":
    main()

