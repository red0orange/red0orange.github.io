# Dehao Huang's academic homepage

A Jekyll / GitHub Pages site retaining the Minimal Mistakes-style sidebar, white background, and blue links.

## Local preview

Use Ruby and Bundler compatible with `tools/Gemfile.lock` (Bundler 2.2.7), then:

```bash
BUNDLE_GEMFILE=tools/Gemfile bundle install
./scripts/run-jekyll.sh serve --config _config.yml,_config.dev.yml --host 127.0.0.1 --port 4000
```

Visit `http://127.0.0.1:4000`. To build without serving:

```bash
./scripts/run-jekyll.sh build
```

## Updating the homepage

The homepage is one continuous researcher profile: introduction, research, education and experience, open source, and awards. The navigation links to sections on that page; CV opens the PDF and Blogs remains separate.

- `_pages/about.md`: the single-page profile and concise background information.
- `_data/profile.yml`: research introduction and Scholar URL, shared by the homepage and PDF CV. Keep the sidebar Scholar URL in `_config.yml` synchronized.
- `_data/publications.yml`: titles, authors, publication status, year, descriptions, and resource links. Keep newest work first within each year. Set `status` to `published` or `preprint`; list each paper once.
- `featured: true`: shows the paper in the default Selected view. All papers remain available through the All filter and in the PDF CV. Without JavaScript the full list is visible.
- `_includes/research-entry.html`: one research row combining the figure or video preview, title, authors, venue, summary, and resource links.
- `display_title`: an optional concise research headline; the full paper title and authors remain in the expandable citation. This does not alter the PDF CV.
- `_sass/_academic.scss`: shared theme refinements. `_sass/_research-home.scss` adds the homepage typography, larger research figures, citation disclosures, and date-aligned background information without changing blog layouts.
- `static/js/research-index.js`: filtering, direct paper anchors, and section navigation. `research-media.js` loads video players only on demand.

The former `/highlight/` and `/publications/` URLs redirect to `/#research`; `/projects/` redirects to `/#open-source`. `/cv/` and `/resume` open the PDF. Existing `/portfolio/portfolio-N/` URLs redirect to the corresponding paper anchor on the homepage. Publication anchors such as `/#rtagrasp` automatically reveal the full list when needed. Images are local and lazy-loaded.

## Rebuilding the CV

The editable template is `media/files/cv.tex`. Install a LaTeX distribution with `latexmk` and the Python package PyYAML, then:

```bash
python3 -m pip install PyYAML
./scripts/build-cv.sh
```

The script regenerates `cv_research.tex` and `cv_publications.tex` from the shared data, builds in a temporary directory, resolves page references, and replaces `media/files/cv.pdf` only after compilation succeeds. Set `PYTHON=/path/to/python` to use a virtual environment. Review the two-page PDF after changing content; its layout is not guaranteed to remain two pages as publications grow.

## One-page Chinese resume

The Chinese resume is `output/pdf/黄德豪_中文简历_一页版.pdf`. Its editable source is `scripts/build-cv-zh.py`, which reads publication authors, venues, and status from the shared data. Run it with a Python environment containing `reportlab`, `PyYAML`, and `pypdf`; the current font configuration uses macOS Heiti SC and Arial. The script enforces a single A4 page. Render and visually review the PDF after changing content or spacing.

## Research figure sources

Figures are reproduced from the corresponding research project or author-uploaded paper, without changing scientific content.

| Local asset | Source |
| --- | --- |
| `media/images/research/erlt.jpg` | [eRLT video poster](https://red0orange.github.io/eRLT_site/assets/media/overview.jpg) |
| `media/images/research/vlaconf.png` | [VLAConf problem formulation](https://arxiv.org/html/2605.29605v2/images/problem_formulation.png) |
| `media/images/research/hgdiffuser.png` | [HGDiffuser pipeline](https://arxiv.org/html/2503.00508v1/main_pipeline_v4.png) |
| `media/images/research/cocoreviewbench.png` | [CoCoReviewBench framework](https://arxiv.org/html/2605.07905v2/framework.png) |

Additional research figures: [Easy-IIL](https://arxiv.org/html/2603.12769v2/intro.png), [RTAGrasp](https://arxiv.org/html/2409.16033v1/intro_5.png), and [OmniScientist](https://arxiv.org/html/2511.16931v2/OmniScientist_framework.png). Files ending in `-video.jpg` are thumbnails from the corresponding YouTube demonstrations listed in the publication data. Video players load only when the visitor chooses to play a demonstration; the same links work without JavaScript.

Publication metadata was checked against arXiv and the cited publisher/project pages in November 2026. CoCoReviewBench is listed as ICML 2026; eRLT, VLAConf, Easy-IIL, and OmniScientist remain labeled as preprints. Do not add Code or Video links until a working public resource is available.
