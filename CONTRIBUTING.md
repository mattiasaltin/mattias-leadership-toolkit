# Contributing to Mattias Leadership Toolkit

Thank you for considering a contribution. This toolkit is a curated Markdown library of
leadership resources. British English spelling is used throughout ("organised", "optimise",
"prioritise").

## How to contribute

1. Fork the repository and create a branch.
2. Make your changes following the domain guides and the definition of done below.
3. Run `make check-all` (Markdown lint + nav + link check).
4. Open a pull request with a short explanation of why the resource belongs.

## Where to contribute

- **Engineering:** [engineering-leadership-resources/CONTRIBUTING.md](engineering-leadership-resources/CONTRIBUTING.md)
- **Product:** [product-leadership-resources/CONTRIBUTING.md](product-leadership-resources/CONTRIBUTING.md)

## Resource format

```markdown
📘 [Title](url) by Author  
A brief description of the resource and why it’s valuable
```

Icons: 📘 Book · 🎥 Video/Talk · 📄 Article/Blog · 🎧 Podcast · 📊 Research Paper/Whitepaper

## Definition of done (adding or moving a topic file)

When you add, rename, or remove a topic `.md` file, update all of the following:

1. The topic file itself (resources, Related Topics, Navigation — include Toolkit root link)
2. The section `README.md` (engineering) or domain Quick Nav (product)
3. Domain Quick Nav / Start Here paths if the topic is foundational
4. Neighbouring prev/next links so the browse chain stays consistent
5. Related Topics on closely related pages (prefer a real cross-link over duplication)
6. `mkdocs.yml` nav entry (published site sidebar)
7. `make check-all` passes locally (lint + nav + links); `make docs-build` for site changes

Do **not** invent placeholder URLs. Prefer durable sources (books, primary research, canonical
articles) over ephemeral webinars when both exist. After changing a URL, confirm the final page
title matches the citation (HTTP 200 alone is not enough — SVPG/ThoughtWorks often soft-404).

## Deduplication

If a resource already lives on another page, link to that page in Related Topics instead of
pasting the same entry again. Shared people-leadership material (coaching, recruiting craft)
should have one canonical home.

## Code of Conduct

This project follows the [Code of Conduct](CODE_OF_CONDUCT.md).
