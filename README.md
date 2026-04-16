# weasyprint-flexoki

A small starter repo that combines **WeasyPrint 68.1** with the **Flexoki** color system to produce warm, editorial, print-friendly PDFs.

It is meant as a clean starting point for:
- reports
- essays
- internal memos
- Markdown-based briefs
- one-page handouts
- branded clinical or academic PDFs

## Preview

![WeasyPrint Flexoki preview](assets/preview-light.png)

## What you get

- `weasyprint==68.1` pinned in `pyproject.toml`
- a reusable `flexoki.css` stylesheet tuned for PDF output
- sample light and dark HTML documents
- Markdown to PDF support built into the CLI
- a clinical brief example that is closer to real-world handout / summary work
- a tiny CLI for rendering HTML to PDF with WeasyPrint
- a small Python API you can call directly
- a GitHub Actions workflow that renders example PDFs on push and pull requests

## Quick start

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e .
weasyprint-flexoki examples/article-light.html dist/article-light.pdf
weasyprint-flexoki examples/article-dark.html dist/article-dark.pdf
weasyprint-flexoki examples/clinical-brief.md dist/clinical-brief.pdf
```

Markdown input supports `--theme` and `--title`:

```bash
weasyprint-flexoki examples/clinical-brief.md dist/clinical-brief-dark.pdf --theme dark --title "Clinical Brief"
```

## Python usage

```python
from weasyprint_flexoki import render_document_to_pdf

render_document_to_pdf("examples/article-light.html", "dist/article-light.pdf")
render_document_to_pdf("examples/clinical-brief.md", "dist/clinical-brief.pdf")
```

## Project layout

```text
weasyprint-flexoki/
├── .github/workflows/
│   └── render-examples.yml
├── assets/
│   └── preview-light.png
├── examples/
│   ├── article-dark.html
│   ├── article-light.html
│   └── clinical-brief.md
├── src/weasyprint_flexoki/
│   ├── cli.py
│   ├── flexoki.css
│   └── render.py
└── pyproject.toml
```

## Design notes

This repo uses the **Flexoki** palette and naming conventions from the upstream project by Steph Ango, but applies them in a PDF-first way for WeasyPrint.

- Upstream project: https://github.com/kepano/flexoki
- Project page: https://stephango.com/flexoki
- Upstream license: MIT

This starter kit does **not** bundle the whole upstream repository. It includes a focused stylesheet built around the Flexoki palette for PDF generation.

## Included examples

- `examples/article-light.html` for a light editorial page
- `examples/article-dark.html` for an on-screen dark variant
- `examples/clinical-brief.md` for a more practical one-page clinic / report layout

## Why this combo works

WeasyPrint is excellent for HTML-to-PDF workflows, but the default visual result is often too plain. Flexoki gives the output a calmer and more literary feel while keeping contrast strong enough for serious reading.

That makes this combo especially good for prose-heavy documents where you want something softer than a typical corporate PDF, but still clean and professional.

## Ideas for next steps

- Jinja templates for letters and reports
- branded themes for hospitals, research groups, or newsletters
- cover pages, footers, and appendix templates
- optional front matter support for Markdown metadata
- release workflow that publishes packaged builds

## License

MIT
