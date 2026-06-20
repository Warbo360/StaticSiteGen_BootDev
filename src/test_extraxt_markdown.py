import unittest
from extract_markdown import extract_markdown_images, extract_markdown_links, split_nodes_image, split_nodes_link
from textnode import TextNode, TextType

class TestMarkdownExtractImage(unittest.TestCase):
    def test_valid_pattern(self):
        pattern1 = "![ThisIsATest](https://ThisIsATest.png)"
        pattern2 = "![](https://TestingWithNoAltText)"
        pattern3 = "Some test text around the wanted pattern ![AltText](https://url.png) More test text"
        pattern4 = (
            "Some place holder text to imbed multiple pattern that should match ![AltText](https://url.png)"
            "This should result in 3 matches total so should be a list of 3 elements when this test case finishes"
            "![AltText2](https://url2.jpeg), then how about one more for good measure ![Alt3](https://url3.gif) some padding"
            "also for good measure I would say"
        )
        self.assertEqual(extract_markdown_images(pattern1), [("ThisIsATest", "https://ThisIsATest.png")])
        self.assertEqual(extract_markdown_images(pattern2), [("", "https://TestingWithNoAltText")])
        self.assertEqual(extract_markdown_images(pattern3), [("AltText", "https://url.png")])
        self.assertEqual(
            extract_markdown_images(pattern4),
            [
                ("AltText", "https://url.png"),
                ("AltText2", "https://url2.jpeg"),
                ("Alt3", "https://url3.gif")
            ]
        )

    def test_not_valid_pattern(self):
        pattern1 = "![nested[]](https:www.nestbrackets.com)"
        pattern2 = "[NormalLink](https:www.wrongelement!.com)"
        pattern3 = "![NestedParens](https://().com)"
        self.assertEqual(extract_markdown_images(pattern1), [])
        self.assertEqual(extract_markdown_images(pattern2), [])
        self.assertEqual(extract_markdown_images(pattern3), [])

    def test_type_error(self):
        invalid_int = 21
        invalid_float = 2.1
        invalid_list = ["words", 21, 2.1]
        invalid_dict = {"test": 21, "test2": 2.1}
        invalid_tuple = (1, 2, 3)
        invalid_set = {1, 2, 3, 4}
        invalid_bool = True
        invalid_None = None
        with self.assertRaises(TypeError):
            _ = extract_markdown_images(invalid_int)
        with self.assertRaises(TypeError):
            _ = extract_markdown_images(invalid_float)
        with self.assertRaises(TypeError):
            _ = extract_markdown_images(invalid_list)
        with self.assertRaises(TypeError):
            _ = extract_markdown_images(invalid_dict)
        with self.assertRaises(TypeError):
            _ = extract_markdown_images(invalid_tuple)
        with self.assertRaises(TypeError):
            _ = extract_markdown_images(invalid_set)
        with self.assertRaises(TypeError):
            _ = extract_markdown_images(invalid_bool)
        with self.assertRaises(TypeError):
            _ = extract_markdown_images(invalid_None)

class TestMarkdownExtractLink(unittest.TestCase):
    def test_valid_pattern(self):
        pattern1 = "[AltText](https://linktoimage.png)"
        pattern3 = "[Alt1](https://linktoimage1.png) some test text [Alt2](https://linktoimage2.png)"
        self.assertEqual(extract_markdown_links(pattern1), [("AltText", "https://linktoimage.png")])
        self.assertEqual(extract_markdown_links(
            pattern3),
            [("Alt1", "https://linktoimage1.png"), ("Alt2", "https://linktoimage2.png")]
        )

    def test_not_valid_pattern(self):
        pattern1 = "[nested[]](https:www.nestbrackets.com)"
        pattern2 = "![NormalLink](https:www.wrongelement!.com)"
        pattern3 = "[NestedParens](https://().com)"
        self.assertEqual(extract_markdown_links(pattern1), [])
        self.assertEqual(extract_markdown_links(pattern2), [])
        self.assertEqual(extract_markdown_links(pattern3), [])


    def test_type_error(self):
        invalid_int = 21
        invalid_float = 2.1
        invalid_list = ["words", 21, 2.1]
        invalid_dict = {"test": 21, "test2": 2.1}
        invalid_tuple = (1, 2, 3)
        invalid_set = {1, 2, 3, 4}
        invalid_bool = True
        invalid_None = None
        with self.assertRaises(TypeError):
            _ = extract_markdown_links(invalid_int)
        with self.assertRaises(TypeError):
            _ = extract_markdown_links(invalid_float)
        with self.assertRaises(TypeError):
            _ = extract_markdown_links(invalid_list)
        with self.assertRaises(TypeError):
            _ = extract_markdown_links(invalid_dict)
        with self.assertRaises(TypeError):
            _ = extract_markdown_links(invalid_tuple)
        with self.assertRaises(TypeError):
            _ = extract_markdown_links(invalid_set)
        with self.assertRaises(TypeError):
            _ = extract_markdown_links(invalid_bool)
        with self.assertRaises(TypeError):
            _ = extract_markdown_links(invalid_None)

class TestSplitNodesImage(unittest.TestCase):
    def test_nothing_extracted(self):
        node1 = TextNode(
            "This contains no pattern to extract thus should append the whole thing as one node",
            TextType.PLAIN
        )
        node2 = TextNode(
            "This is another node with no pattern to extract so I can make a proper list of text nodes for testing",
            TextType.PLAIN
        )
        self.assertEqual(split_nodes_image([node1]), [node1])
        self.assertEqual(split_nodes_image([node1, node2]), [node1, node2])

    def test_string_w_one_pattern(self):
        node1 = TextNode(
            f"This contains a inline image ![Image1](https://www.imagehere.png) this should match",
            TextType.PLAIN
        )
        self.assertEqual(
            split_nodes_image([node1]),
            [
                TextNode("This contains a inline image ", TextType.PLAIN),
                TextNode("Image1", TextType.IMAGE, "https://www.imagehere.png"),
                TextNode(" this should match", TextType.PLAIN)
                ]
        )

    def test_string_w_patterns(self):
        node1 = TextNode(
            "![Image](https://ImageHere.jpeg) Then some more text",
            TextType.PLAIN
        )
        node2 = TextNode(
            "The node comes at the end of the string ![Image](https://ImageHere.jpeg)",
            TextType.PLAIN
        )
        node3 = TextNode(
            "![Image](https://ImageHere.jpeg) Then some middle text ![Image2](https://ImageHere2.jpeg)",
            TextType.PLAIN
        )
        node4 = TextNode(
            (
                "This will be a test of a long string with multiple nodes to extract ![Image1](https://Image1.jpeg)"
                "More text that goes here ![Image2](https://Image2.png) more text more text, how about more text"
                "![Image3](https://Image3.gif). This sure is some crazy amount of text that goes here. How is your day"
                "? I hope ok ![Image4](https://Image4.png) and some final text that can go here before ending with"
                " one more image link ![Image5](https://Image5.png)"
            ),
            TextType.PLAIN
        )
        self.assertEqual(
            split_nodes_image([node4]),
            [
                TextNode("This will be a test of a long string with multiple nodes to extract ", TextType.PLAIN),
                TextNode("Image1", TextType.IMAGE, "https://Image1.jpeg"),
                TextNode("More text that goes here ", TextType.PLAIN),
                TextNode("Image2", TextType.IMAGE, "https://Image2.png"),
                TextNode(" more text more text, how about more text", TextType.PLAIN),
                TextNode("Image3", TextType.IMAGE, "https://Image3.gif"),
                TextNode(
                    ". This sure is some crazy amount of text that goes here. How is your day? I hope ok ",
                    TextType.PLAIN
                ),
                TextNode("Image4", TextType.IMAGE, "https://Image4.png"),
                TextNode(
                    " and some final text that can go here before ending with one more image link ",
                    TextType.PLAIN
                ),
                TextNode("Image5", TextType.IMAGE, "https://Image5.png")
            ]
        )
        self.assertEqual(
            split_nodes_image([node1]),
            [
                TextNode("Image", TextType.IMAGE, "https://ImageHere.jpeg"),
                TextNode(" Then some more text", TextType.PLAIN)
            ]
        )
        self.assertEqual(
            split_nodes_image([node2]),
            [
                TextNode("The node comes at the end of the string ", TextType.PLAIN),
                TextNode("Image", TextType.IMAGE, "https://ImageHere.jpeg")
            ]
        )
        self.assertEqual(
            split_nodes_image([node3]),
            [
                TextNode("Image", TextType.IMAGE, "https://ImageHere.jpeg"),
                TextNode(" Then some middle text ", TextType.PLAIN),
                TextNode("Image2", TextType.IMAGE, "https://ImageHere2.jpeg"),
            ]
        )
        self.assertEqual(
            split_nodes_image([node1, node2]),
            [
                TextNode("Image", TextType.IMAGE, "https://ImageHere.jpeg"),
                TextNode(" Then some more text", TextType.PLAIN),
                TextNode("The node comes at the end of the string ", TextType.PLAIN),
                TextNode("Image", TextType.IMAGE, "https://ImageHere.jpeg")
            ]
        )
        self.assertEqual(
            split_nodes_image([node1, node3]),
            [
                TextNode("Image", TextType.IMAGE, "https://ImageHere.jpeg"),
                TextNode(" Then some more text", TextType.PLAIN),
                TextNode("Image", TextType.IMAGE, "https://ImageHere.jpeg"),
                TextNode(" Then some middle text ", TextType.PLAIN),
                TextNode("Image2", TextType.IMAGE, "https://ImageHere2.jpeg"),
            ]
        )
        self.assertEqual(
            split_nodes_image([node2, node3]),
            [
                TextNode("The node comes at the end of the string ", TextType.PLAIN),
                TextNode("Image", TextType.IMAGE, "https://ImageHere.jpeg"),
                TextNode("Image", TextType.IMAGE, "https://ImageHere.jpeg"),
                TextNode(" Then some middle text ", TextType.PLAIN),
                TextNode("Image2", TextType.IMAGE, "https://ImageHere2.jpeg"),
            ]
        )
        self.assertEqual(
            split_nodes_image([node1, node2, node3]),
            [
                TextNode("Image", TextType.IMAGE, "https://ImageHere.jpeg"),
                TextNode(" Then some more text", TextType.PLAIN),
                TextNode("The node comes at the end of the string ", TextType.PLAIN),
                TextNode("Image", TextType.IMAGE, "https://ImageHere.jpeg"),
                TextNode("Image", TextType.IMAGE, "https://ImageHere.jpeg"),
                TextNode(" Then some middle text ", TextType.PLAIN),
                TextNode("Image2", TextType.IMAGE, "https://ImageHere2.jpeg"),
            ]
        )

    def test_empty_alt_text_valid(self):
        node1 = TextNode("![](https://ThisShouldStillExtract.png)", TextType.PLAIN)
        self.assertEqual(
            split_nodes_image([node1]),
            [
                TextNode("", TextType.IMAGE, "https://ThisShouldStillExtract.png")
            ]
        )

    def test_incorrect_patterns_nothing_extracted(self):
        node1 = TextNode("[This is a link](https://ThisIsNotAnImage)", TextType.PLAIN)
        node2 = TextNode("![[This is a nested alt text which should not extract]](https://Wrong.png)", TextType.PLAIN)
        node3 = TextNode("![Alt](https:()NestedBracketsHereAreNotAllowed.png)", TextType.PLAIN)
        node4 = TextNode("![ALTTEXT](https://[]BracketsAreNotAllowedHereEither.png)", TextType.PLAIN)
        self.assertEqual(
            split_nodes_image([node1]),
            [TextNode("[This is a link](https://ThisIsNotAnImage)", TextType.PLAIN)]
        )
        self.assertEqual(
            split_nodes_image([node2]),
            [TextNode("![[This is a nested alt text which should not extract]](https://Wrong.png)", TextType.PLAIN)]
        )
        self.assertEqual(
            split_nodes_image([node3]),
            [TextNode("![Alt](https:()NestedBracketsHereAreNotAllowed.png)", TextType.PLAIN)]
        )
        self.assertEqual(
            split_nodes_image([node4]),
            [TextNode("![ALTTEXT](https://[]BracketsAreNotAllowedHereEither.png)", TextType.PLAIN)]
        )
        self.assertEqual(
            split_nodes_image([node1, node2, node3, node4]),
            [node1, node2, node3, node4]
        )

    def test_type_erros(self):
        node1 = "![Wrong](https://ForgotToPutThisInATextNode.png)"
        node2 = [12, "word", TextNode("![ThisShouldNotWork](https://WRONG.png)", TextType.PLAIN)]
        node3 = 12
        node4 = {"![ThisIsWrong](https://WRONG.png)": TextType.PLAIN}
        node5 = 5.6
        node6 = [] # raises a TypeError since signature accepts list[TextNode]
        node7 = ("![ThisIsWrong](https://WRONG.png)", "![ThisWillNotWork](https://WRONG.png)")
        node8 = {"![ThisIsASetAndWillNotWork](https://WRONG.PNG)", "![WRONG](https://WRONG.png)"}
        with self.assertRaises(TypeError):
            _ = split_nodes_image([node1])
        with self.assertRaises(TypeError):
            _ = split_nodes_image([node2])
        with self.assertRaises(TypeError):
            _ = split_nodes_image([node3])
        with self.assertRaises(TypeError):
            _ = split_nodes_image([node4])
        with self.assertRaises(TypeError):
            _ = split_nodes_image([node5])
        with self.assertRaises(TypeError):
            _ = split_nodes_image([node6])
        with self.assertRaises(TypeError):
            _ = split_nodes_image([node7])
        with self.assertRaises(TypeError):
            _ = split_nodes_image([node8])

class TextSplitLinkNodes(unittest.TestCase):
    def test_nothing_extracted(self):
        node1 = TextNode(
            "This contains no pattern to extract thus should append the whole thing as one node",
            TextType.PLAIN
        )
        node2 = TextNode(
            "This is another node with no pattern to extract so I can make a proper list of text nodes for testing",
            TextType.PLAIN
        )
        self.assertEqual(split_nodes_link([node1]), [node1])
        self.assertEqual(split_nodes_link([node1, node2]), [node1, node2])

    def test_string_w_one_pattern(self):
        node1 = TextNode(
            f"This contains a inline link [Link1](https://www.link1.png) this should match",
            TextType.PLAIN
        )
        self.assertEqual(
            split_nodes_link([node1]),
            [
                TextNode("This contains a inline link ", TextType.PLAIN),
                TextNode("Link1", TextType.LINK, "https://www.link1.png"),
                TextNode(" this should match", TextType.PLAIN)
                ]
        )

    def test_string_w_patterns(self):
        node1 = TextNode(
            "[Image](https://ImageHere.jpeg) Then some more text",
            TextType.PLAIN
        )
        node2 = TextNode(
            "The node comes at the end of the string [Image](https://ImageHere.jpeg)",
            TextType.PLAIN
        )
        node3 = TextNode(
            "[Image](https://ImageHere.jpeg) Then some middle text [Image2](https://ImageHere2.jpeg)",
            TextType.PLAIN
        )
        node4 = TextNode(
            (
                "This will be a test of a long string with multiple nodes to extract [Image1](https://Image1.jpeg)"
                "More text that goes here [Image2](https://Image2.png) more text more text, how about more text"
                "[Image3](https://Image3.gif). This sure is some crazy amount of text that goes here. How is your day"
                "? I hope ok [Image4](https://Image4.png) and some final text that can go here before ending with"
                " one more image link [Image5](https://Image5.png)"
            ),
            TextType.PLAIN
        )
        self.assertEqual(
            split_nodes_link([node4]),
            [
                TextNode("This will be a test of a long string with multiple nodes to extract ", TextType.PLAIN),
                TextNode("Image1", TextType.LINK, "https://Image1.jpeg"),
                TextNode("More text that goes here ", TextType.PLAIN),
                TextNode("Image2", TextType.LINK, "https://Image2.png"),
                TextNode(" more text more text, how about more text", TextType.PLAIN),
                TextNode("Image3", TextType.LINK, "https://Image3.gif"),
                TextNode(
                    ". This sure is some crazy amount of text that goes here. How is your day? I hope ok ",
                    TextType.PLAIN
                ),
                TextNode("Image4", TextType.LINK, "https://Image4.png"),
                TextNode(
                    " and some final text that can go here before ending with one more image link ",
                    TextType.PLAIN
                ),
                TextNode("Image5", TextType.LINK, "https://Image5.png")
            ]
        )
        self.assertEqual(
            split_nodes_link([node1]),
            [
                TextNode("Image", TextType.LINK, "https://ImageHere.jpeg"),
                TextNode(" Then some more text", TextType.PLAIN)
            ]
        )
        self.assertEqual(
            split_nodes_link([node2]),
            [
                TextNode("The node comes at the end of the string ", TextType.PLAIN),
                TextNode("Image", TextType.LINK, "https://ImageHere.jpeg")
            ]
        )
        self.assertEqual(
            split_nodes_link([node3]),
            [
                TextNode("Image", TextType.LINK, "https://ImageHere.jpeg"),
                TextNode(" Then some middle text ", TextType.PLAIN),
                TextNode("Image2", TextType.LINK, "https://ImageHere2.jpeg"),
            ]
        )
        self.assertEqual(
            split_nodes_link([node1, node2]),
            [
                TextNode("Image", TextType.LINK, "https://ImageHere.jpeg"),
                TextNode(" Then some more text", TextType.PLAIN),
                TextNode("The node comes at the end of the string ", TextType.PLAIN),
                TextNode("Image", TextType.LINK, "https://ImageHere.jpeg")
            ]
        )
        self.assertEqual(
            split_nodes_link([node1, node3]),
            [
                TextNode("Image", TextType.LINK, "https://ImageHere.jpeg"),
                TextNode(" Then some more text", TextType.PLAIN),
                TextNode("Image", TextType.LINK, "https://ImageHere.jpeg"),
                TextNode(" Then some middle text ", TextType.PLAIN),
                TextNode("Image2", TextType.LINK, "https://ImageHere2.jpeg"),
            ]
        )
        self.assertEqual(
            split_nodes_link([node2, node3]),
            [
                TextNode("The node comes at the end of the string ", TextType.PLAIN),
                TextNode("Image", TextType.LINK, "https://ImageHere.jpeg"),
                TextNode("Image", TextType.LINK, "https://ImageHere.jpeg"),
                TextNode(" Then some middle text ", TextType.PLAIN),
                TextNode("Image2", TextType.LINK, "https://ImageHere2.jpeg"),
            ]
        )
        self.assertEqual(
            split_nodes_link([node1, node2, node3]),
            [
                TextNode("Image", TextType.LINK, "https://ImageHere.jpeg"),
                TextNode(" Then some more text", TextType.PLAIN),
                TextNode("The node comes at the end of the string ", TextType.PLAIN),
                TextNode("Image", TextType.LINK, "https://ImageHere.jpeg"),
                TextNode("Image", TextType.LINK, "https://ImageHere.jpeg"),
                TextNode(" Then some middle text ", TextType.PLAIN),
                TextNode("Image2", TextType.LINK, "https://ImageHere2.jpeg"),
            ]
        )

    def test_empty_alt_text_valid(self):
        node1 = TextNode("[](https://ThisShouldStillExtract.png)", TextType.PLAIN)
        self.assertEqual(split_nodes_link([node1]),[node1])

    def test_incorrect_patterns_nothing_extracted(self):
        node1 = TextNode("![This is a link](https://ThisIsNotAnImage)", TextType.PLAIN)
        node2 = TextNode("[[This is a nested alt text which should not extract]](https://Wrong.png)", TextType.PLAIN)
        node3 = TextNode("[Alt](https:()NestedBracketsHereAreNotAllowed.png)", TextType.PLAIN)
        node4 = TextNode("[ALTTEXT](https://[]BracketsAreNotAllowedHereEither.png)", TextType.PLAIN)
        self.assertEqual(
            split_nodes_link([node1]),
            [TextNode("![This is a link](https://ThisIsNotAnImage)", TextType.PLAIN)]
        )
        self.assertEqual(
            split_nodes_link([node2]),
            [TextNode("[[This is a nested alt text which should not extract]](https://Wrong.png)", TextType.PLAIN)]
        )
        self.assertEqual(
            split_nodes_link([node3]),
            [TextNode("[Alt](https:()NestedBracketsHereAreNotAllowed.png)", TextType.PLAIN)]
        )
        self.assertEqual(
            split_nodes_link([node4]),
            [TextNode("[ALTTEXT](https://[]BracketsAreNotAllowedHereEither.png)", TextType.PLAIN)]
        )
        self.assertEqual(
            split_nodes_link([node1, node2, node3, node4]),
            [node1, node2, node3, node4]
        )

    def test_type_erros(self):
        node1 = "![Wrong](https://ForgotToPutThisInATextNode.png)"
        node2 = [12, "word", TextNode("![ThisShouldNotWork](https://WRONG.png)", TextType.PLAIN)]
        node3 = 12
        node4 = {"![ThisIsWrong](https://WRONG.png)": TextType.PLAIN}
        node5 = 5.6
        node6 = [] # raises a TypeError since signature accepts list[TextNode]
        node7 = ("![ThisIsWrong](https://WRONG.png)", "![ThisWillNotWork](https://WRONG.png)")
        node8 = {"![ThisIsASetAndWillNotWork](https://WRONG.PNG)", "![WRONG](https://WRONG.png)"}
        with self.assertRaises(TypeError):
            _ = split_nodes_link([node1])
        with self.assertRaises(TypeError):
            _ = split_nodes_link([node2])
        with self.assertRaises(TypeError):
            _ = split_nodes_link([node3])
        with self.assertRaises(TypeError):
            _ = split_nodes_link([node4])
        with self.assertRaises(TypeError):
            _ = split_nodes_link([node5])
        with self.assertRaises(TypeError):
            _ = split_nodes_link([node6])
        with self.assertRaises(TypeError):
            _ = split_nodes_link([node7])
        with self.assertRaises(TypeError):
            _ = split_nodes_link([node8])

if __name__ == "__main__":
    unittest.main()
