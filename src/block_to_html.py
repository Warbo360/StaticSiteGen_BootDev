from extract_markdown import text_to_textnodes
from markdown_to_blocks import block_to_block_type, markdown_to_blocks, BlockType
from htmlnode import HTMLNode, LeafNode, ParentNode
from textnode import TextNode, text_node_to_html_node
import re

def markdown_to_html_node(markdown: str):
    markdown_blocks: list[str] = markdown_to_blocks(markdown)
    html_list: list[HTMLNode] = []
    for blocks in markdown_blocks:
        block_type = block_to_block_type(blocks)
        match block_type:
            case BlockType.HEADING:
                repl_block_heading: str = re.sub(r"#+? ", "", blocks)
                heading_node = ParentNode(md_heading_to_html_heading(blocks), text_to_children(repl_block_heading))
                html_list.append(heading_node)
            case BlockType.CODE:
                code_parent_node: ParentNode = ParentNode(
                    "pre",
                    [LeafNode("code", re.sub(r"```(?:\w*)?\n?", "", blocks))],
                )
                html_list.append(code_parent_node)
            case BlockType.QUOTE:
                repl_block_quote: str = blocks.replace("> ", "")
                quote_node = ParentNode("blockquote", text_to_children(repl_block_quote))
                html_list.append(quote_node)
            case BlockType.UNORDERED_LIST:
                ul_li_nodes: list[ParentNode] = list_builder(blocks, BlockType.UNORDERED_LIST)
                ul_block_node: ParentNode = ParentNode("ul", ul_li_nodes)
                html_list.append(ul_block_node)
            case BlockType.ORDERED_LIST:
                ol_li_nodes: list[ParentNode] = list_builder(blocks, BlockType.ORDERED_LIST)
                ordered_list_node = ParentNode("ol", ol_li_nodes)
                html_list.append(ordered_list_node)
            case BlockType.PARAGRAPH:
                paragraph_node = ParentNode("p", text_to_children(blocks.replace("\n", " ")))
                html_list.append(paragraph_node)
    div_node = ParentNode("div", html_list)
    return div_node

def text_to_children(text: str) -> list[HTMLNode]:
    textnodes: list[TextNode] = text_to_textnodes(text)
    html_nodes: list[HTMLNode] = []
    for node in textnodes:
        html_nodes.append(text_node_to_html_node(node))
    return html_nodes

def md_heading_to_html_heading(text: str) -> str:
    heading_total = 0
    for i in range(len(text)):
        if text[i] == "#":
            heading_total += 1
        else:
            break
    return f"h{heading_total}"

def list_builder(text: str, block_type: BlockType) -> list[ParentNode]:
    split_list_block: list[str] = []
    match block_type:
        case BlockType.UNORDERED_LIST:
            split_list_block = text.replace("- ", "").split("\n")
        case BlockType.ORDERED_LIST:
            remove_nums: str = re.sub(r"\d\. ", "", text)
            split_list_block = remove_nums.split("\n")
        case _:
            raise TypeError(f"Invalid passed BlockType in {block_type}")
    li_nodes: list[ParentNode] = []
    for li in split_list_block:
        li_nodes.append(ParentNode("li", text_to_children(li)))
    return li_nodes
