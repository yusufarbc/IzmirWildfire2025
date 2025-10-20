#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/../paper"

# Clean auxiliary files (optional)
rm -f main.{aux,out,toc,log,synctex.gz,fls,fdb_latexmk}

echo "[1/2] pdflatex main.tex"
pdflatex -interaction=nonstopmode -halt-on-error main.tex >/dev/null
echo "[2/2] pdflatex main.tex (second pass)"
pdflatex -interaction=nonstopmode -halt-on-error main.tex >/dev/null

echo "PDF built: $(pwd)/main.pdf"

