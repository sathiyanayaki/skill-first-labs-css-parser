# Demo video plan (about 2–3 minutes)

1. Introduce the project: "This is my CSS Parser for Milestone 1."
2. Open `sample.css` and point out selectors, properties, and values.
3. Run `python parser_writer.py sample.css`.
4. Point out the JSON keys `rule_count`, `selectors`, and `rules`.
5. Explain the edge case: a semicolon inside a quoted value or URL should not split a declaration.
6. Run `python -m unittest discover -s tests -v` and show all tests passing.
7. Finish by explaining the parser's current scope: ordinary CSS rule blocks; nested at-rules are not supported.
