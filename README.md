# weasyprint-flexoki

A small toolkit for turning **HTML, Markdown, and Jinja templates** into polished PDFs with **WeasyPrint 68.1**.

It started as a Flexoki-flavored PDF starter, but it has grown into a more flexible document kit for:
- reports
- letters
- briefs
- handouts
- reusable template-driven documents
- editorial HTML and magazine-style experiments

## Why this exists

WeasyPrint is excellent, but raw HTML-to-PDF output often feels plain. This project gives you better defaults, cleaner templates, and a set of style presets so documents feel intentional instead of merely rendered.

## What you get

- WeasyPrint pinned to **68.1**
- one bundled stylesheet with multiple theme presets
- HTML to PDF rendering
- Markdown to PDF rendering
- Jinja template to PDF rendering
- built-in letter and report templates
- a generated GitHub trending magazine demo
- GitHub Actions that render example outputs on CI

## Theme presets

For Markdown and Jinja templates, you can choose:

- `light` - default Flexoki editorial look
- `dark` - dark Flexoki for screen-first documents
- `terminal` - terminal-blog / hacker minimalism
- `indie-web` - serif personal-site / indie-web feel
- `retro-neon` - retro cyber-neon dark preset
- `brutalist` - stark black-and-white minimalism

## Installation

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e .
```

## Quick start

### HTML

```bash
weasyprint-flexoki examples/article-light.html dist/article-light.pdf
weasyprint-flexoki examples/article-dark.html dist/article-dark.pdf
```

### Markdown

```bash
weasyprint-flexoki examples/clinical-brief.md dist/clinical-brief.pdf

weasyprint-flexoki \
  examples/clinical-brief.md \
  dist/clinical-brief-terminal.pdf \
  --theme terminal \
  --title "Clinical Brief"
```

### Jinja templates

```bash
weasyprint-flexoki \
  src/weasyprint_flexoki/templates/letter.html.j2 \
  dist/letter.pdf \
  --context examples/letter-context.json

weasyprint-flexoki \
  src/weasyprint_flexoki/templates/report.html.j2 \
  dist/report-indie-web.pdf \
  --context examples/report-context.json \
  --theme indie-web \
  --title "Quarterly Operations Report"
```

## Python API

```python
from weasyprint_flexoki import render_document_to_pdf

render_document_to_pdf("examples/article-light.html", "dist/article-light.pdf")
render_document_to_pdf("examples/clinical-brief.md", "dist/clinical-brief.pdf", theme="terminal")
render_document_to_pdf(
    "src/weasyprint_flexoki/templates/report.html.j2",
    "dist/report.pdf",
    context_path="examples/report-context.json",
    theme="indie-web",
)
```

## Supported inputs

- `.html`
- `.md`
- `.html.j2` with `--context <json-file>`

## Included examples

### HTML
- `examples/article-light.html`
- `examples/article-dark.html`
- `examples/github-trending-magazine.html`
- `examples/github-trending-magazine-print.html`

### Markdown
- `examples/clinical-brief.md`

### Templates
- `src/weasyprint_flexoki/templates/letter.html.j2`
- `src/weasyprint_flexoki/templates/report.html.j2`
- `src/weasyprint_flexoki/templates/github-trending-magazine-screen.html.j2`
- `src/weasyprint_flexoki/templates/github-trending-magazine-print.html.j2`

### Context / generated data
- `examples/letter-context.json`
- `examples/report-context.json`
- `examples/github-trending-magazine-data.json`

## GitHub trending magazine

The repo includes a generator for a weekly GitHub-trending magazine issue.

It produces:
- interactive screen HTML
- print/export HTML
- JSON issue data
- PDF export

Run it with:

```bash
python scripts/generate_github_trending_magazine.py \
  --period week \
  --screen-output examples/github-trending-magazine.html \
  --print-output examples/github-trending-magazine-print.html \
  --data-output examples/github-trending-magazine-data.json \
  --pdf-output dist/github-trending-magazine-weekly.pdf
```

Note:
- the weekly issue targets **12 repos across 14 pages**
- if GitHub returns fewer than 12 weekly repos, the generator tops up from the daily feed to preserve the format

## GitHub Actions

The workflow in `.github/workflows/render-examples.yml`:
- regenerates the weekly magazine assets
- renders example PDFs
- runs on push, pull request, and manual dispatch
- uploads rendered PDFs as artifacts

## Project structure

```text
weasyprint-flexoki/
├── .github/workflows/
│   └── render-examples.yml
├── assets/
│   └── preview-light.png
├── examples/
│   ├── article-dark.html
│   ├── article-light.html
│   ├── clinical-brief.md
│   ├── github-trending-magazine-data.json
│   ├── github-trending-magazine-print.html
│   ├── github-trending-magazine.html
│   ├── letter-context.json
│   ├── report-context.json
│   └── template-render-demo.md
├── scripts/
│   └── generate_github_trending_magazine.py
├── src/weasyprint_flexoki/
│   ├── cli.py
│   ├── flexoki.css
│   ├── render.py
│   └── templates/
│       ├── github-trending-magazine-print.html.j2
│       ├── github-trending-magazine-screen.html.j2
│       ├── letter.html.j2
│       └── report.html.j2
└── pyproject.toml
```

## Design notes

The default visual language is inspired by **Flexoki** by Steph Ango, adapted here for PDF-first document rendering.

- Upstream repo: https://github.com/kepano/flexoki
- Project page: https://stephango.com/flexoki
- Upstream license: MIT

This repo does **not** bundle the full Flexoki project. It uses a focused stylesheet and theme system built for WeasyPrint output.

## Good fits

This toolkit works especially well for:
- internal memos
- clinical briefs
- formal letters
- short reports
- one-page handouts
- reusable document templates
- editorial PDF experiments
- magazine-style HTML and PDF outputs

## License

MIT
