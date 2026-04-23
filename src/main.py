import os

from textnode import TextNode, TextType
from htmlnode import LeafNode, ParentNode
from copy import copy, generate_page

def main():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    source_dir = os.path.abspath(os.path.join(current_dir, "..", "static"))
    copy(source_dir)
    content_path = os.path.abspath(os.path.join(current_dir, "..", "content/index.md"))
    template_path = os.path.abspath(os.path.join(current_dir, "..", "template.html"))
    dest_path = os.path.abspath(os.path.join(current_dir, "..", "public/index.html"))
    generate_page(content_path, template_path, dest_path)

main()