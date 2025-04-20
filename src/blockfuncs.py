#import re
from enum import Enum

from textnode import *
from htmlnode import *
from loosefunctions import *

#i'm breaking these blocks up ok

def markdown_to_blocks(markdown): 
    split_md = markdown.split("\n\n")
    md_blocks = []
    for block in split_md:
        block = block.strip()
        if block != "\n" and block != "":
            md_blocks.append(block)
    return md_blocks

class BlockType(Enum): #i'm never quite sure what the values should be
    paragraph = "p"
    heading = "h"
    code = "pre"
    quote = "blockquote"
    unordered_list = "ul"
    ordered_list = "ol"

def block_to_block_type(markdown): #i feel like there should be a better way to do this than six tests in a row but hey
    markdown = markdown.strip()
    
    headings = [
        "# ",
        "## ",
        "### ",
        "#### ",
        "##### ",
        "###### "
    ]
    for h in headings:
        if markdown.startswith(h):
            return BlockType.heading
    
    if markdown.startswith("```") and markdown.endswith("```"):
        return BlockType.code
    
    if markdown.startswith("> "):
        quote_block = markdown.splitlines()
        for quote in quote_block:
            quote = quote.strip()
            #print(f"QUOTE CHECKING {quote}")
            if quote.startswith(">") == False:
                return BlockType.paragraph
        return BlockType.quote
    
    if markdown.startswith("- "):
        ul_block = markdown.splitlines()
        for ul in ul_block:
            ul = ul.strip()
            if ul.startswith("- ") == False:
                return BlockType.paragraph
        return BlockType.unordered_list
    
    if markdown.startswith("1. "):
        ol_block = markdown.splitlines()
        ordered = True
        count = 1
        for ol in ol_block:
            ol = ol.strip()
            if ol.startswith(f"{str(count)}. "):
                #print(f"line {count} appears to be an ordered list")
                count += 1   
            else:
                return BlockType.paragraph
        return BlockType.ordered_list
        
    return BlockType.paragraph

def markdown_to_html_node(markdown): 
    childnodes = []
    md_blocks = markdown_to_blocks(markdown)
    for block in md_blocks:
        node = block_typer(block)
        childnodes.append(node)
    return ParentNode("div", childnodes)



def block_typer(block): #returns the html tag for the block
    type = block_to_block_type(block)
    match(type):
        case BlockType.paragraph:
            return block_paragrapher(block)
        case BlockType.heading:
            return block_headers(block)
        case BlockType.quote:
            return block_quoter(block)
        case BlockType.unordered_list:
            #print(f"{block} is an unordered list")
            return block_unlister(block)
        case BlockType.ordered_list:
            return block_orlister(block)
        case BlockType.code:
            return block_coder(block)
            
def inline_checker(tag, text):
    text_nodes = text_to_textnodes(text)
    if len(text_nodes) > 1:
        children = []
        for node in text_nodes:
            #print(f"processing inline node {node}")
            #if node.text != None and node.text != "":
            
            child_node = text_node_to_html_node(node)
            #print(f"appending {child_node}")
            children.append(child_node)
        return ParentNode(tag, children)
    solo_node = text_node_to_html_node(text_nodes[0])
    #if tag != 
    #solo_node.tag = tag
    #print(f"appending {solo_node}")

    return ParentNode(tag, [solo_node])

def block_paragrapher(block):
    p_lines = block.splitlines()
    p_list = []
    for line in p_lines:
        p_line = text_to_textnodes(line.strip())
        #if p_line != None and p_line != "" and p_line != "\n":
            #print(p_line)
        for p in p_line:
            p_list.append(text_node_to_html_node(p))
    #p_block = " ".join(p_list)
    return ParentNode("p", p_list)

def block_headers(block):
    #h_level = 0
    headings = [
        "# ",
        "## ",
        "### ",
        "#### ",
        "##### ",
        "###### "
    ]
    for h in headings:
        if block.startswith(h):
            tag = f"h{headings.index(h)+1}"
            text = block.lstrip(h)
            return inline_checker(tag, text)
    raise Exception("invalid header format somehow idk")

def block_quoter(block):
    lines = block.splitlines()
    #print(f"BLOCK QUOTE PROCESSING {lines}")
    q_lines = []
    #print(lines)
    for line in lines:
        stripped_line = text_to_textnodes(line.lstrip("> "))
        #if stripped_line == "" or stripped_line == None:
        #   stripped_line = "\n"
        for s in stripped_line:
            s.text += "<br />"
            q_lines.append(text_node_to_html_node(s))
    
    #print(q_block)
    return ParentNode("blockquote", q_lines)

def block_unlister(block):
    lines = block.splitlines()
    ul_lines = []
    for line in lines:
        ul_lines.append(inline_checker("li", line.lstrip("- ")))
    #print(f"unordered list containing {ul_lines} identified")
    return ParentNode("ul", ul_lines)

def block_orlister(block):
    lines = block.splitlines()
    ol_lines = []
    count = 1
    for line in lines:
        ol_lines.append(inline_checker("li", line.lstrip(f"{count}. ")))
        count +=1
    return ParentNode("ol", ol_lines)

def block_coder(block):
    lines = block.splitlines()
    c_lines = []
    for line in lines:
        c_text = line.strip("```")
        c_text = c_text.strip()
        if c_text != "":
            c_lines.append(c_text)
    c_result = "\n".join(c_lines)
    #print(c_result)
    c_t_node = TextNode(c_result, TextType.CODE)
    return ParentNode("pre", [text_node_to_html_node(c_t_node)])

def extract_title(markdown):
    md_lines = markdown.splitlines()
    for line in md_lines:
        if line.startswith("# "):
            return line
    raise Exception("no title line defined")
