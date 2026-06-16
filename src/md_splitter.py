from textnode import TextNode, TextType

def split_nodes_delimiter(old_nodes: list[TextNode], delimiter: str, text_type: TextType) -> list[TextNode]:
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type is not TextType.PLAIN:
            new_nodes.append(old_node)
            continue

        temp: list[TextNode] = []

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
