from textnode import TextNode, TextType
from htmlnode import LeafNode, ParentNode

def text_node_to_html_node(text_node):
    match text_node.text_type:
        case TextType.TEXT:
            return LeafNode(None, text_node.text)
        case TextType.BOLD:
            return LeafNode("b", text_node.text)
        case TextType.ITALIC:
            return LeafNode("i", text_node.text)
        case TextType.CODE:
            return LeafNode("code", text_node.text)
        case TextType.LINK:
            return LeafNode(
                "a", 
                text_node.text, 
                {
                    "href":text_node.url
                },
                )
        case TextType.IMAGE:
            return LeafNode(
                "img",
                "",
                {
                    "src": text_node.url,
                    "alt": text_node.text,
                },
                )
        case _:
            raise Exception("Text type is not supported.")

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
        else:
            old_text = old_node.text
            if old_text.count(delimiter) >= 2 and old_text.count(delimiter) % 2 == 0:
                while delimiter in old_text:
                    tmp_text_list = old_text.split(delimiter, 2)
                    for i in range(0, len(tmp_text_list)):
                        if i == 0 and tmp_text_list[i] != "":
                            tmp_node = TextNode(tmp_text_list[i], TextType.TEXT)
                            new_nodes.append(tmp_node)
                        elif i == 1:
                            tmp_node = TextNode(tmp_text_list[i], text_type)
                            new_nodes.append(tmp_node)
                    old_text = tmp_text_list[-1]
                if old_text != "":
                    new_nodes.append(TextNode(old_text, TextType.TEXT))
            elif delimiter in old_text:
                raise Exception("Delimiter found in text but not closed properly")
            else:
                new_nodes.append(old_node)
    return new_nodes
