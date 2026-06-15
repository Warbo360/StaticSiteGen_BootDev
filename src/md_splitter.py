from enum import Enum
from textnode import TextNode, TextType

class MDDelimiter(Enum):
    ITALIC = "_"
    BOLD = "**"
    CODE = "`"

def split_nodes_delimiter(old_nodes: list[TextNode], delimiter: str, text_type: TextType) -> list[TextNode]:
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type is not TextType.PLAIN:
            new_nodes.append(old_node)
        if delimiter in old_node.text:
            split_node = old_node.text.split(delimiter)
            if len(split_node) % 2 == 0:
                raise ValueError(f"{old_node} has odd number of \"{delimiter}\" and thus is not valid markdown")
                         


