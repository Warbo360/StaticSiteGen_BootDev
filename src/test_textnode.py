import unittest
from textnode import TextNode, TextType

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

if __name__ == "__main__":
    unittest.main()
