from textnode import *
from htmlnode import *
from loosefunctions import *
from blockfuncs import *
from importstatic import *

import sys

basepath = sys.argv[0]
if basepath == None:
    basepath = "/"


import_from_static("logfile.log", "docs")
convert_md_files("logfile.log", "content", "docs", basepath)

#test_md = """#This series, a cornerstone of what I, in my many years as an **Archmage**, have come to recognize as the pinnacle of imaginative creation, stands unrivaled in its depth, complexity, and the sheer scope of its _legendarium_. As we embark on this exploration, let us delve into the reasons why this monumental work is celebrated as the finest in the world."""
#print(markdown_to_html_node(test_md))
#print(text_to_textnodes(test_md))
#test_blocks = block_typer(test_md)
#print(test_blocks.to_html())
#print(text_to_textnodes(test_md))
#print(node_delistifer(text_to_textnodes(test_md)))