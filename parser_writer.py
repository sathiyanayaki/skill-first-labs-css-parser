"""Beginner-friendly CSS parser for the Skill First Labs task.

Extracts CSS selectors and declaration property/value pairs into JSON.
This is a small educational parser, not a complete CSS-standard parser.
"""
import json
import sys
from pathlib import Path


def remove_comments(css_text):
    """Remove CSS comments while preserving comment-like text inside quotes."""
    result = []
    i = 0
    quote = None

    while i < len(css_text):
        char = css_text[i]

        if quote:
            result.append(char)
            if char == "\\" and i + 1 < len(css_text):
                result.append(css_text[i + 1])
                i += 2
                continue
            if char == quote:
                quote = None
            i += 1
            continue

        if char in ("'", '"'):
            quote = char
            result.append(char)
            i += 1
        elif css_text.startswith("/*", i):
            end = css_text.find("*/", i + 2)
            if end == -1:
                # An unfinished comment: ignore the rest of the file.
                break
            i = end + 2
        else:
            result.append(char)
            i += 1

    return "".join(result)


def split_top_level(text, delimiter):
    """Split by comma/semicolon only outside quotes and parentheses."""
    parts = []
    current = []
    quote = None
    depth = 0
    i = 0

    while i < len(text):
        char = text[i]

        if quote:
            current.append(char)
            if char == "\\" and i + 1 < len(text):
                current.append(text[i + 1])
                i += 2
                continue
            if char == quote:
                quote = None
        elif char in ("'", '"'):
            quote = char
            current.append(char)
        elif char == "(":
            depth += 1
            current.append(char)
        elif char == ")":
            depth = max(0, depth - 1)
            current.append(char)
        elif char == delimiter and depth == 0:
            parts.append("".join(current).strip())
            current = []
        else:
            current.append(char)

        i += 1

    parts.append("".join(current).strip())
    return [part for part in parts if part]


def parse_css(css_text):
    """Parse simple CSS rules into a dictionary suitable for JSON output."""
    cleaned_css = remove_comments(css_text)
    rules = []
    position = 0

    while position < len(cleaned_css):
        opening = cleaned_css.find("{", position)
        if opening == -1:
            break

        closing = cleaned_css.find("}", opening + 1)
        if closing == -1:
            # Malformed rule: no closing brace, so stop without crashing.
            break

        selector_text = cleaned_css[position:opening].strip()
        body = cleaned_css[opening + 1:closing]
        position = closing + 1

        # This beginner parser skips at-rules such as @media.
        if not selector_text or selector_text.startswith("@"):
            continue

        selectors = split_top_level(selector_text, ",")
        declarations = []

        for item in split_top_level(body, ";"):
            if ":" not in item:
                # Ignore malformed declarations instead of crashing.
                continue

            property_name, value = item.split(":", 1)
            property_name = property_name.strip()
            value = value.strip()

            if property_name and value:
                declarations.append({
                    "property": property_name,
                    "value": value
                })

        rules.append({
            "selectors": selectors,
            "declarations": declarations
        })

    return {
        "rule_count": len(rules),
        "selectors": [s for rule in rules for s in rule["selectors"]],
        "rules": rules
    }


def main():
    if len(sys.argv) != 2:
        print("Usage: python parser_writer.py <css-file>")
        raise SystemExit(1)

    css_file = Path(sys.argv[1])

    try:
        css_text = css_file.read_text(encoding="utf-8")
    except OSError as error:
        print(f"Could not read file: {error}", file=sys.stderr)
        raise SystemExit(1)

    print(json.dumps(parse_css(css_text), indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
