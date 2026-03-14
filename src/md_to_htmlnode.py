from markdown_blocks import BlockType, markdown_to_blocks, block_to_block_type
from htmlnode import LeafNode, ParentNode
from inline_markdown import text_to_textnodes
from textnode import text_node_to_html_node

def markdown_to_html_node(markdown: str):
    blocks = markdown_to_blocks(markdown)
    children_list = []
    
    for block in blocks:
        match block_to_block_type(block):
            case BlockType.PARAGRAPH:
                block = block.replace("\n", " ")
                children_list.append(ParentNode("p", text_to_children(block)))
            case BlockType.HEADING:
                count, block = heading_count(block)
                children_list.append(ParentNode(f"h{count}", text_to_children(block)))
            case BlockType.CODE:
                children_list.append(ParentNode("pre", [LeafNode("code", block[4:-3])]))
            case BlockType.QUOTE:
                block = process_quote(block)
                children_list.append(ParentNode("blockquote", text_to_children(block)))
            case BlockType.UNORDERED_LIST:
                lines = process_unordered_list(block)
                children_list.append(ParentNode("ul", [ParentNode("li", text_to_children(line)) for line in lines]))
            case BlockType.ORDERED_LIST:
                lines = process_ordered_list(block)
                children_list.append(ParentNode("ol", [ParentNode("li", text_to_children(line)) for line in lines]))
    return ParentNode("div", children_list)

def text_to_children(text: str):
    return [text_node_to_html_node(node) for node in text_to_textnodes(text)]

def heading_count(text: str):
    count = 0
    for char in text:
        if char == "#":
            count += 1
        else:
            break
    return count, text[count+1:]

def process_quote(text: str):
    lines = text.split("\n")
    new_lines = []
    for line in lines:
        new_lines.append(line.lstrip(">").strip())
    return "\n".join(new_lines)

def process_ordered_list(text: str):
    lines = text.split("\n")
    new_lines = []
    for line in lines:
        new_lines.append(line.lstrip("0123456789.").strip())
    return new_lines

def process_unordered_list(text: str):
    lines = text.split("\n")
    new_lines = []
    for line in lines:
        new_lines.append(line.lstrip("-").strip())
    return new_lines