from enum import Enum
from htmlnode import *

class TextType(Enum):
    TEXT = "text"
    BOLD = "bold"
    ITALIC = "italic"
    CODE = "code"
    LINK = "link"
    IMAGE = "image"

class TextNode():
    def __init__(self, text, text_type: TextType, url=None):
        self.text = text
        self.text_type = text_type
        self.url = url

    def __eq__(self, other):
        if self.text == other.text and self.text_type == other.text_type and self.url == other.url:
            return True
        return False
    
    def __repr__(self):
        return f"TextNode({self.text}, {self.text_type.value}, {self.url})"
    
def text_node_to_html_node(text_node):
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

def split_nodes_delimiter(old_nodes, delimiter, text_type):
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