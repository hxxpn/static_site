class TextType:
    BOLD = "bold"
    ITALIC = "italic"
    TEXT = "text"
    CODE = "code"
    LINK = "link"
    IMAGE = "image"


class TextNode:
    def __init__(self, text: str, text_type: TextType, url: str = None) -> None:
        self.text = text
        self.text_type = text_type
        self.url = url

    def __eq__(self, __value: object) -> bool:
        return (
            self.url == __value.url
            and self.text == __value.text
            and self.text_type == __value.text_type
        )

    def __repr__(self) -> str:
        return f"TextNode({self.text=}, {self.text_type=}, {self.url=})"
