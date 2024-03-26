from unittest import TestCase
from markdown_block import (
    BlockType,
    block_to_block_type,
    heading_block_to_html,
    markdown_to_blocks,
    is_quote,
    is_ordered_list,
    is_unordered_list,
    quote_block_to_html,
    ordered_list_block_to_html,
    unordered_list_block_to_html,
    markdown_to_html_node,
)

from htmlnode import LeafNode, ParentNode


class TestMarkdownBlockProcessing(TestCase):
    def test_markdown_to_blocks(self):
        markdown = "This is a test.\n\nThis is another test."
        expected_result = ["This is a test.", "This is another test."]
        self.assertEqual(markdown_to_blocks(markdown), expected_result)

    def test_is_quote(self):
        lines = ["> This is a quote."]
        self.assertTrue(is_quote(lines))

    def test_is_unordered_list(self):
        lines = ["- Item 1", "- Item 2"]
        self.assertTrue(is_unordered_list(lines))

    def test_is_ordered_list(self):
        lines = ["1. Item 1", "2. Item 2"]
        self.assertTrue(is_ordered_list(lines))

    def test_block_type_quote(self):
        block_quote = ["> Test."]

        result = block_to_block_type(block_quote)

        self.assertEqual(result, [BlockType.QUOTE])

    def test_multiple_blocks(self):
        blocks = ["This is a test.", "> This is a quote.", "- Item 1", "1. Item 1"]
        expected_result = [
            BlockType.PARAGRAPH,
            BlockType.QUOTE,
            BlockType.UNORDERED_LIST,
            BlockType.ORDERED_LIST,
        ]
        self.assertEqual(block_to_block_type(blocks), expected_result)

    def test_heading_block_to_html(self):
        block = "### Heading stuff"
        expected_node = LeafNode(tag="h1", value="Heading stuff")
        result = heading_block_to_html(block)

        self.assertEqual(result.to_html(), expected_node.to_html())

    def test_heading_block_to_html(self):
        block = "### Heading stuff"
        expected_node = LeafNode(tag="h3", value="Heading stuff")
        result = heading_block_to_html(block)

        self.assertEqual(result.to_html(), expected_node.to_html())

    def test_heading_block_to_html_edge_cases(self):
        block_h1 = "# Heading 1"
        expected_node_h1 = LeafNode(tag="h1", value="Heading 1")
        result_h1 = heading_block_to_html(block_h1)

        self.assertEqual(result_h1.to_html(), expected_node_h1.to_html())

        block_h6 = "###### Heading 6"
        expected_node_h6 = LeafNode(tag="h6", value="Heading 6")
        result_h6 = heading_block_to_html(block_h6)

        self.assertEqual(result_h6.to_html(), expected_node_h6.to_html())

    def test_quote_block_to_html(self):
        block = "> Potato\n> Tomato\n> Aristotle"
        expected_node = LeafNode(tag="blockquote", value="Potato\nTomato\nAristotle")
        result = quote_block_to_html(block)

        self.assertEqual(result.to_html(), expected_node.to_html())

    def test_ordered_list_block_to_html(self):
        block = "1. Item 1\n2. Item 2\n3. Item 3"
        expected_node = ParentNode(
            tag="ol",
            children=[
                LeafNode(tag="li", value="Item 1"),
                LeafNode(tag="li", value="Item 2"),
                LeafNode(tag="li", value="Item 3"),
            ],
        )
        result = ordered_list_block_to_html(block)

        self.assertEqual(result.to_html(), expected_node.to_html())

    def test_ordered_list_block_complex_data(self):
        block = "1. Item 1. 2.Stuff stuff stuff.\n2. Item 2\n3. Item 3"
        expected_node = ParentNode(
            tag="ol",
            children=[
                LeafNode(tag="li", value="Item 1. 2.Stuff stuff stuff."),
                LeafNode(tag="li", value="Item 2"),
                LeafNode(tag="li", value="Item 3"),
            ],
        )
        result = ordered_list_block_to_html(block)

        self.assertEqual(result.to_html(), expected_node.to_html())

    def test_unordered_list_block_to_html(self):
        block = "- Item 1\n- Item 2\n- Item 3"
        expected_node = ParentNode(
            tag="ul",
            children=[
                LeafNode(tag="li", value="Item 1"),
                LeafNode(tag="li", value="Item 2"),
                LeafNode(tag="li", value="Item 3"),
            ],
        )
        result = unordered_list_block_to_html(block)

        self.assertEqual(result.to_html(), expected_node.to_html())


class TestMarkdownBlockProcessing(TestCase):
    def test_markdown_to_blocks(self):
        markdown = "This is a test.\n\nThis is another test."
        expected_result = ["This is a test.", "This is another test."]
        self.assertEqual(markdown_to_blocks(markdown), expected_result)

    def test_is_quote(self):
        lines = ["> This is a quote."]
        self.assertTrue(is_quote(lines))

    def test_is_unordered_list(self):
        lines = ["- Item 1", "- Item 2"]
        self.assertTrue(is_unordered_list(lines))

    def test_is_ordered_list(self):
        lines = ["1. Item 1", "2. Item 2"]
        self.assertTrue(is_ordered_list(lines))

    def test_block_type_quote(self):
        block_quote = ["> Test."]

        result = block_to_block_type(block_quote)

        self.assertEqual(result, [BlockType.QUOTE])

    def test_multiple_blocks(self):
        blocks = ["This is a test.", "> This is a quote.", "- Item 1", "1. Item 1"]
        expected_result = [
            BlockType.PARAGRAPH,
            BlockType.QUOTE,
            BlockType.UNORDERED_LIST,
            BlockType.ORDERED_LIST,
        ]
        self.assertEqual(block_to_block_type(blocks), expected_result)

    def test_heading_block_to_html(self):
        block = "### Heading stuff"
        expected_node = LeafNode(tag="h1", value="Heading stuff")
        result = heading_block_to_html(block)

        self.assertEqual(result.to_html(), expected_node.to_html())

    def test_heading_block_to_html(self):
        block = "### Heading stuff"
        expected_node = LeafNode(tag="h3", value="Heading stuff")
        result = heading_block_to_html(block)

        self.assertEqual(result.to_html(), expected_node.to_html())

    def test_heading_block_to_html_edge_cases(self):
        block_h1 = "# Heading 1"
        expected_node_h1 = LeafNode(tag="h1", value="Heading 1")
        result_h1 = heading_block_to_html(block_h1)

        self.assertEqual(result_h1.to_html(), expected_node_h1.to_html())

        block_h6 = "###### Heading 6"
        expected_node_h6 = LeafNode(tag="h6", value="Heading 6")
        result_h6 = heading_block_to_html(block_h6)

        self.assertEqual(result_h6.to_html(), expected_node_h6.to_html())

    def test_quote_block_to_html(self):
        block = "> Potato\n> Tomato\n> Aristotle"
        expected_node = LeafNode(tag="blockquote", value="Potato\nTomato\nAristotle")
        result = quote_block_to_html(block)

        self.assertEqual(result.to_html(), expected_node.to_html())

    def test_ordered_list_block_to_html(self):
        block = "1. Item 1\n2. Item 2\n3. Item 3"
        expected_node = ParentNode(
            tag="ol",
            children=[
                LeafNode(tag="li", value="Item 1"),
                LeafNode(tag="li", value="Item 2"),
                LeafNode(tag="li", value="Item 3"),
            ],
        )
        result = ordered_list_block_to_html(block)

        self.assertEqual(result.to_html(), expected_node.to_html())

    def test_ordered_list_block_complex_data(self):
        block = "1. Item 1. 2.Stuff stuff stuff.\n2. Item 2\n3. Item 3"
        expected_node = ParentNode(
            tag="ol",
            children=[
                LeafNode(tag="li", value="Item 1. 2.Stuff stuff stuff."),
                LeafNode(tag="li", value="Item 2"),
                LeafNode(tag="li", value="Item 3"),
            ],
        )
        result = ordered_list_block_to_html(block)

        self.assertEqual(result.to_html(), expected_node.to_html())

    def test_unordered_list_block_to_html(self):
        block = "- Item 1\n- Item 2\n- Item 3"
        expected_node = ParentNode(
            tag="ul",
            children=[
                LeafNode(tag="li", value="Item 1"),
                LeafNode(tag="li", value="Item 2"),
                LeafNode(tag="li", value="Item 3"),
            ],
        )
        result = unordered_list_block_to_html(block)

        self.assertEqual(result.to_html(), expected_node.to_html())

    def test_markdown_to_html_node(self):  # Added test for the new function
        markdown = "This is a test.\n\nThis is another test."
        expected_node = ParentNode(
            tag="div",
            children=[
                LeafNode(tag="p", value="This is a test."),
                LeafNode(tag="p", value="This is another test."),
            ],
        )
        result = markdown_to_html_node(markdown)

        self.assertEqual(result.to_html(), expected_node.to_html())
