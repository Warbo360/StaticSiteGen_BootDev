from extract_markdown import text_to_textnodes
from markdown_to_blocks import block_to_block_type, markdown_to_blocks, BlockType
from htmlnode import HTMLNode, ParentNode
from textnode import TextNode, text_node_to_html_node, TextType

def markdown_to_html_node(markdown: str):
    markdown_blocks: list[str] = markdown_to_blocks(markdown)
    html_list: list[HTMLNode] = []
    for blocks in markdown_blocks:
        block_type = block_to_block_type(blocks)
        match block_type:
            case BlockType.HEADING:
                heading_node = ParentNode("h", text_to_children(blocks))
                html_list.append(heading_node)
            case BlockType.CODE:
                code_text_node = TextNode(blocks, TextType.CODE)
                code_html_node = text_node_to_html_node(code_text_node)
                html_list.append(code_html_node)
            case BlockType.QUOTE:
                quote_node = ParentNode("q", text_to_children(blocks))
                html_list.append(quote_node)
            case BlockType.UNORDERED_LIST:
                unordered_list_node = ParentNode("ul", text_to_children(blocks))
                html_list.append(unordered_list_node)
            case BlockType.ORDERED_LIST:
                ordered_list_node = ParentNode("ol", text_to_children(blocks))
                html_list.append(ordered_list_node)
            case BlockType.PARAGRAPH:
                paragraph_node = ParentNode("p", text_to_children(blocks))
                html_list.append(paragraph_node)
    div_node = ParentNode("div", html_list)
    return div_node

def text_to_children(text: str) -> list[HTMLNode]:
    textnodes: list[TextNode] = text_to_textnodes(text)
    html_nodes: list[HTMLNode] = []
    for node in textnodes:
        html_nodes.append(text_node_to_html_node(node))
    return html_nodes

