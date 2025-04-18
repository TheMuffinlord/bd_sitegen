from textnode import *
from htmlnode import *

import re

def text_node_to_html_node(text_node): #chapter 2 lesson 6
    match(text_node.text_type):
        case TextType.TEXT:
            return LeafNode(None, text_node.text)
        case TextType.BOLD:
            return LeafNode("b", text_node.text)
        case TextType.ITALIC:
            return LeafNode("i", text_node.text)
        case TextType.CODE:
            return LeafNode("code", text_node.text)
        case TextType.LINK:
            return LeafNode("a", text_node.text, {"href":text_node.url})
        case TextType.IMAGE:
            return LeafNode("img",None, props={"src":text_node.url,"alt":text_node.text})
        case _:
            return LeafNode()

def split_nodes_delimiter(old_nodes, delimiter, text_type): #chapter 3 lesson 1
    node_list = []
    for node in old_nodes:
        old_text = node.text
        old_type = node.text_type
        if delimiter in old_text:
            if old_text.count(delimiter) != 2:
                raise Exception("invalid markdown syntax")
            if old_type.value == "text":
                split_text = old_text.split(delimiter)
                if split_text[0] != "":
                    node_list.append(TextNode(split_text[0], old_type))
                node_list.append(TextNode(split_text[1], text_type))
                if split_text[2] != "":
                    node_list.append(TextNode(split_text[2], old_type))
            else:
                node_list.append(node)
        else:
            node_list.append(node)
    return node_list

def extract_markdown_images(text): #chapter 3 lesson 4
    extracted_imgs = re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
    return extracted_imgs

def extract_markdown_links(text): #ch3 L4
    extd_links = re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
    return extd_links

def split_nodes_image(old_nodes):
    node_list = []
    for old_node in old_nodes:
        old_text = old_node.text
        old_type = old_node.text_type
        
        img_count = old_text.count("![")
        if img_count > 0:
            ext_imgs = extract_markdown_images(old_text)
            for ei in ext_imgs:
                result = old_text.split(f"![{ei[0]}]({ei[1]})", 1)
                if result[0] != "":
                    node_list.append(TextNode(result[0], old_type))
                node_list.append(TextNode(ei[0], TextType.IMAGE, ei[1]))
                old_text = result[1]
            if old_text != "":
                node_list.append(TextNode(old_text, old_type))
                    
        else:
            node_list.append(old_node)
    return node_list
            
            

def split_nodes_link(old_nodes):
    node_list = []
    for old_node in old_nodes:
        old_text = old_node.text
        old_type = old_node.text_type
        
        link_count = old_text.count("[") - old_text.count("![")
        if link_count > 0:
            ext_links = extract_markdown_links(old_text)
            for ei in ext_links:
                result = old_text.split(f"[{ei[0]}]({ei[1]})", 1)
                if result[0] != "":
                    node_list.append(TextNode(result[0], old_type))
                node_list.append(TextNode(ei[0], TextType.LINK, ei[1]))
                old_text = result[1]
            if old_text != "":
                node_list.append(TextNode(old_text, old_type))
        else:
            node_list.append(old_node)
    return node_list
            
def text_to_textnodes(text):
    text_nodes = [TextNode(text, TextType.TEXT)]
    img_count = text.count("![")
    if img_count > 0:
        text_nodes = split_nodes_image(text_nodes)
    link_count = text.count("[")
    if link_count > img_count:
        link_count -= img_count
    if link_count > 0:
        text_nodes = split_nodes_link(text_nodes)

    if text.count("**")// 2 > 0:
        text_nodes = split_nodes_delimiter(text_nodes, "**", TextType.BOLD)
    
    if text.count("_") // 2 > 0:
        text_nodes = split_nodes_delimiter(text_nodes, "_", TextType.ITALIC)

    if text.count("`") // 2 > 0:
        text_nodes = split_nodes_delimiter(text_nodes, "`", TextType.CODE)


    return text_nodes

            

        