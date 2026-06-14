import unittest
from textnode import TextNode, TextType, text_node_to_html_node

class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)

    def test_noteq(self):
        node1 = TextNode("This is the 1st text node", TextType.BOLD)
        node2 = TextNode("This is the 2nd text node", TextType.ITALIC)
        self.assertNotEqual(node1, node2)

    def test_NoneUrl(self):
        node = TextNode("This is a text node", TextType.BOLD)
        self.assertIsNone(node.url)

    def test_URL(self):
        node = TextNode("This is a text node", TextType.BOLD, "https://This is a test URL")
        self.assertIs(node.url, "https://This is a test URL")

    def test_TextType(self):
        plain_node = TextNode("This is a plain text node", TextType.PLAIN)
        italic_node  = TextNode("This is a plain text node", TextType.ITALIC)
        bold_node  = TextNode("This is a plain text node", TextType.BOLD)
        code_node  = TextNode("This is a plain text node", TextType.CODE)
        link_node  = TextNode("This is a plain text node", TextType.LINK)
        image_node  = TextNode("This is a plain text node", TextType.IMAGE)
        self.assertIs(plain_node.text_type.value, "plain")
        self.assertIs(italic_node.text_type.value, "italic")
        self.assertIs(bold_node.text_type.value, "bold")
        self.assertIs(code_node.text_type.value, "code")
        self.assertIs(link_node.text_type.value, "link")
        self.assertIs(image_node.text_type.value, "image")
    
    def test_text(self):
        plain_node = TextNode("This is a text node", TextType.PLAIN)
        italic_node = TextNode("This is a italic node", TextType.ITALIC)
        bold_node = TextNode("This is a bold node", TextType.BOLD)
        code_node = TextNode("This is a code node", TextType.CODE)
        link_node = TextNode("This is a link node", TextType.LINK, "https://www.This is a test.com")
        image_node = TextNode("This is a image node", TextType.IMAGE, "./this/is/the/way/image.png")
        plain_html_node = text_node_to_html_node(plain_node)
        italic_html_node = text_node_to_html_node(italic_node)
        bold_html_node = text_node_to_html_node(bold_node)
        code_html_node = text_node_to_html_node(code_node)
        link_html_node = text_node_to_html_node(link_node)
        image_html_node = text_node_to_html_node(image_node)
        self.assertEqual(plain_html_node.tag, None)
        self.assertEqual(plain_html_node.value, "This is a text node")
        self.assertEqual(italic_html_node.tag, "i")
        self.assertEqual(italic_html_node.value, "This is a italic node")
        self.assertEqual(bold_html_node.tag, "b")
        self.assertEqual(bold_html_node.value, "This is a bold node")
        self.assertEqual(code_html_node.tag, "code")
        self.assertEqual(code_html_node.value, "This is a code node")
        self.assertEqual(link_html_node.tag, "a")
        self.assertEqual(link_html_node.value, "This is a link node")
        self.assertEqual(link_html_node.props, {"href": "https://www.This is a test.com"})
        self.assertEqual(image_html_node.tag, "img")
        self.assertEqual(image_html_node.value, "")
        self.assertEqual(image_html_node.props, {"src": "./this/is/the/way/image.png", "alt": "This is a image node"})

if __name__ == "__main__":
    unittest.main()
