from textnode import *
from htmlnode import *
from loosefunctions import *
from blockfuncs import *
from importstatic import *


import_from_static("logfile.log")
convert_md_files("logfile.log", "content", "public")
