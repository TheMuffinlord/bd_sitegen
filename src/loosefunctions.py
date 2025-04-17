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
    old_text = old_nodes.text
    old_type = old_nodes.text_type
    node_list = []
    if old_text.count(delimiter) != 2:
        raise Exception("invalid markdown syntax")
    if old_type.value == "text":
        split_text = old_text.split(delimiter)
        node_list.append(TextNode(split_text[0], old_type))
        node_list.append(TextNode(split_text[1], text_type))
        node_list.append(TextNode(split_text[2], old_type))
    else:
        node_list.append(old_nodes)
    return node_list

def extract_markdown_images(text): #chapter 3 lesson 4
    extracted_imgs = re.findall(r"\!\[(.*)\]\((.*)\)", text)
    return extracted_imgs

def extract_markdown_links(text): #ch3 L4
    extd_links = re.findall(r"\[(.*)\]\((.*)\)", text)
    return extd_links