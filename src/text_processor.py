import re
from textnode import TextNode, TextType
from htmlnode import LeafNode


IMAGES_REGEX = r"!\[(.*?)\]\((.*?)\)"
LINKS_REGEX = r"\[(.*?)\]\((.*?)\)"


class Delimeters:
    CODE = "`"
    ITALIC = "*"
    BOLD = "**"


def extract_markdown_images(text_node: TextNode):
    return re.findall(IMAGES_REGEX, text_node.text)


def extract_markdown_links(text_node: TextNode):
    return re.findall(LINKS_REGEX, text_node.text)


def split_nodes_delimiter(old_nodes, delimiter):
    new_nodes = []
    for node in old_nodes:
        tmp_list = []

        if node.text_type == TextType.TEXT:
            pieces = node.text.split(delimiter, 2)
            if len(pieces) < 3:
                new_nodes.append(node)
            else:
                if pieces[0] != "":
                    tmp_list.append(TextNode(pieces[0], TextType.TEXT))

                if delimiter == Delimeters.BOLD:
                    tmp_list.append(TextNode(pieces[1], TextType.BOLD))
                elif delimiter == Delimeters.CODE:
                    tmp_list.append(TextNode(pieces[1], TextType.CODE))
                elif delimiter == Delimeters.ITALIC:
                    tmp_list.append(TextNode(pieces[1], TextType.ITALIC))
                else:
                    raise ValueError("Unknown delimeter type")

                if pieces[2] != "":
                    tmp_list.append(TextNode(pieces[2], TextType.TEXT))

        else:
            new_nodes.append(node)

        new_nodes.extend(tmp_list)

    return new_nodes


def split_nodes_image(old_nodes):
    result = []
    for node in old_nodes:
        if node.text_type == TextType.TEXT:
            image_elements = extract_markdown_images(node)
            if image_elements:
                inline_text = node.text
                for im in image_elements:
                    image_md_text = f"![{im[0]}]({im[1]})"
                    text_pieces = inline_text.split(image_md_text, 1)  # split once only
                    if text_pieces[0] != "":
                        result.append(TextNode(text_pieces[0], TextType.TEXT))
                        result.append(
                            TextNode(text=im[0], text_type=TextType.IMAGE, url=im[1])
                        )
                    elif text_pieces[1] != "":
                        result.append(
                            TextNode(text=im[0], text_type=TextType.IMAGE, url=im[1])
                        )
                        result.append(
                            TextNode(text=text_pieces[1], text_type=TextType.TEXT)
                        )
                    else:
                        result.append(
                            TextNode(text=im[0], text_type=TextType.IMAGE, url=im[1])
                        )

                    inline_text = text_pieces[1]
                if inline_text != "":
                    result.append(TextNode(text=inline_text, text_type=TextType.TEXT))
            else:
                result.append(node)
        else:
            result.append(node)

    return result


def split_nodes_links(old_nodes):
    result = []
    for node in old_nodes:
        if node.text_type == TextType.TEXT:
            image_elements = extract_markdown_links(node)
            if image_elements:
                inline_text = node.text
                for im in image_elements:
                    image_md_text = f"[{im[0]}]({im[1]})"
                    text_pieces = inline_text.split(image_md_text, 1)  # split once only
                    if text_pieces[0] != "":
                        result.append(TextNode(text_pieces[0], TextType.TEXT))
                        result.append(
                            TextNode(text=im[0], text_type=TextType.LINK, url=im[1])
                        )
                    elif text_pieces[1] != "":
                        result.append(
                            TextNode(text=im[0], text_type=TextType.LINK, url=im[1])
                        )
                        result.append(
                            TextNode(text=text_pieces[1], text_type=TextType.TEXT)
                        )
                    else:
                        result.append(
                            TextNode(text=im[0], text_type=TextType.LINK, url=im[1])
                        )

                    inline_text = text_pieces[1]
                if inline_text != "":
                    result.append(TextNode(text=inline_text, text_type=TextType.TEXT))
            else:
                result.append(node)
        else:
            result.append(node)

    return result


def _generate_text_node(text_node: TextNode):
    return LeafNode(value=text_node.text)


def _generate_link_node(text_node: TextNode):
    return LeafNode(tag="a", value=text_node.text, props={"href": text_node.url})


def _generate_code_node(text_node: TextNode):
    return LeafNode(tag="code", value=text_node.text)


def _generate_italic_node(text_node: TextNode):
    return LeafNode(tag="i", value=text_node.text)


def _generate_bold_node(text_node: TextNode):
    return LeafNode(tag="b", value=text_node.text)


def _generate_image_node(text_node: TextNode):
    return LeafNode(
        tag="img", value=" ", props={"src": text_node.url, "alt": text_node.text}
    )


def text_node_to_html_node(text_node: TextNode):
    if text_node.text_type == TextType.TEXT:
        return _generate_text_node(text_node)
    elif text_node.text_type == TextType.BOLD:
        return _generate_bold_node(text_node)
    elif text_node.text_type == TextType.ITALIC:
        return _generate_italic_node(text_node)
    elif text_node.text_type == TextType.CODE:
        return _generate_code_node(text_node)
    elif text_node.text_type == TextType.LINK:
        return _generate_link_node(text_node)
    elif text_node.text_type == TextType.IMAGE:
        return _generate_image_node(text_node)
    else:
        raise ValueError("Unsupported text type")


def text_to_textnodes(text: str):
    nodes = [TextNode(text=text, text_type=TextType.TEXT)]
    nodes = split_nodes_delimiter(nodes, Delimeters.BOLD)
    nodes = split_nodes_delimiter(nodes, Delimeters.ITALIC)
    nodes = split_nodes_delimiter(nodes, Delimeters.CODE)
    nodes = split_nodes_image(nodes)
    nodes = split_nodes_links(nodes)
    return nodes


def text_to_html(text):
    nodes = text_to_textnodes(text)
    return [text_node_to_html_node(n) for n in nodes]
