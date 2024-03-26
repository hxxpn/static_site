import unittest

from textnode import TextNode, TextType


class TestTextNode(unittest.TestCase):
    def test_eq_different(self):
        test_node1 = TextNode("a", "bold", "url")
        test_node2 = TextNode("b", "bold", "url")

        self.assertNotEqual(test_node1, test_node2)

    def test_eq_equal(self):
        test_node1 = TextNode("a", "bold", "url")
        test_node2 = TextNode("a", "bold", "url")

        self.assertEqual(test_node1, test_node2)

    def test_equal_with_none_url(self):
        test_node1 = TextNode("a", "bold", None)
        test_node2 = TextNode("a", "bold", None)

        self.assertEqual(test_node1, test_node2)

    def test_not_equal_with_none_url(self):
        test_node1 = TextNode("a", "bold", "something")
        test_node2 = TextNode("a", "bold", None)

        self.assertNotEqual(test_node1, test_node2)

    def test_text_type_is_different(self):
        test_node1 = TextNode("a", "italic", "something")
        test_node2 = TextNode("a", "bold", "something")

        self.assertNotEqual(test_node1, test_node2)
