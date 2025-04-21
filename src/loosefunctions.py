from textnode import *
from htmlnode import *


import re


def node_delistifer(nodes):
    flat_list = []
    for node in nodes:
        if isinstance(node, list):
            flat_list.extend(node)
        else:
            flat_list.append(node)
    return flat_list

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
            #print("identified an image")
            return LeafNode("img",None, props={"src":text_node.url,"alt":text_node.text})
        case _:
            return LeafNode()

def split_nodes_delimiter(old_nodes, delimiter, text_type): #chapter 3 lesson 1
    node_list = []
    for node in old_nodes:
        #print(f"node to split: {node}")
        if isinstance(node, list):
            #print(f"{node} triggered 1st list exception.")
            new_node = split_nodes_delimiter(node, delimiter, text_type)
            return new_node
        old_text = node.text
        old_type = node.text_type
        if delimiter in old_text:
            if old_text.count(delimiter) != 2 and old_text.count(delimiter) % 2 != 0:
                print(f"delimiter exception on line {old_text}")
                raise Exception("invalid markdown syntax")
            #if old_type.value == ("text" or "bold" or "italic"):
            split_text = old_text.split(delimiter,2)
            #print(split_text) #AAAAAAAAAAAAAAA
            if split_text[0] != "":
                #print(split_text[0]) #COMMENT THIS OUT WHEN YOU'RE DONE
                node_list.append(TextNode(split_text[0], old_type))
            #print(split_text[1]) #COMMENT OUT
            node_list.append(TextNode(split_text[1], text_type))
            if split_text[2] != "": #fix this later
                if split_text[2].count(delimiter) %2 == 0:
                    #node_list.append(split_nodes_delimiter([TextNode(split_text[2], old_type)], delimiter, text_type))
                    node_list.append(text_to_textnodes(split_text[2]))
                else:
                    print(split_text[2])
                    node_list.append(text_to_textnodes(split_text[2]))
            #else:
                #node_list.append(node)
        else:
            node_list.append(node)
    node_flat = node_delistifer(node_list)
    return node_flat

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
        #print(f"results of image split: {node_list}")
    return node_list
            
            

def split_nodes_link(old_nodes):
    node_list = []
    for old_node in old_nodes:
        old_text = old_node.text
        old_type = old_node.text_type
        
        link_count = old_text.count("[") - old_text.count("![")
        #print(f"link count: {link_count}")
        if link_count > 0:
            ext_links = extract_markdown_links(old_text)
            #print(f"extracted links: {ext_links}")
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
    #print(f"results of link split: {node_list}")
    return node_list
            
def text_to_textnodes(text):
    text_nodes = [TextNode(text, TextType.TEXT)]

    img_count = text.count("![")
    if img_count > 0:
        #print("found images, splitting")
        #print(f"{img_count} images found")
        text_nodes = split_nodes_image(text_nodes)
    link_count = text.count("[")
    if link_count > img_count:
        link_count -= img_count
    if link_count > 0:
        #print(f"found {link_count} links, splitting")
        text_nodes = split_nodes_link(text_nodes)

    if text.count("**")// 2 > 0:
        text_nodes = split_nodes_delimiter(text_nodes, "**", TextType.BOLD)
    
    if text.count("_") // 2 > 0:
        #print(f"ITALICS: SPLITTING {text_nodes}")
        text_nodes = split_nodes_delimiter(text_nodes, "_", TextType.ITALIC)

    if text.count("`") // 2 > 0:
        text_nodes = split_nodes_delimiter(text_nodes, "`", TextType.CODE)
    #by god this seems to work
    flat_list = node_delistifer(text_nodes)
    
    return flat_list

#to be continued in blockfuncs

            

        