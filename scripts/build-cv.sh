#!/usr/bin/env bash
set -euo pipefail
project_root="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
"${PYTHON:-python3}" "$project_root/scripts/generate-cv.py"
# Build twice (via latexmk) to resolve the LastPage reference and keep aux files out of source.
build_dir="$(mktemp -d "${TMPDIR:-/tmp}/homepage-cv.XXXXXX")"
trap 'rm -rf "$build_dir"' EXIT
cd "$project_root/media/files"
latexmk -pdf -interaction=nonstopmode -halt-on-error -outdir="$build_dir" cv.tex
cp "$build_dir/cv.pdf" cv.pdf
