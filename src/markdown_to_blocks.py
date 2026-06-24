from enum import Enum
import re

class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"

def markdown_to_blocks(markdown: str) -> list[str]:
    split_markdown: list[str] = markdown.split("\n\n")
    filtered_blocks: list[str] = []
    for block in split_markdown:
        if block == "":
            continue
        block = block.strip()
        filtered_blocks.append(block)
    return filtered_blocks

def block_to_block_type(markdown: str) -> BlockType:
    if re.fullmatch(r"^#{1,6} [\s\S]*?", markdown):
        return BlockType.HEADING
    if re.fullmatch(r"```(\w*)\n[\s\S]*?```", markdown):
        return BlockType.CODE
    if re.fullmatch(r"(?:> ?[^\n]*(?:\n|$))+", markdown):
        return BlockType.QUOTE
    if re.fullmatch(r"(?:- [^\n]*(:?\n|$))+", markdown):
        return BlockType.UNORDERED_LIST
    if ordered_list_checker(markdown):
        return BlockType.ORDERED_LIST
    else:
        return BlockType.PARAGRAPH

def ordered_list_checker(markdown: str) -> bool:
    if len(markdown) == 0:
        return False
    if markdown[0] == "1" and markdown[1] == "." and markdown[2] == " ":
        current: int = 1
        for i in range(len(markdown)):
            if markdown[i] == "\n" and markdown[i + 1].isdigit() and markdown[i + 2] == ".":
                if int(markdown[i + 1]) == current + 1:
                    current += 1
                    continue
            elif markdown[i] != "\n":
                continue
            return False
        return True
    return False
