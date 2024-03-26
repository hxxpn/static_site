class HTMLNode:
    def __init__(
        self, tag: str = None, value: str = None, children=None, props: dict = None
    ) -> None:
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def __repr__(self) -> str:
        return f"HTMLNode({self.tag}, {self.value}, {self.children}, {self.props})"

    def to_html(self):
        raise NotImplemented()

    def props_to_html(self):
        props_string = ""
        for k, v in self.props.items():
            props_string += f' {k}="{v}"'

        return props_string

    def _create_opening_ang_closing_tags(self):
        tag_const_close = f"</{self.tag}>"
        if self.props is None or self.props == {}:
            tag_const_open = f"<{self.tag}>"
        else:
            tag_const_open = f"<{self.tag}{self.props_to_html()}>"

        return tag_const_open, tag_const_close


class LeafNode(HTMLNode):
    def __init__(
        self,
        tag: str = None,
        value: str = None,
        children: HTMLNode = None,
        props: dict = None,
    ) -> None:
        if not value:
            raise ValueError("Missing node value")
        super().__init__(tag, value, children, props)

    def to_html(self):
        if not self.tag:
            return self.value

        tag_open, tag_close = self._create_opening_ang_closing_tags()

        return tag_open + self.value + tag_close


class ParentNode(HTMLNode):
    def __init__(
        self,
        tag: str = None,
        value: str = None,
        children: HTMLNode = None,
        props: dict = None,
    ) -> None:
        if tag is None:
            raise ValueError("Missing tag for node")
        elif children is None:
            raise ValueError("Missing children nodes")
        elif value is not None:
            raise ValueError("Value added when it should be none")

        super().__init__(tag, value, children, props)

    def to_html(self):
        tag_open, tag_close = self._create_opening_ang_closing_tags()

        children_content = ""
        for child in self.children:
            children_content += child.to_html()

        return tag_open + children_content + tag_close
