import unittest
from htmlnode import HTMLNode, LeafNode, ParentNode

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

class TestLeafNode(unittest.TestCase):
    def test_leaf_child(self):
        with self.assertRaises(TypeError):
            _ = LeafNode()

    def test_leaf_to_html_p(self):
        nodep = LeafNode("p", "Hello, world!")
        nodeh = LeafNode("h1", "Hello, world!")
        node_main = LeafNode("main", "Hello, world!")
        self.assertEqual(nodep.to_html(), "<p>Hello, world!</p>")
        self.assertEqual(nodeh.to_html(), "<h1>Hello, world!</h1>")
        self.assertEqual(node_main.to_html(), "<main>Hello, world!</main>")

class TestParentNode(unittest.TestCase):
    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )

    def test_to_html_with_great_grandchildren(self):
        great_grandchild_node = LeafNode("p", "great-grandchild")
        grandchild_node = ParentNode("span", [great_grandchild_node])
        child_node = ParentNode("div", [grandchild_node])
        parent_node = ParentNode("main", [child_node])
        self.assertEqual(
                parent_node.to_html(),
                "<main><div><span><p>great-grandchild</p></span></div></main>"
                )

    def test_to_html_with_multi_childs(self):
        child1 = LeafNode("p", "child1")
        child2 = LeafNode("a", "child2")
        child3 = LeafNode("b", "child3")
        child4 = LeafNode("body", "child4")
        children = [child1, child2, child3, child4]
        parent = ParentNode("main", children)
        self.assertEqual(
                parent.to_html(),
                "<main><p>child1</p><a>child2</a><b>child3</b><body>child4</body></main>"
                )

    def test_parent_node_none_value(self):
        invalid_child = LeafNode("b", None)
        valid_child = LeafNode("b", "this is a test node")
        parent = ParentNode("p", [invalid_child])
        childless_parent = ParentNode("b", None)
        tagless_parent = ParentNode(None, [valid_child])
        self.assertEqual(parent.value, None)
        with self.assertRaises(ValueError):
            _ = parent.to_html()
        with self.assertRaises(ValueError):
            _ = childless_parent.to_html()
        with self.assertRaises(ValueError):
            _ = tagless_parent.to_html()
        

if __name__ == "__main__":
    unittest.main()
