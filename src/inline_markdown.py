from textnode import TextNode, TextType

def split_nodes_delimiter(old_nodes: list, deliminiter: str, text_type: TextType):
    new_nodes = []
    for node in old_nodes:
        if node.text_type == TextType.TEXT:
            split = node.text.split(deliminiter)
            if len(split) % 2 == 0:
                raise ValueError("invalid markdown: missing closing deliminiter")
            for i, part in enumerate(split):
                if part == "":
                    continue
                if i % 2 == 0:
                    new_nodes.append(TextNode(part, TextType.TEXT))
                else:
                    new_nodes.append(TextNode(part, text_type))
        else:
            new_nodes.append(node)
    return new_nodes
