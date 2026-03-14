import re

from enum import Enum

class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"

def block_to_block_type(block: str):
    if bool(re.match(r'^#{1,6} ', block)) and "\n" not in block:
        return BlockType.HEADING
    elif block.startswith("```\n") and block.endswith("```"):
        return BlockType.CODE
    elif is_quote_block(block):
        return BlockType.QUOTE
    elif is_unordered_list_block(block):
        return BlockType.UNORDERED_LIST
    elif is_ordered_list_block(block):
        return BlockType.ORDERED_LIST
    else:
        return BlockType.PARAGRAPH

def is_quote_block(block: str):
    lines = block.split("\n")
    return all(line.startswith(">") for line in lines)

def is_unordered_list_block(block: str):
    lines = block.split("\n")
    return all(line.startswith("- ") for line in lines)

def is_ordered_list_block(block: str):
    lines = block.split("\n")
    for i, line in enumerate(lines):
        if not line.startswith(f"{i+1}. "):
            return False
    return True

def markdown_to_blocks(markdown: str):
    blocks = markdown.split("\n\n")
    return [block.strip() for block in blocks if block.strip()]