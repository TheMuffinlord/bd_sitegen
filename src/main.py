from textnode import *
from htmlnode import *
from loosefunctions import *
from blockfuncs import *
from importstatic import *

convert_md_files("logfile.log", "content", "static")
import_from_static("logfile.log")

