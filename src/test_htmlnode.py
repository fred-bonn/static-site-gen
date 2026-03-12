import unittest

from htmlnode import HTMLnode, LeafNode, ParentNode

class TestHTMLnode(unittest.TestCase):
    def test_not_implemented(self):
        node = HTMLnode("div")
        with self.assertRaises(NotImplementedError):
            node.to_html()
            
    def test_props_to_html_none(self):
        node = HTMLnode("div")
        leaf = LeafNode("p", "Hello, world!")
        parent = ParentNode("div", [leaf])
        self.assertEqual(node.props_to_html(), "")
        self.assertEqual(leaf.props_to_html(), "")
        self.assertEqual(parent.props_to_html(), "")

    def test_props_to_html(self):
        node = HTMLnode("div", props={"class": "container", "id": "main"})
        self.assertEqual(node.props_to_html(), ' class="container" id="main"')

    def test_leaf_to_html(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

    def test_leaf_to_html_notag(self):
        node = LeafNode(None, "Hello, world!")
        self.assertEqual(node.to_html(), "Hello, world!")

    def test_leaf_to_html_with_props(self):
        node = LeafNode("a", "Click here", props={"href": "www.example.com"})
        self.assertEqual(node.to_html(), '<a href="www.example.com">Click here</a>')

    def test_to_html_with_child(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span><b>grandchild</b></span></div>")

    def test_parentnode_no_tag(self):
        parent_node = ParentNode(None, [LeafNode("span", "child")])
        with self.assertRaises(ValueError):
            parent_node.to_html()

    def test_parentnode_none_children(self):
        parent_node = ParentNode("div", None)
        with self.assertRaises(ValueError):
            parent_node.to_html()

    def test_parentnode_no_children(self):
        parent_node = ParentNode("div", [])
        with self.assertRaises(ValueError):
            parent_node.to_html()

    def test_to_html_with_children(self):
        parent_node = ParentNode("div", [LeafNode("span", "child"), LeafNode(None, "other child")])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span>other child</div>")

    def test_parent_to_html_with_props(self):
        parent_node = ParentNode("div", [LeafNode("span", "child"), LeafNode(None, "other child")], props={"class": "container"})
        self.assertEqual(parent_node.to_html(), '<div class="container"><span>child</span>other child</div>')

    def test_parent_to_html_with_mixed_children(self):
        parent_node = ParentNode("div", [LeafNode("span", "child"), ParentNode("p", [LeafNode(None, "other child"), LeafNode("span", "another child")])], props={"class": "container"})
        self.assertEqual(parent_node.to_html(), '<div class="container"><span>child</span><p>other child<span>another child</span></p></div>')