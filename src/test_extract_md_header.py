import unittest
from extract_title import extract_title

class TestExtractTitle(unittest.TestCase):
    def test_valid_extract(self):
        md = """
# Header text that should be extracted as valid

Some header text that goes here, this should not be taken
Just want another line."""
        self.assertEqual(extract_title(md), f"Header text that should be extracted as valid")
        
    def test_not_valid_extract(self):
        md = """
There is not header in this string thus there should be no match and
an Exception should be raised by the function."""
        with self.assertRaises(Exception):
            _ = extract_title(md)

    def test_multi_headers(self):
        md = """
# this string will have
# multiple headers but,
# only the first one should be returned
# a match"""
        self.assertEqual(extract_title(md), f"this string will have")
