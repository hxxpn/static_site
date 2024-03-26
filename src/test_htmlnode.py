from unittest import TestCase
from htmlnode import HTMLNode, LeafNode, ParentNode


class TestHTMLNode(TestCase):
    def test_props_to_html_one_prop(self):
        test_prop = {"href": "linky link"}

        test_html_node = HTMLNode("p", "This is some text", None, test_prop)

        result = test_html_node.props_to_html()
        expected_res = ' href="linky link"'

        self.assertEqual(result, expected_res)

    def test_to_html(self):
        test_html_node = HTMLNode("p", "This is some text", None, {})

        with self.assertRaises(Exception):
            test_html_node.to_html()


class TestLeafNode(TestCase):
    def test_leaf_node_creation(self):
        test_prop = {"href": "linky link", "target": "potato"}

        test_leaf = LeafNode("p", "This is some text", None, test_prop)

        result = test_leaf.to_html()
        expected_res = '<p href="linky link" target="potato">This is some text</p>'

        self.assertEqual(result, expected_res)

    def test_link_node(self):
        test_prop = {"href": "linky link"}

        test_leaf = LeafNode("a", "This is some text", None, test_prop)

        result = test_leaf.to_html()
        expected_res = '<a href="linky link">This is some text</a>'

        self.assertEqual(result, expected_res)

    def test_missing_value(self):
        with self.assertRaises(ValueError):
            _ = LeafNode("a", None, None, None)

    def test_no_tag(self):
        test_leaf = LeafNode(None, "some val")

        result = test_leaf.to_html()

        self.assertEqual(result, "some val")


class TestParentNode(TestCase):
    def test_parent_node_creation(self):
        test_node = ParentNode(
            "p",
            children=[
                LeafNode("b", "Bold text"),
                LeafNode(None, "Normal text"),
                LeafNode("i", "italic text"),
                LeafNode(None, "Normal text"),
            ],
        )

        result = test_node.to_html()
        expected_result = (
            "<p><b>Bold text</b>Normal text<i>italic text</i>Normal text</p>"
        )

        self.assertEqual(result, expected_result)

    def test_parent_node_creation_fail_no_tag(self):
        with self.assertRaises(ValueError):
            _ = ParentNode(tag=None, children=[], value=None)

    def test_parent_node_creation_fail_no_children(self):
        with self.assertRaises(ValueError):
            _ = ParentNode(tag="tag", children=None, value=None)

    def test_parent_node_creation_fail_value_not_none(self):
        with self.assertRaises(ValueError):
            _ = ParentNode(tag="tag", children=[], value="value")

    def test_nested_parent_node_one_level(self):
        test_node_lowest = ParentNode("p", children=[LeafNode("a", "depth_1")])

        test_node_root = ParentNode(
            "div", children=[test_node_lowest, LeafNode("p", "I am also here")]
        )

        result = test_node_root.to_html()
        expected_res = "<div><p><a>depth_1</a></p><p>I am also here</p></div>"
        self.assertEqual(result, expected_res)
