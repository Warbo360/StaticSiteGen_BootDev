from md_splitter import split_nodes_delimiter
from extract_markdown import split_nodes_image, split_nodes_link
from textnode import TextNode, TextType

def text_to_textnodes(text: str) -> list[TextNode]:
    if not isinstance(text, str):
        raise TypeError("Type string is only type accepted for text_to_textnodes()")
    input_node = TextNode(text, TextType.PLAIN)
    output_nodes: list[TextNode] = []

    # Need initial builder to start output_nodes but then each one after just takes output_nodes as input

    output_nodes = split_nodes_delimiter([input_node], "**", TextType.BOLD)
    output_nodes = split_nodes_delimiter(output_nodes, "_", TextType.ITALIC)
    output_nodes = split_nodes_delimiter(output_nodes, "`", TextType.CODE)
    output_nodes = split_nodes_image(output_nodes)
    output_nodes = split_nodes_link(output_nodes)

    return output_nodes
