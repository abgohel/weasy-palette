# Impeccable design notes

<span class="section-number">01 / Imported design language</span>
<p class="section-subtitle">This example shows the reusable styles pulled from the impeccable repo into weasy-palette: editorial typography, framed panels, category chips, and softer product-report cards.</p>

<div class="chips">
  <span class="chip chip-create">Create</span>
  <span class="chip chip-evaluate">Evaluate</span>
  <span class="chip chip-refine">Refine</span>
  <span class="chip chip-simplify">Simplify</span>
  <span class="chip chip-harden">Harden</span>
  <span class="chip chip-system">System</span>
</div>

<div class="frame">
  <p><strong>What came over:</strong> serif display rhythm, clean sans body text, mono metadata, paper-toned surfaces, magenta accent handling, sharper framed containers, and the command-category badge palette.</p>
</div>

## Editorial helpers

The `impeccable` preset now supports a few helper classes that fit PDF work well, not just the theme variables.

- `section-number` for mono section markers
- `section-subtitle` for muted editorial intros
- `frame` for a sharper bordered panel with subtle depth
- `chip` plus category variants for command- or workflow-style labels
- `pullquote` for a more magazine-like highlighted statement

<p class="pullquote">The goal is not to clone impeccable.style. It is to bring its strongest document-friendly styling patterns into printable HTML and PDF output.</p>

## Why this matters

These additions make the preset more useful for reports, design docs, and editorial PDFs, especially when you want a product-design feel without falling back to generic SaaS cards.
