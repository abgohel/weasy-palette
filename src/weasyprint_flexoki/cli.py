from __future__ import annotations

import argparse
from pathlib import Path

from .render import render_html_to_pdf


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Render an HTML file to PDF with WeasyPrint 68.1 and the bundled Flexoki stylesheet."
    )
    parser.add_argument("input_html", help="Path to the source HTML file")
    parser.add_argument("output_pdf", help="Path to the output PDF file")
    return parser


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()
    output = render_html_to_pdf(Path(args.input_html), Path(args.output_pdf))
    print(f"Rendered {output}")


if __name__ == "__main__":
    main()
