from htmlnode import LeafNode, ParentNode
from text_processor import text_to_textnodes, text_node_to_html_node, text_to_html


class BlockType:
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"


def markdown_to_blocks(markdown):
    blocks = markdown.split("\n\n")
    filtered_blocks = []
    for block in blocks:
        if block == "":
            continue
        block = block.strip()
        filtered_blocks.append(block)
    return filtered_blocks


def is_quote(lines):
    for l in lines:
        if not l.startswith("> "):
            return False

    return True


def is_unordered_list(lines):
    lead = lines[0][0]
    if lead in ("-", "."):
        for l in lines:
            if not l.startswith(lead + " "):
                return False

        return True

    return False


def is_ordered_list(lines):
    n = len(lines)
    if n < 1:
        return False
    for i in range(n):
        if not lines[i].startswith(str(i + 1) + ". "):
            return False

    return True


def block_to_block_type(blocks):
    block_types = []
    for block in blocks:
        if block.startswith(("# ", "## ", "### ", "#### ", "##### ", "###### ")):
            block_types.append(BlockType.HEADING)
        elif block.startswith("```") and block.endswith("```"):
            block_types.append(BlockType.CODE)
        elif is_ordered_list(block.split("\n")):
            block_types.append(BlockType.ORDERED_LIST)
        elif is_unordered_list(block.split("\n")):
            block_types.append(BlockType.UNORDERED_LIST)
        elif is_quote(block.split("\n")):
            block_types.append(BlockType.QUOTE)
        else:
            block_types.append(BlockType.PARAGRAPH)

    return block_types


def heading_block_to_html(block):
    heading_depth = 0
    for c in block:
        if c == "#":
            heading_depth += 1
        else:
            break
    heading_content = block.lstrip("#" * heading_depth + " ")
    childs = text_to_html(heading_content)

    return ParentNode(tag="h" + str(heading_depth), children=childs)


def code_block_to_html(block):
    code_content = block.lstrip("```\n")
    code_content = code_content.rstrip("```\n")
    code_block = LeafNode(tag="code", value=code_content)

    return ParentNode(tag="pre", value=None, children=[code_block])


def quote_block_to_html(block):
    quote_lines = block.split("\n")
    quote_block_sanitized = []
    for line in quote_lines:
        quote_block_sanitized.append(line.lstrip("> "))
    quote = "\n".join(quote_block_sanitized)
    childs = text_to_html(quote)

    return ParentNode(tag="blockquote", children=childs)


def unordered_list_block_to_html(block):
    block_lines = block.split("\n")
    list_elements = []
    for l in block_lines:
        if l.startswith("- "):
            lval = l.lstrip("- ")
            childs = text_to_html(lval)
        elif l.startswith("* "):
            lval = l.lstrip("* ")
            childs = text_to_html(lval)

        list_elements.append(ParentNode(tag="li", children=childs))

    return ParentNode(tag="ul", children=list_elements)


def _extract_ordered_list_content(element):
    c = element.split(".")
    return ".".join(c[1:]).lstrip(" ")


def ordered_list_block_to_html(block):
    block_lines = block.split("\n")
    list_elements = []
    for l in block_lines:
        v = _extract_ordered_list_content(l)
        childs = text_to_html(v)
        list_elements.append(ParentNode(tag="li", children=childs))

    return ParentNode(tag="ol", children=list_elements)


def paragraph_block_to_html(block):
    nodes = text_to_textnodes(block)
    html_nodes = [text_node_to_html_node(t) for t in nodes]

    return ParentNode(tag="p", children=html_nodes)


def blocks_to_html(blocks):
    block_types = block_to_block_type(blocks)
    html_nodes = []

    for i in range(len(blocks)):
        if block_types[i] == BlockType.HEADING:
            html_nodes.append(heading_block_to_html(blocks[i]))
        elif block_types[i] == BlockType.CODE:
            html_nodes.append(code_block_to_html(blocks[i]))
        elif block_types[i] == BlockType.QUOTE:
            html_nodes.append(quote_block_to_html(blocks[i]))
        elif block_types[i] == BlockType.ORDERED_LIST:
            html_nodes.append(ordered_list_block_to_html(blocks[i]))
        elif block_types[i] == BlockType.UNORDERED_LIST:
            html_nodes.append(unordered_list_block_to_html(blocks[i]))
        else:
            html_nodes.append(paragraph_block_to_html(blocks[i]))

    return html_nodes


def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    inline_nodes = blocks_to_html(blocks)

    return ParentNode(tag="div", children=inline_nodes)
