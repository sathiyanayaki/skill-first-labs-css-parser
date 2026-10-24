# Skill First Labs – Milestone 1: CSS Parser

## What it does
Reads a CSS file and extracts:
- selectors, such as `.header` and `#main`
- declaration properties, such as `color` and `font-size`
- property values, such as `blue` and `16px`

The result is printed as JSON. This is an educational parser for ordinary CSS rules, not a complete CSS-standard parser. Nested at-rules such as `@media` are not supported.

## Requirements
- Python 3.10 or newer
- No external packages

## Run it
Open a terminal in this folder:

```bash
python parser_writer.py sample.css
```

To run the tests:

```bash
python -m unittest discover -s tests -v
```

## 3–4 line task explanation
I extracted CSS selectors and declaration property-value pairs because they describe which elements are styled and how. I output the information as JSON so other programs can easily read and reuse it. The parser handles comments, comma-separated selectors, and values containing semicolons inside quotes or parentheses. One edge case is malformed CSS, such as a missing closing brace; the parser stops safely rather than crashing.

## GitHub
Create a repository named `skill-first-labs-css-parser`, upload the files while preserving the `tests` folder, and copy the repository URL for submission. Follow the organizer's instructions for repository visibility.
