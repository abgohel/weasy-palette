from __future__ import annotations

import argparse
from pathlib import Path

from .render import render_document_to_pdf


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Render an HTML or Markdown file to PDF with WeasyPrint 68.1 and the bundled Flexoki stylesheet."
    )
    parser.add_argument("input_html", help="Path to the source HTML or Markdown file")
    parser.add_argument("output_pdf", help="Path to the output PDF file")
    parser.add_argument(
        "--theme",
        choices=["light", "dark"],
        default="light",
        help="Theme used for Markdown input (HTML files manage their own theme)",
    )
    parser.add_argument(
        "--title",
        help="Optional document title for Markdown input",
    )
    return parser


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()
    output = render_document_to_pdf(
        Path(args.input_html),
        Path(args.output_pdf),
        theme=args.theme,
        title=args.title,
    )
    print(f"Rendered {output}")


if __name__ == "__main__":
    main()
