# weasyprint-flexoki

A small starter repo that combines **WeasyPrint 68.1** with the **Flexoki** color system to produce clean, print-friendly PDFs.

The goal is simple: give you a ready-to-push repo with a nice default aesthetic for prose-heavy documents, reports, letters, and one-page handouts.

## What is included

- `weasyprint==68.1` pinned in `pyproject.toml`
- a reusable `flexoki.css` stylesheet for PDF-friendly typography
- sample light and dark HTML documents
- a tiny CLI for rendering HTML to PDF with WeasyPrint

## Quick start

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e .
weasyprint-flexoki examples/article-light.html dist/article-light.pdf
weasyprint-flexoki examples/article-dark.html dist/article-dark.pdf
```

## Project layout

```text
weasyprint-flexoki/
├── examples/
├── src/weasyprint_flexoki/
│   ├── cli.py
│   ├── flexoki.css
│   └── render.py
└── pyproject.toml
```

## Notes on Flexoki

This repo uses the Flexoki palette and naming conventions from the upstream project by Steph Ango.

- Upstream: https://github.com/kepano/flexoki
- License: MIT
- Courtesy / attribution: https://stephango.com/flexoki

This starter kit does **not** bundle the entire upstream repo. It only includes a PDF-oriented stylesheet built around the Flexoki palette.

## Next ideas

- Jinja templates for reports and letters
- markdown-to-pdf pipeline
- branded hospital / academic handout presets
- cover pages and appendix layouts

## License

MIT
