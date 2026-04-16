# Jinja template rendering examples

Use the bundled templates with JSON context files:

```bash
weasyprint-flexoki src/weasyprint_flexoki/templates/letter.html.j2 dist/letter.pdf --context examples/letter-context.json
weasyprint-flexoki src/weasyprint_flexoki/templates/report.html.j2 dist/report.pdf --context examples/report-context.json
weasyprint-flexoki src/weasyprint_flexoki/templates/cv.html.j2 dist/cv-public.pdf --context examples/cv-context.json --theme indie-web
```

You can also point the CLI at your own `.html.j2` files and pass any matching JSON context.
