import unittest
from htmlnode import HTMLNode

class TestHTMLNode(unittest.TestCase):
    def test_HTML_tag(self):
        node = HTMLNode("This is a test self.tag")
        node_none = HTMLNode()
        self.assertEqual(node.tag, "This is a test self.tag")
        self.assertIsNone(node_none.tag)

    def test_HTML_value(self):
        node = HTMLNode(None, "This is a test self.value")
        node_none = HTMLNode()
        self.assertEqual(node.value, "This is a test self.value")
        self.assertIsNone(node_none.value)

    def test_HTML_children(self):
        child1 = HTMLNode()
        child2 = HTMLNode()
        child_list = [child1, child2]
        parent = HTMLNode(None, None, child_list)
        parent_none = HTMLNode()
        self.assertIsInstance(parent.children, list)
        self.assertEqual(parent.children, [child1, child2])
        self.assertIsNone(parent_none.children)

    def test_HTML_props(self):
        test_dict = {"This is a test prop key": "This is a test prop value"}
        node = HTMLNode(None, None, None, test_dict)
        node_none = HTMLNode()
        self.assertIsInstance(node.props, dict)
        self.assertEqual(node.props, {"This is a test prop key": "This is a test prop value"})
        self.assertIsNone(node_none.props)

    def test_props_to_html(self):
        test_dict = {"This is a test prop key": "This is a test prop value"}
        node = HTMLNode(None, None, None, test_dict)
        node_none = HTMLNode()
        self.assertEqual(node.props_to_html(), f" This is a test prop key=\"This is a test prop value\"")
        self.assertEqual(node_none.props_to_html(), "")

if __name__ == "__main__":
    unittest.main()
