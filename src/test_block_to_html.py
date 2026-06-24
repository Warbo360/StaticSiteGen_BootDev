from block_to_html import markdown_to_html_node
import unittest

class TestBlockToHTML(unittest.TestCase):
    def test_headings(self):
        md = """
### This is a heading to a markdown file"""
        self.assertEqual(
            markdown_to_html_node(md).to_html(),
            "<div><h3>This is a heading to a markdown file</h3></div>"
        )

    def test_paragraphs(self):
        md = """
This is **bolded** paragraph
text in a p
tag here

This is another paragraph with _italic_ text and `code` here

"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
        )

    def test_codeblock(self):
        md = """
```Python
This is text that _should_ remain
the **same** even with inline stuff
```
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><pre><code>This is text that _should_ remain\nthe **same** even with inline stuff\n</code></pre></div>",
        )

    def test_quoteblocks(self):
        md = """
> This is a blockquote
> More block quote with an inline ![Pic1](https://www.imagelink.com)
> Final with **bold** test
"""
        self.assertEqual(
            markdown_to_html_node(md).to_html(),
            (
                "<div><blockquote>This is a blockquote\nMore block quote with an inline <img "
                "src=\"https://www.imagelink.com\""
                " alt=\"Pic1\"></img>\nFinal with <b>bold</b> test</blockquote></div>"
            )
        )

    def test_unordered_list(self):
        md = """
- This is an unordered list with
- various _elements_ like **bold**
- `some code snippet`
"""
        self.assertEqual(
            markdown_to_html_node(md).to_html(),
            (
                "<div><ul>"
                "<li>This is an unordered list with</li>"
                "<li>various <i>elements</i> like <b>bold</b></li>"
                "<li><code>some code snippet</code></li>"
                "</ul></div>"
            )
        )

    def test_ordered_list(self):
        md = """
1. This is an unordered list with
2. various _elements_ like **bold**
3. `some code snippet`
"""
        self.assertEqual(
            markdown_to_html_node(md).to_html(),
            (
                "<div><ol>"
                "<li>This is an unordered list with</li>"
                "<li>various <i>elements</i> like <b>bold</b></li>"
                "<li><code>some code snippet</code></li>"
                "</ol></div>"
            )
        )
