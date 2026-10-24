import unittest
from parser_writer import parse_css


class TestCSSParser(unittest.TestCase):
    def test_extracts_selector_and_properties(self):
        result = parse_css(".box { color: red; font-size: 12px; }")
        self.assertEqual(result["rule_count"], 1)
        self.assertEqual(result["selectors"], [".box"])
        self.assertEqual(
            result["rules"][0]["declarations"][0],
            {"property": "color", "value": "red"}
        )

    def test_multiple_selectors(self):
        result = parse_css(".a, .b { color: blue; }")
        self.assertEqual(result["selectors"], [".a", ".b"])

    def test_semicolon_inside_url_is_preserved(self):
        result = parse_css('.x { background: url("image;wide.png"); }')
        self.assertEqual(
            result["rules"][0]["declarations"][0]["value"],
            'url("image;wide.png")'
        )

    def test_comments_and_malformed_declaration(self):
        result = parse_css("/* note */ .x { color: green; broken; }")
        self.assertEqual(result["rule_count"], 1)
        self.assertEqual(len(result["rules"][0]["declarations"]), 1)

    def test_unclosed_rule_does_not_crash(self):
        result = parse_css(".x { color: red;")
        self.assertEqual(result["rule_count"], 0)


if __name__ == "__main__":
    unittest.main()
