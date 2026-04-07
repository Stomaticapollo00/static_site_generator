import unittest

from textnode import TextNode, TextType
from htmlnode import HTMLNode, LeafNode, ParentNode
from nodeconverter import text_node_to_html_node, split_nodes_delimiter


class TestTextToHTMLConverter(unittest.TestCase):
    def test_text(self):
        node = TextNode("This is a text node", TextType.TEXT)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")
    
    def test_bold(self):
        node = TextNode("This is a bold text node", TextType.BOLD)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "b")
        self.assertEqual(html_node.value, "This is a bold text node")
        
    def test_italic(self):
        node = TextNode("This is an italic text node", TextType.ITALIC)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "i")
        self.assertEqual(html_node.value, "This is an italic text node")

    def test_code(self):
        node = TextNode("This is a code text node", TextType.CODE)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "code")
        self.assertEqual(html_node.value, "This is a code text node")

    def test_link(self):
        node = TextNode("This is a link text node", TextType.LINK, "https://www.google.com")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "a")
        self.assertEqual(html_node.value, "This is a link text node")
        self.assertEqual(html_node.props, {"href": "https://www.google.com"})

    def test_image(self):
        node = TextNode("This is an image alt text node", TextType.IMAGE, "https://www.google.com")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "img")
        self.assertEqual(html_node.value, "")
        self.assertEqual(html_node.props, {"src":"https://www.google.com", "alt": "This is an image alt text node"})

    def test_unknown(self):
        node = TextNode("This is a hyperlink text node", "hyperlink", "https://www.google.com")
        with self.assertRaises(Exception):
            text_node_to_html_node(node)

class TestSplitNodesDelimiter(unittest.TestCase):
    def test_splitting(self):
        node = TextNode("This is text with a `code block` word", TextType.TEXT)
        node2 = TextNode("This is text with a **bolded phrase** in the middle", TextType.TEXT)
        node3 = TextNode("This is text with a bold phrase at **the end**", TextType.TEXT)
        node4 = TextNode("This is **text** with a few **bold** words **in it**", TextType.TEXT)
        node5 = TextNode("**This is text** with a bold phrase at the beginning", TextType.TEXT)
        node6 = TextNode("This is `text without closing the delimiter", TextType.TEXT)
        node7 = TextNode("This is _text_ with **multiple** delimiters", TextType.TEXT)
        node8 = TextNode("This is already bold", TextType.BOLD)
        node9 = TextNode("This is already italic", TextType.ITALIC)
        node10 = TextNode("This is just text", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        new_nodes2 = split_nodes_delimiter([node2, node3, node4], "**", TextType.BOLD)
        new_nodes3 = split_nodes_delimiter([node5], "**", TextType.BOLD)
        new_nodes4 = split_nodes_delimiter(split_nodes_delimiter([node7], "_", TextType.ITALIC), "**", TextType.BOLD)
        new_nodes5 = split_nodes_delimiter([node2, node8, node9, node10], "**", TextType.BOLD)
        self.assertEqual(
                            new_nodes,
                            [
                                TextNode("This is text with a ", TextType.TEXT),
                                TextNode("code block", TextType.CODE),
                                TextNode(" word", TextType.TEXT),
                            ],
                        )
        self.assertEqual(
                            new_nodes2,
                            [
                                TextNode("This is text with a ", TextType.TEXT),
                                TextNode("bolded phrase", TextType.BOLD),
                                TextNode(" in the middle", TextType.TEXT),
                                TextNode("This is text with a bold phrase at ", TextType.TEXT),
                                TextNode("the end", TextType.BOLD),
                                TextNode("This is ", TextType.TEXT),
                                TextNode("text", TextType.BOLD),
                                TextNode(" with a few ", TextType.TEXT),
                                TextNode("bold", TextType.BOLD),
                                TextNode(" words ", TextType.TEXT),
                                TextNode("in it", TextType.BOLD),
                            ],
                        )
        self.assertEqual(
                            new_nodes3,
                            [
                                TextNode("This is text", TextType.BOLD),
                                TextNode(" with a bold phrase at the beginning", TextType.TEXT),
                            ],
                        )
        self.assertEqual(
                            new_nodes4,
                            [
                                TextNode("This is ", TextType.TEXT),
                                TextNode("text", TextType.ITALIC),
                                TextNode(" with ", TextType.TEXT),
                                TextNode("multiple", TextType.BOLD),
                                TextNode(" delimiters", TextType.TEXT),
                            ],
                        )
        self.assertEqual(
                            new_nodes5,
                            [
                                TextNode("This is text with a ", TextType.TEXT),
                                TextNode("bolded phrase", TextType.BOLD),
                                TextNode(" in the middle", TextType.TEXT),
                                TextNode("This is already bold", TextType.BOLD),
                                TextNode("This is already italic", TextType.ITALIC),
                                TextNode("This is just text", TextType.TEXT),
                            ],
                        )
        with self.assertRaises(Exception):
            split_nodes_delimiter([node6], "`", TextType.CODE)