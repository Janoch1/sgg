from enum import Enum
from htmlnode import HTMLNode, text_node_to_html_node, ParentNode, LeafNode
from inline_markdown import text_to_textnodes
from textnode import TextNode, TextType

class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"


def markdown_to_blocks(markdown):
    blocks = markdown.split("\n\n")
    filtered_blocks = []
    for block in blocks:
        block = block.strip()
        if block == "":
            continue
        filtered_blocks.append(block)
    return filtered_blocks

def block_to_block_type(markdown):
    for i in range(1,7):
        if markdown.startswith("#" * i + ' '):
            return BlockType.HEADING
    
    if markdown.startswith("```\n") and markdown.endswith("```"):
        return BlockType.CODE
    lines = markdown.split("\n")
    is_quote = True 
    for line in lines:
        if not line.startswith(">"):
            is_quote = False
            break
    if is_quote:
        return BlockType.QUOTE
    is_unordered = True
    for line in lines:
        if not line.startswith("- "):
            is_unordered = False
            break
    if is_unordered:
        return BlockType.UNORDERED_LIST
    is_ordered = True
    for index, line in enumerate(lines):
        expected = f"{index + 1}. "
        if not line.startswith(expected):
            is_ordered = False
            break
    if is_ordered:
        return BlockType.ORDERED_LIST
    else:
        return BlockType.PARAGRAPH

def tag_identify(block_type, block):
    if block_type == BlockType.HEADING:
        return heading_tag_from_block(block)
    if block_type == BlockType.CODE:
        return "code"
    if block_type == BlockType.QUOTE:
        return "blockquote"
    if block_type == BlockType.UNORDERED_LIST:
        return "ul"
    if block_type == BlockType.ORDERED_LIST:
        return "ol"
    if block_type == BlockType.PARAGRAPH:
        return "p"

def heading_tag_from_block(block:str) -> str:
    level = 0
    for ch in block:
        if ch == "#":
            level += 1
        else:
            break
    return f"h{level}"

def block_inner_text(block_type, block: str) -> str:
    if block_type == BlockType.HEADING:
        i = 0
        while i < len(block) and block[i] == "#":
            i += 1
        if  i < len(block) and block[i] == " ":
            i += 1
        return block[i:]

    elif block_type == BlockType.QUOTE:
        if block.startswith("> "):
            return block[2:]
        else:
            return block
    else:
        return block

def code_block_inner_text(block: str) -> str:
    # block looks like: "```\n...code...\n```"
    lines = block.split("\n")
    # drop first and last line (the ``` markers)
    inner_lines = lines[1:-1]
    return "\n".join(inner_lines) + "\n"
    
def list_item_text(block_type, block:str) -> list[str]:
    lines = block.split("\n")
    items = []
    for line in lines:
        stripped = line.strip()
        if not stripped:
            continue

        if block_type == BlockType.UNORDERED_LIST:
            if stripped.startswith("- "):
                items.append(stripped[2:])
            elif stripped.startswith("* "):
                items.append(stripped[2:])
        
        if block_type == BlockType.ORDERED_LIST:
            i = 0
            while i < len(stripped) and stripped[i].isdigit():
                i += 1
            if i < len(stripped) - 1 and stripped[i] == "." and stripped[i+1] == " ":
                items.append(stripped[i+2:])
    return items

def text_to_children(text: str) -> list[HTMLNode]:
    # 1. text_to_textnodes is whatever you named your inline parser
    text_nodes = text_to_textnodes(text)
    # 2. Convert each text node to HTMLNode
    children = []
    for tn in text_nodes:
        child = text_node_to_html_node(tn)
        children.append(child)
    return children


    
def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    children = []
    for block in blocks:
        block_type = block_to_block_type(block)
        if block_type in(BlockType.HEADING, BlockType.QUOTE):
            tag = tag_identify(block_type, block)
            inner = block_inner_text(block_type, block)
            inline_children = text_to_children(inner)
            children.append(ParentNode(tag=tag, children=inline_children))
        elif block_type == BlockType.PARAGRAPH:
            text = " ".join(block.split())
            inline_children = text_to_children(text)
            children.append(ParentNode("p", inline_children))
            continue
        elif block_type in (BlockType.UNORDERED_LIST, BlockType.ORDERED_LIST):
            tag = tag_identify(block_type, block)
            items = list_item_text(block_type, block)
            li_nodes = []
            for item_text in items:
                li_children = text_to_children(item_text)
                li_nodes.append(ParentNode(tag = "li", children= li_children))
            children.append(ParentNode(tag=tag, children=li_nodes))
        elif block_type == BlockType.CODE:
            code_text = code_block_inner_text(block)

            code_child = text_node_to_html_node(TextNode(code_text,TextType.TEXT ))
            code_node = ParentNode(tag = "code", children=[code_child])
            node = ParentNode(tag = "pre", children= [code_node])
            children.append(node)
    return ParentNode(tag="div", children=children)


