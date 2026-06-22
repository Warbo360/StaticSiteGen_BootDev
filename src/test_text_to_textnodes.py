import unittest
from textnode import TextNode, TextType
from extract_markdown import text_to_textnodes

class TestTextToTextNodes(unittest.TestCase):
    def test_all_pattern_match(self):
        text = (
            "This is **text** with an _italic_ word and a `code block` and an ![obi wan"
            " image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        )
        nodes = [
            TextNode("This is ", TextType.PLAIN),
            TextNode("text", TextType.BOLD),
            TextNode(" with an ", TextType.PLAIN),
            TextNode("italic", TextType.ITALIC),
            TextNode(" word and a ", TextType.PLAIN),
            TextNode("code block", TextType.CODE),
            TextNode(" and an ", TextType.PLAIN),
            TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
            TextNode(" and a ", TextType.PLAIN),
            TextNode("link", TextType.LINK, "https://boot.dev"),
        ]
        self.assertEqual(text_to_textnodes(text), nodes)

    def test_multiple_pattern_type(self):
        text = (
            "This is **text** with an _italic_ word and a `code block` and an ![obi wan"
            " image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
            " **more bold text** for testing of properly catching of multiple of one pattern"
            " **2nd more bold text**."
        )
        nodes = [
            TextNode("This is ", TextType.PLAIN),
            TextNode("text", TextType.BOLD),
            TextNode(" with an ", TextType.PLAIN),
            TextNode("italic", TextType.ITALIC),
            TextNode(" word and a ", TextType.PLAIN),
            TextNode("code block", TextType.CODE),
            TextNode(" and an ", TextType.PLAIN),
            TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
            TextNode(" and a ", TextType.PLAIN),
            TextNode("link", TextType.LINK, "https://boot.dev"),
            TextNode(" ", TextType.PLAIN),
            TextNode("more bold text", TextType.BOLD),
            TextNode(" for testing of properly catching of multiple of one pattern ", TextType.PLAIN),
            TextNode("2nd more bold text", TextType.BOLD),
            TextNode(".", TextType.PLAIN)
        ]
        self.assertEqual(text_to_textnodes(text), nodes)

    def test_unmatched_delimter(self):

        # There is an unmatched delimiter in this so should raise a value error from split_nodes_delimiter

        text1 = (
            "This is **text* with an _italic_ word and a `code block` and an ![obi wan"
            " image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
            " **more bold text** for testing of properly catching of multiple of one pattern"
            " **2nd more bold text**."
        )
        text2 = (
            "This is **text** with an _italic_ word and a code block` and an ![obi wan"
            " image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
            " **more bold text** for testing of properly catching of multiple of one pattern"
            " **2nd more bold text**."
        )
        text3 = (
            "This is **text** with an _italic word and a code `block` and an ![obi wan"
            " image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
            " **more bold text** for testing of properly catching of multiple of one pattern"
            " **2nd more bold text**."
        )
        with self.assertRaises(ValueError):
            _ = text_to_textnodes(text1)
        with self.assertRaises(ValueError):
            _ = text_to_textnodes(text2)
        with self.assertRaises(ValueError):
            _ = text_to_textnodes(text3)

    def test_no_patterns_to_split(self):
        text1 = (
            "This is text with an italic word and a code block and an ![obi wan"
            " image[]](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](()https://boot.dev)"
            " more bold text for testing of properly catching of multiple of one pattern"
            " 2nd more bold text."
        )
        self.assertEqual(text_to_textnodes(text1), [TextNode(text1, TextType.PLAIN)])

    def test_raise_error(self):
        not_text1 = 21
        not_text2 = 2.1
        not_text3 = ["words", 21]
        not_text4 = {"words": 21}
        not_text5 = {21, 1, 5}
        not_text6 = (21, 1, 6)
        not_text7 = TextNode("", TextType.PLAIN)
        with self.assertRaises(TypeError):
            _ = text_to_textnodes(not_text1)
        with self.assertRaises(TypeError):
            _ = text_to_textnodes(not_text2)
        with self.assertRaises(TypeError):
            _ = text_to_textnodes(not_text3)
        with self.assertRaises(TypeError):
            _ = text_to_textnodes(not_text4)
        with self.assertRaises(TypeError):
            _ = text_to_textnodes(not_text5)
        with self.assertRaises(TypeError):
            _ = text_to_textnodes(not_text6)
        with self.assertRaises(TypeError):
            _ = text_to_textnodes(not_text7)

if __name__ == "__main__":
    unittest.main()
