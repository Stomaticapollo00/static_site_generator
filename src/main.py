import os, sys

from textnode import TextNode, TextType
from htmlnode import LeafNode, ParentNode
from copy import copy, generate_pages

def main(basepath='/'):
    current_dir = os.path.dirname(os.path.abspath(__file__))
    source_dir = os.path.abspath(os.path.join(current_dir, "..", "static"))
    copy(source_dir)
    content_path = os.path.abspath(os.path.join(current_dir, "..", "content"))
    template_path = os.path.abspath(os.path.join(current_dir, "..", "template.html"))
    dest_path = os.path.abspath(os.path.join(current_dir, "..", "docs"))
    generate_pages(content_path, template_path, dest_path, basepath)

main(sys.argv[1])