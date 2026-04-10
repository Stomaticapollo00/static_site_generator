import re

from textnode import TextNode, TextType
from htmlnode import LeafNode

TOKEN_REGEX = re.compile(
    r"(!\[([^\[\]]*)\]\(([^\(\)]*)\))"      #IMAGE
    r"|(\[([^\[\]]*)\]\(([^\(\)]*)\))"      #LINK
    r"|(\*\*([^*]+)\*\*)"                   #BOLD
    r"|(_([^_]+)_)"                         #ITALIC
    r"|(`([^`]+)`)"                         #CODE
)

def text_node_to_html_node(text_node):
    html_tags = {
        TextType.BOLD: "b",
        TextType.CODE: "code",
        TextType.ITALIC: "i",
        TextType.TEXT: None,
    }
    if text_node.text_type in html_tags:
        return LeafNode(html_tags[text_node.text_type], text_node.text)
    if text_node.text_type == TextType.IMAGE:
        return LeafNode(
                "img",
                "",
                {
                    "src": text_node.url,
                    "alt": text_node.text,
                },
            )
    if text_node.text_type == TextType.LINK:
        return LeafNode(
                "a", 
                text_node.text, 
                {
                    "href":text_node.url
                },
            )
    raise Exception("Text type is not supported.")

def tokenize_inline_markdown(text):
    new_nodes = []
    last_index = 0
    for match in TOKEN_REGEX.finditer(text):
        start, end = match.span()
        if start > last_index:  #LEADING TEXT
            new_nodes.append(TextNode(text[last_index:start], TextType.TEXT))
        if match.group(1):      #IMAGE
            alt_text = match.group(2)
            url = match.group(3)
            new_nodes.append(TextNode(alt_text, TextType.IMAGE, url))
        elif match.group(4):    #LINK
            link_text = match.group(5)
            url = match.group(6)
            new_nodes.append(TextNode(link_text, TextType.LINK, url))
        elif match.group(7):    #BOLD
            bold_text = match.group(8)
            new_nodes.append(TextNode(bold_text, TextType.BOLD))
        elif match.group(9):    #ITALIC
            italic_text = match.group(10)
            new_nodes.append(TextNode(italic_text, TextType.ITALIC))
        elif match.group(11):   #CODE
            code_text = match.group(12)
            new_nodes.append(TextNode(code_text, TextType.CODE))
        last_index = end
    if last_index < len(text):  #TRAILING TEXT
        new_nodes.append(TextNode(text[last_index:], TextType.TEXT))
    return new_nodes

def text_to_textnodes(text):
    return tokenize_inline_markdown(text)
