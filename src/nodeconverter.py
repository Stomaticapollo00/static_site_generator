import re

from textnode import TextNode, TextType
from htmlnode import LeafNode, ParentNode
from textblock import markdown_to_blocks, block_to_blocktype, BlockType

TOKEN_REGEX = re.compile(
    r"(!\[([^\[\]]*)\]\(([^\(\)]*)\))"      #IMAGE
    r"|(\[([^\[\]]*)\]\(([^\(\)]*)\))"      #LINK
    r"|(\*\*([^*]+)\*\*)"                   #BOLD
    r"|(_([^_]+)_)"                         #ITALIC
    r"|(`([^`]+)`)"                         #CODE
)

def strip_ordered_list_prefix(line):
    return re.sub(r"^\d+\.\s+", "", line)

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

def text_to_children(text):
    textnodes = text_to_textnodes(text)
    return [text_node_to_html_node(textnode) for textnode in textnodes]

def markdown_to_html_node(markdown):
    html_master = []
    md_blocks = markdown_to_blocks(markdown)
    for md_block in md_blocks:
        blocktype = block_to_blocktype(md_block)
        lines = md_block.split("\n")
        if blocktype == BlockType.CODE:         #CODE BLOCK
            code_text = "\n".join(lines[1:-1]) + "\n"
            code_node = LeafNode("code", code_text)
            parentnode = ParentNode("pre", [code_node])
        elif blocktype == BlockType.HEADING:    #HEADING BLOCK
            count = 0
            heading_text = md_block
            while heading_text.startswith("#"):
                count += 1
                heading_text = heading_text[1:]
            heading_text = heading_text.strip()
            parentnode = ParentNode(f"h{count}", text_to_children(heading_text))
        elif blocktype == BlockType.QUOTE:      #QUOTE BLOCK
            quote_lines = [line[1:].strip() for line in lines]
            quote_text = " ".join(quote_lines)
            parentnode = ParentNode("blockquote", text_to_children(quote_text))
        elif blocktype == BlockType.U_LIST:     #UNORDERED LIST
            line_items = []
            for line in lines:
                item_text = line[2:].strip()
                line_items.append(ParentNode("li", text_to_children(item_text)))
            parentnode = ParentNode("ul", line_items)
        elif blocktype == BlockType.O_LIST:     #ORDERED LIST
            line_items = []
            for line in lines:
                item_text = strip_ordered_list_prefix(line).strip()
                line_items.append(ParentNode("li", text_to_children(item_text)))
            parentnode = ParentNode("ol", line_items)
        else:                                   #PARAGRAPH BLOCK
            paragraph_text = " ".join(line.strip() for line in lines)
            parentnode = ParentNode("p", text_to_children(paragraph_text))
        html_master.append(parentnode)
    return ParentNode("div", html_master)
