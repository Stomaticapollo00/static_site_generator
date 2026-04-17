import os

from textnode import TextNode, TextType
from htmlnode import LeafNode, ParentNode
from copy import copy

def main():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    source_dir = os.path.abspath(os.path.join(current_dir, "..", "static"))
    copy(source_dir)

main()