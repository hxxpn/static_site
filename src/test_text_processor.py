from text_processor import (
    split_nodes_delimiter,
    split_nodes_image,
    split_nodes_links,
    Delimeters,
    text_to_textnodes,
    extract_markdown_images,
    extract_markdown_links,
)
import unittest
from textnode import TextNode, TextType


class TestTextNodeSplitting(unittest.TestCase):
    def test_split_with_bold(self):
        test_text_node = TextNode("This is example with **bold**", TextType.TEXT)
        old_nodes = [test_text_node]

        result = split_nodes_delimiter(old_nodes, Delimeters.BOLD)
        expected_result = [
            TextNode("This is example with ", TextType.TEXT),
            TextNode("bold", TextType.BOLD),
        ]

        self.assertEqual(result, expected_result)

    def test_split_bold_first_word(self):
        test_text_node = TextNode("**bold** stuff", TextType.TEXT)
        old_nodes = [test_text_node]

        result = split_nodes_delimiter(old_nodes, Delimeters.BOLD)
        expected_result = [
            TextNode("bold", TextType.BOLD),
            TextNode(" stuff", TextType.TEXT),
        ]
        self.assertEqual(result, expected_result)

    def test_split_images(self):
        unsplit_image_node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )

        result = split_nodes_image([unsplit_image_node])

        expected_nodes = [
            TextNode("This is text with an ", TextType.TEXT),
            TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
            TextNode(" and another ", TextType.TEXT),
            TextNode("second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"),
        ]

        self.assertEqual(result, expected_nodes)

    def test_split_links(self):
        unsplit_link_node = TextNode(
            "This is text with an [image](https://i.imgur.com/zjjcJKZ.png) and another [second image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )

        result = split_nodes_links([unsplit_link_node])

        expected_nodes = [
            TextNode("This is text with an ", TextType.TEXT),
            TextNode("image", TextType.LINK, "https://i.imgur.com/zjjcJKZ.png"),
            TextNode(" and another ", TextType.TEXT),
            TextNode("second image", TextType.LINK, "https://i.imgur.com/3elNhQu.png"),
        ]

        self.assertEqual(result, expected_nodes)

    def test_text_to_nodes(self):
        text = "This is **text** with an *italic* word and a `code block` and an ![image](https://i.imgur.com/zjjcJKZ.png) and a [link](https://boot.dev)"
        tn = TextNode(text=text, text_type=TextType.TEXT)

        result = text_to_textnodes(text)
        expected = [
            TextNode("This is ", TextType.TEXT),
            TextNode("text", TextType.BOLD),
            TextNode(" with an ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" word and a ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(" and an ", TextType.TEXT),
            TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
            TextNode(" and a ", TextType.TEXT),
            TextNode("link", TextType.LINK, "https://boot.dev"),
        ]
        self.assertEqual(result, expected)


class TestExtractImageLint(unittest.TestCase):
    def test_extract_image_happy_path(self):
        text = (
            "This is text ![image](https://i.im.png) and ![another](https://i.im.png)"
        )
        t = TextNode(text, text_type=TextType.TEXT)
        res = extract_markdown_images(t)

        self.assertEqual(
            res, [("image", "https://i.im.png"), ("another", "https://i.im.png")]
        )

    def test_extract_link(self):
        text = "This is text [image](https://i.im.png) and [another](https://i.im.png)"
        t = TextNode(text, text_type=TextType.TEXT)
        res = extract_markdown_links(t)

        self.assertEqual(
            res, [("image", "https://i.im.png"), ("another", "https://i.im.png")]
        )
