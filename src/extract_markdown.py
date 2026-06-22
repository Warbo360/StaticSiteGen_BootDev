import re
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

def extract_markdown_images(text: str) -> list[tuple[str, str]]:

    # regex to pull inline images from markdown text, regex reads as staring with an exlamantion point, left bracket,
    # then capture group which can be anything but brackets, forward slashes zero to multiple times, then after that
    # capture group left bracket, right parens, 2nd capture group which excludes parens, brackets, and whitespace.
    # Should re-work for filepaths (which would allow whitespace) if needed. That group atleast 1 of more times then
    # ending in a right parens
    # Example pattern to be matched: ![alt-text](https:www.somelinktoanimage.png)
    # will return matches as a list of tuples each tuple being (alt-text, url) matches found in the passed text

    return re.findall(r"!\[([^\[\]\\]*?)\]\(([^\(\)\[\]\s]+?)\)", text)

def extract_markdown_links(text: str) -> list[tuple[str, str]]:

    # Same as above but uses a behind lookaround for an "!" to be sure it is not an inline image, and is just a link in
    # markdown, also returns as a list of tuples in the same format as above

    return re.findall(r"(?<!!)\[([^\[\]\\]+?)\]\(([^\(\)\[\]\s]+?)\)", text)

def split_nodes_image(old_nodes: list[TextNode]) -> list[TextNode]:
    if len(old_nodes) == 0 or not isinstance(old_nodes, list):
        raise TypeError(f"Empty list passed when only list of TextNode are accepted")
    new_nodes: list[TextNode] = []
    for old_node in old_nodes:
        if not isinstance(old_node, TextNode):
            raise TypeError(f"List element is not of type TextNode")
        extracts: list[tuple[str, str]] = extract_markdown_images(old_node.text)
        if len(extracts) == 0:
            new_nodes.append(old_node)
            continue
        temp_node_list: list[TextNode] = []
        not_extracted_yet: str = old_node.text
        for extract in extracts:
            split_old_nodes = not_extracted_yet.split(f"![{extract[0]}]({extract[1]})", 1)
            if split_old_nodes[0] == "":
                temp_node_list.append(TextNode(extract[0], TextType.IMAGE, extract[1]))
                not_extracted_yet = split_old_nodes[1]
                continue
            temp_node_list.append(TextNode(split_old_nodes[0], TextType.PLAIN))
            temp_node_list.append(TextNode(extract[0], TextType.IMAGE, extract[1]))
            not_extracted_yet = split_old_nodes[1]
        if not_extracted_yet != "":
            temp_node_list.append(TextNode(not_extracted_yet, TextType.PLAIN))
        new_nodes.extend(temp_node_list)
    return new_nodes

def split_nodes_link(old_nodes: list[TextNode]) -> list[TextNode]:
    if len(old_nodes) == 0 or not isinstance(old_nodes, list):
        raise TypeError(f"Empty list passed when only list of TextNode are accepted")
    new_nodes: list[TextNode] = []
    for old_node in old_nodes:
        if not isinstance(old_node, TextNode):
            raise TypeError(f"List element is not of type TextNode")
        extracts: list[tuple[str, str]] = extract_markdown_links(old_node.text)
        if len(extracts) == 0:
            new_nodes.append(old_node)
            continue
        temp_node_list: list[TextNode] = []
        not_extracted_yet: str = old_node.text
        for extract in extracts:
            split_old_nodes = not_extracted_yet.split(f"[{extract[0]}]({extract[1]})", 1)
            if split_old_nodes[0] == "":
                temp_node_list.append(TextNode(extract[0], TextType.LINK, extract[1]))
                not_extracted_yet = split_old_nodes[1]
                continue
            temp_node_list.append(TextNode(split_old_nodes[0], TextType.PLAIN))
            temp_node_list.append(TextNode(extract[0], TextType.LINK, extract[1]))
            not_extracted_yet = split_old_nodes[1]
        if not_extracted_yet != "":
            temp_node_list.append(TextNode(not_extracted_yet, TextType.PLAIN))
        new_nodes.extend(temp_node_list)
    return new_nodes

def split_nodes_delimiter(old_nodes: list[TextNode], delimiter: str, text_type: TextType) -> list[TextNode]:
    new_nodes: list[TextNode] = []
    for old_node in old_nodes:
        if old_node.text_type is not TextType.PLAIN:
            new_nodes.append(old_node)
            continue

        temp: list[TextNode] = []

        # Only difference between solution and mine was instead of checking for delimiter in the old_node
        # theirs just goes straight to splitting them at the delimiter and if presumably there are none,
        # they never get split and thus just get added to new_nodes just as is, not sure if it makes a huge difference
        # besdies readability possibly, since they enter as plain text they all get checked regardless so nothing gets
        # missed really and the initial check can get around all the other check and go straigh to else... something to
        # think about still I suppose

        if delimiter in old_node.text:
            split_old_node = old_node.text.split(delimiter)
            if len(split_old_node) % 2 == 0:
                raise ValueError(f"{old_node} has unmatched number of delimiter: \"{delimiter}\"")
            for i in range(len(split_old_node)):
                if split_old_node[i] == "":
                    continue
                if i % 2 == 0:
                    temp.append(TextNode(split_old_node[i], TextType.PLAIN))
                else:
                    temp.append(TextNode(split_old_node[i], text_type))
            new_nodes.extend(temp)
        else:
            new_nodes.append(old_node)
    return new_nodes
