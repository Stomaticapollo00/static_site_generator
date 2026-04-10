import re
from enum import Enum

class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    U_LIST = "unordered list"
    O_LIST = "ordered list"

def markdown_to_blocks(markdown):
    return [
        clean_block
        for block in markdown.split("\n\n")
        if (clean_block := block.strip()) != ""
    ]

def block_to_blocktype(block):
    lines = block.split("\n")
    if re.match(r"^#{1,6} ", block):
        return BlockType.HEADING
    if block.startswith("```") and block.endswith("```"):
        return BlockType.CODE
    if all(line.startswith(">") for line in lines):
        return BlockType.QUOTE
    if all(re.match(r"^[-*] ", line) for line in lines):
        return BlockType.U_LIST
    if all(line.startswith(f"{i}. ") for i, line in enumerate(lines, 1)):
        return BlockType.O_LIST
    return BlockType.PARAGRAPH
    
    