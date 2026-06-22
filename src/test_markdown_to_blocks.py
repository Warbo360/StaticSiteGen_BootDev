import unittest
from markdown_to_blocks import markdown_to_blocks

class TestMarkdownToBlocks(unittest.TestCase):
    def test_site(self):
        text = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
        self.assertEqual(
            markdown_to_blocks(text),
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ]
        )

    def test_pattern2(self):
        text = """
This is **bolded** text in a paragraph that continues on
This is still part of the same paragraph, testing with various lengths of paragraphs
This is still that same paragraph but with an _italic_ in the paragraph
or how about an inline ![Image](https://Imagelink.png)
or maybe an inline actual [link](https://ALinkToNoWhere.com)

- Or an unordered list now
- Another item
- item number 3

1. An ordered list now
2. item 2
3. item 3

One last one line paragraph
"""
        self.assertEqual(
            markdown_to_blocks(text),
            [
                (
                    "This is **bolded** text in a paragraph that continues on\nThis is still part of the same paragraph, "
                    "testing with various lengths of paragraphs\nThis is still that same paragraph but with an _italic_ in "
                    "the paragraph\nor how about an inline ![Image](https://Imagelink.png)\nor maybe an inline actual"
                    " [link](https://ALinkToNoWhere.com)"
                ),
                "- Or an unordered list now\n- Another item\n- item number 3",
                "1. An ordered list now\n2. item 2\n3. item 3",
                "One last one line paragraph"
            ]
        )
