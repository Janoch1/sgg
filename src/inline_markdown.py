from textnode import TextNode, TextType
import re, textwrap

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
        else:
            if delimiter not in node.text:
                new_nodes.append(node)
            else:
                text_parts = node.text.split(delimiter)
                if len(text_parts) % 2 == 0:
                    raise Exception("Invalid markdown, missing closing delimiter")
                else:
                    for i in range (len(text_parts)):
                        part = text_parts[i]
                        if part == "":
                            continue
                        if i % 2 == 0:
                            new_nodes.append(TextNode(part, TextType.TEXT))
                        else:
                            new_nodes.append(TextNode(part, text_type))
    return new_nodes

def extract_markdown_images(text):
    matches = re.findall( r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
    return matches

def extract_markdown_links(text):
    matches = re.findall( r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
    return matches

def split_nodes_image(old_nodes):
    new_nodes = []
    for node in old_nodes:
        extract_list = extract_markdown_images(node.text)
        if len(extract_list) == 0:
            new_nodes.append(node)
            continue
        original_text = node.text
        for image in extract_list:
            sections = original_text.split(f"![{image[0]}]({image[1]})", 1)
            if len(sections) != 2:
                raise ValueError("invalid markdown, image section not closed")
            if sections[0] != "":
                new_nodes.append(TextNode(sections[0], TextType.TEXT))
            new_nodes.append(TextNode(image[0], TextType.IMAGE, image[1]) )
            original_text = sections[1]
        if original_text != "":
            new_nodes.append(TextNode(original_text, TextType.TEXT))
    return new_nodes
        

def split_nodes_link(old_nodes):
    new_nodes = []
    for node in old_nodes:
        extract_list = extract_markdown_links(node.text)
        if len(extract_list) == 0:
            new_nodes.append(node)
            continue
        original_text = node.text
        for link in extract_list:
            sections = original_text.split(f"[{link[0]}]({link[1]})", 1)
            if len(sections) != 2:
                raise ValueError("invalid markdown, image section not closed")
            if sections[0] != "":
                new_nodes.append(TextNode(sections[0], TextType.TEXT))
            new_nodes.append(TextNode(link[0], TextType.LINK, link[1]) )
            original_text = sections[1]
        if original_text != "":
            new_nodes.append(TextNode(original_text, TextType.TEXT))
    return new_nodes
        
def text_to_textnodes(text):
    nodes = [TextNode(text, TextType.TEXT)]
    nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD)
    nodes = split_nodes_delimiter(nodes, "_", TextType.ITALIC)
    nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)
    nodes = split_nodes_image(nodes)
    nodes = split_nodes_link(nodes)
    return nodes

