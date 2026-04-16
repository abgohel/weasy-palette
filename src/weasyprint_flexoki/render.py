from __future__ import annotations

import re
from html import escape
from pathlib import Path

import markdown
from weasyprint import CSS, HTML


PACKAGE_DIR = Path(__file__).resolve().parent
DEFAULT_STYLESHEET = PACKAGE_DIR / "flexoki.css"


def _infer_markdown_title(markdown_text: str, fallback: str) -> str:
    match = re.search(r"^#\s+(.+)$", markdown_text, flags=re.MULTILINE)
    return match.group(1).strip() if match else fallback


def _build_markdown_html_document(markdown_text: str, *, title: str, theme: str) -> str:
    body_html = markdown.markdown(
        markdown_text,
        extensions=["extra", "sane_lists", "tables", "fenced_code", "attr_list", "md_in_html"],
    )
    return f"""<!doctype html>
<html lang=\"en\" data-theme=\"{escape(theme)}\">
  <head>
    <meta charset=\"utf-8\" />
    <meta name=\"viewport\" content=\"width=device-width, initial-scale=1\" />
    <title>{escape(title)}</title>
  </head>
  <body>
    <main>
      {body_html}
    </main>
  </body>
</html>
"""


def render_html_to_pdf(input_html: str | Path, output_pdf: str | Path) -> Path:
    """Render an HTML file to PDF using the bundled Flexoki stylesheet."""
    input_path = Path(input_html).resolve()
    output_path = Path(output_pdf).resolve()
    output_path.parent.mkdir(parents=True, exist_ok=True)

    html = HTML(filename=str(input_path), base_url=str(input_path.parent))
    css = CSS(filename=str(DEFAULT_STYLESHEET))
    html.write_pdf(str(output_path), stylesheets=[css])
    return output_path


def render_markdown_to_pdf(
    input_markdown: str | Path,
    output_pdf: str | Path,
    *,
    theme: str = "light",
    title: str | None = None,
) -> Path:
    """Render a Markdown file to PDF using the bundled Flexoki stylesheet."""
    input_path = Path(input_markdown).resolve()
    output_path = Path(output_pdf).resolve()
    output_path.parent.mkdir(parents=True, exist_ok=True)

    markdown_text = input_path.read_text(encoding="utf-8")
    document_title = title or _infer_markdown_title(markdown_text, input_path.stem.replace("-", " ").title())
    html_document = _build_markdown_html_document(markdown_text, title=document_title, theme=theme)

    html = HTML(string=html_document, base_url=str(input_path.parent))
    css = CSS(filename=str(DEFAULT_STYLESHEET))
    html.write_pdf(str(output_path), stylesheets=[css])
    return output_path


def render_document_to_pdf(
    input_path: str | Path,
    output_pdf: str | Path,
    *,
    theme: str = "light",
    title: str | None = None,
) -> Path:
    source_path = Path(input_path)
    if source_path.suffix.lower() in {".md", ".markdown"}:
        return render_markdown_to_pdf(source_path, output_pdf, theme=theme, title=title)
    return render_html_to_pdf(source_path, output_pdf)
