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
    def __init__(self, tag: str | None, value: str, children: None = None, props: dict[str, str] | None = None) -> None:
        super().__init__(tag, value, None, props)
        if children is not None:
            raise ValueError("LeafNode is not allowed to have children nodes")

    @override
    def to_html(self) -> str:
        if not self.value:
            raise ValueError("All leaf nodes must have a value")
        if not self.tag:
            return f"{self.value}"
        return f"<{self.tag}>{self.value}</{self.tag}>"

    @override
    def __repr__(self) -> str:
        return f"LeafNode({self.tag}, {self.value}, {self.props})"
