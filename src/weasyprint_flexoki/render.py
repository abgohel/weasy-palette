from __future__ import annotations

from pathlib import Path

from weasyprint import CSS, HTML


PACKAGE_DIR = Path(__file__).resolve().parent
DEFAULT_STYLESHEET = PACKAGE_DIR / "flexoki.css"


def render_html_to_pdf(input_html: str | Path, output_pdf: str | Path) -> Path:
    """Render an HTML file to PDF using the bundled Flexoki stylesheet."""
    input_path = Path(input_html).resolve()
    output_path = Path(output_pdf).resolve()
    output_path.parent.mkdir(parents=True, exist_ok=True)

    html = HTML(filename=str(input_path), base_url=str(input_path.parent))
    css = CSS(filename=str(DEFAULT_STYLESHEET))
    html.write_pdf(str(output_path), stylesheets=[css])
    return output_path
