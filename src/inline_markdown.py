import re

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

def extract_markdown_images(text:str):
    pattern = r"!\[([^\[\]]*)\]\(([^\(\)]*)\)"
    return re.findall(pattern, text)

def extract_markdown_links(text:str):
    pattern = r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)"
    return re.findall(pattern, text)

def split_nodes_image(old_nodes: list):
    new_nodes = []
    for node in old_nodes:
        if node.text_type == TextType.TEXT:
            if not node.text:
                continue 
            images = extract_markdown_images(node.text)
            if not images:
                new_nodes.append(node)
                continue
            text = node.text
            for alt, url in images:
                split = text.split(f"![{alt}]({url})", 1)
                if split[0]:
                    new_nodes.append(TextNode(split[0], TextType.TEXT))
                new_nodes.append(TextNode(alt, TextType.IMAGE, url))
                text = split[1]
            if text:
                new_nodes.append(TextNode(text, TextType.TEXT))
        else:
            new_nodes.append(node)
    return new_nodes

def split_nodes_link(old_nodes: list):
    new_nodes = []
    for node in old_nodes:
        if node.text_type == TextType.TEXT:
            if not node.text:
                continue 
            links = extract_markdown_links(node.text)
            if not links:
                new_nodes.append(node)
                continue
            text = node.text
            for anchor, url in links:
                split = text.split(f"[{anchor}]({url})", 1)
                if split[0]:
                    new_nodes.append(TextNode(split[0], TextType.TEXT))
                new_nodes.append(TextNode(anchor, TextType.LINK, url))
                text = split[1]
            if text:
                new_nodes.append(TextNode(text, TextType.TEXT))
        else:
            new_nodes.append(node)
    return new_nodes

def text_to_textnodes(text: str):
    nodes = [TextNode(text, TextType.TEXT)]
    nodes = split_nodes_delimiter(split_nodes_delimiter(split_nodes_delimiter(nodes, "**", TextType.BOLD), "_", TextType.ITALIC), "`", TextType.CODE)
    return split_nodes_link(split_nodes_image(nodes))