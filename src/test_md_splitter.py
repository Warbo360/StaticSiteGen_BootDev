import unittest
from md_splitter import split_nodes_delimiter
from textnode import TextType, TextNode

class TextSplitNodesDelimiter(unittest.TestCase):
    def test_not_plain_nodes(self):
        node1 = TextNode("This is 1 test node", TextType.ITALIC)
        node2 = TextNode("This is 2 test node", TextType.BOLD)
        node3 = TextNode("This is 3 test node", TextType.CODE)
        node4 = TextNode("This is 4 test node", TextType.ITALIC)
        old_nodes = [node1, node2, node3, node4]
        self.assertEqual(
            split_nodes_delimiter(old_nodes, "_", TextType.ITALIC),
            old_nodes
        ) 
        self.assertEqual(
            split_nodes_delimiter(old_nodes, "`", TextType.CODE),
            old_nodes
        )
        self.assertEqual(
            split_nodes_delimiter(old_nodes, "**", TextType.BOLD),
            old_nodes
        )
        self.assertEqual(
            split_nodes_delimiter(old_nodes, "**", TextType.BOLD),
            [node1, node2, node3, node4]
        )

    def test_plain_for_italic_nodes(self):
        node1 = TextNode("This is a _italic_ node", TextType.PLAIN)
        node2 = TextNode("This is a **bold** node", TextType.PLAIN)
        node3 = TextNode("This is a `code` node", TextType.PLAIN)
        new_node1 = [
            TextNode("This is a ", TextType.PLAIN),
            TextNode("italic", TextType.ITALIC),
            TextNode(" node", TextType.PLAIN)
        ]
        new_node2 = [
            TextNode("This is a ", TextType.PLAIN),
            TextNode("bold", TextType.BOLD),
            TextNode(" node", TextType.PLAIN)
        ]
        new_node3 = [
            TextNode("This is a ", TextType.PLAIN),
            TextNode("code", TextType.CODE),
            TextNode(" node", TextType.PLAIN)
        ]
        self.assertEqual(
            split_nodes_delimiter([node1], "_", TextType.ITALIC),
            new_node1
        )
        self.assertEqual(
            split_nodes_delimiter([node2], "**", TextType.BOLD),
            new_node2
        )
        self.assertEqual(
            split_nodes_delimiter([node3], "`", TextType.CODE),
            new_node3
        )
        self.assertEqual(
            split_nodes_delimiter([node1, node2], "_", TextType.ITALIC),
            [
                TextNode("This is a ", TextType.PLAIN),
                TextNode("italic", TextType.ITALIC),
                TextNode(" node", TextType.PLAIN),
                node2
            ]
        )
        self.assertEqual(
            split_nodes_delimiter([node2, node3], "**", TextType.BOLD),
            [
                TextNode("This is a ", TextType.PLAIN),
                TextNode("bold", TextType.BOLD),
                TextNode(" node", TextType.PLAIN),
                node3
            ]
        )
        self.assertEqual(
            split_nodes_delimiter([node3, node1], "`", TextType.CODE),
            [
                TextNode("This is a ", TextType.PLAIN),
                TextNode("code", TextType.CODE),
                TextNode(" node", TextType.PLAIN),
                node1
            ]
        )

    def test_non_matching_delimiter_error(self):
        old_node = TextNode("This is **invalid markdown", TextType.PLAIN)
        with self.assertRaises(ValueError):
            _ = split_nodes_delimiter([old_node], "**", TextType.BOLD)

if __name__ == "__main__":
    unittest.main()
