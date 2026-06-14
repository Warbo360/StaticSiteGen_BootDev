import unittest
from htmlnode import HTMLNode, LeafNode

class TestLeafNode(unittest.TestCase):
    def test_leaf_child(self):
        child_list = [HTMLNode(), HTMLNode()]
        with self.assertRaises(ValueError):
            _ = LeafNode(None, "This is a test value", child_list, None)
        with self.assertRaises(TypeError):
            _ = LeafNode()

    def test_leaf_to_html_p(self):
        nodep = LeafNode("p", "Hello, world!")
        nodeh = LeafNode("h1", "Hello, world!")
        node_main = LeafNode("main", "Hello, world!")
        self.assertEqual(nodep.to_html(), "<p>Hello, world!</p>")
        self.assertEqual(nodeh.to_html(), "<h1>Hello, world!</h1>")
        self.assertEqual(node_main.to_html(), "<main>Hello, world!</main>")

if __name__ == "__main__":
    unittest.main()
