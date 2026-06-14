from __future__ import annotations
from typing import override

class HTMLNode():
    def __init__(
        self,
        tag: str | None = None,
        value: str | None = None,
        children: list[HTMLNode] | None = None,
        props: dict[str, str] | None = None
    ) -> None:
        self.tag: str | None = tag
        self.value: str | None = value
        self.children: list[HTMLNode] | None = children
        self.props: dict[str, str] | None = props

    def to_html(self) -> None | str:
        raise NotImplementedError

    def props_to_html(self):
        if self.props:
            props = ""
            for attributes in self.props:
                props += f" {attributes}=\"{self.props[attributes]}\""
            return props
        return ""

    @override
    def __repr__(self) -> str:
        return f"HTMLNode({self.tag}, {self.value}, {self.children}, {self.props}) "

class LeafNode(HTMLNode):
    def __init__(self, tag: str | None, value: str, props: dict[str, str] | None = None) -> None:
        super().__init__(tag, value, None, props)

    @override
    def to_html(self) -> str:
        if self.value is None:
            raise ValueError("All leaf nodes must have a value")
        if self.tag is None:
            return f"{self.value}"
        return f"<{self.tag}>{self.value}</{self.tag}>"

    @override
    def __repr__(self) -> str:
        return f"LeafNode({self.tag}, {self.value}, {self.props})"

class ParentNode(HTMLNode):
    def __init__(self, tag: str, children: list[HTMLNode], props: dict[str , str] | None = None) -> None:
        super().__init__(tag, None, children, props)

    @override
    def to_html(self, index: int = 0) -> str:
        if self.tag is None:
            raise ValueError("Invalid HTML: no tag")
        if self.children is None:
            raise ValueError("Invalid HTML: no children for ParentNode")
        children: str = ""
        for child in self.children:
            children += child.to_html()
        return f"<{self.tag}>" + children + f"</{self.tag}>"
