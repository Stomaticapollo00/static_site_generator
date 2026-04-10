import unittest

from textnode import TextNode, TextType
from htmlnode import HTMLNode, LeafNode, ParentNode
from nodeconverter import *


class TestTextNodeToHTMLNode(unittest.TestCase):
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

class TestTokenizer(unittest.TestCase):
    def test_tokenize_inline_markdown(self):
        text1 = "hello"
        text2 = "hello **world**"
        text3 = "hello _world_, hi"
        text4 = "hello `print('world')`"
        text5 = "go to [hello](https://www.world.com)"
        text6 = "![hello](https://www.world.com/image) OMG, check this out!"
        text7 = "**hello**, _I am_ the ![world](https://www.world.com/image)[click here to see more](https://www.world.com)"
        new_nodes1 = tokenize_inline_markdown(text1)
        new_nodes2 = tokenize_inline_markdown(text2)
        new_nodes3 = tokenize_inline_markdown(text3)
        new_nodes4 = tokenize_inline_markdown(text4)
        new_nodes5 = tokenize_inline_markdown(text5)
        new_nodes6 = tokenize_inline_markdown(text6)
        new_nodes7 = tokenize_inline_markdown(text7)
        self.assertEqual(
            new_nodes1,
            [
                TextNode("hello", TextType.TEXT),
            ],
        )
        self.assertEqual(
            new_nodes2,
            [
                TextNode("hello ", TextType.TEXT),
                TextNode("world", TextType.BOLD),
            ],
        )
        self.assertEqual(
            new_nodes3,
            [
                TextNode("hello ", TextType.TEXT),
                TextNode("world", TextType.ITALIC),
                TextNode(", hi", TextType.TEXT),
            ],
        )
        self.assertEqual(
            new_nodes4,
            [
                TextNode("hello ", TextType.TEXT),
                TextNode("print('world')", TextType.CODE),
            ],
        )
        self.assertEqual(
            new_nodes5,
            [
                TextNode("go to ", TextType.TEXT),
                TextNode("hello", TextType.LINK, "https://www.world.com"),
            ],
        )
        self.assertEqual(
            new_nodes6,
            [
                TextNode("hello", TextType.IMAGE, "https://www.world.com/image"),
                TextNode(" OMG, check this out!", TextType.TEXT),
            ],
        )
        self.assertEqual(
            new_nodes7,
            [
                TextNode("hello", TextType.BOLD),
                TextNode(", ", TextType.TEXT),
                TextNode("I am", TextType.ITALIC),
                TextNode(" the ", TextType.TEXT),
                TextNode("world", TextType.IMAGE, "https://www.world.com/image"),
                TextNode("click here to see more", TextType.LINK, "https://www.world.com"),
            ],
        )

    def test_text_to_textnode(self):
        text1 = "hello"
        text2 = "hello **world**"
        text3 = "hello _world_, hi"
        text4 = "hello `print('world')`"
        text5 = "go to [hello](https://www.world.com)"
        text6 = "![hello](https://www.world.com/image) OMG, check this out!"
        text7 = "**hello**, _I am_ the ![world](https://www.world.com/image)[click here to see more](https://www.world.com)"
        new_nodes1 = text_to_textnodes(text1)
        new_nodes2 = text_to_textnodes(text2)
        new_nodes3 = text_to_textnodes(text3)
        new_nodes4 = text_to_textnodes(text4)
        new_nodes5 = text_to_textnodes(text5)
        new_nodes6 = text_to_textnodes(text6)
        new_nodes7 = text_to_textnodes(text7)
        self.assertEqual(
            new_nodes1,
            [
                TextNode("hello", TextType.TEXT),
            ],
        )
        self.assertEqual(
            new_nodes2,
            [
                TextNode("hello ", TextType.TEXT),
                TextNode("world", TextType.BOLD),
            ],
        )
        self.assertEqual(
            new_nodes3,
            [
                TextNode("hello ", TextType.TEXT),
                TextNode("world", TextType.ITALIC),
                TextNode(", hi", TextType.TEXT),
            ],
        )
        self.assertEqual(
            new_nodes4,
            [
                TextNode("hello ", TextType.TEXT),
                TextNode("print('world')", TextType.CODE),
            ],
        )
        self.assertEqual(
            new_nodes5,
            [
                TextNode("go to ", TextType.TEXT),
                TextNode("hello", TextType.LINK, "https://www.world.com"),
            ],
        )
        self.assertEqual(
            new_nodes6,
            [
                TextNode("hello", TextType.IMAGE, "https://www.world.com/image"),
                TextNode(" OMG, check this out!", TextType.TEXT),
            ],
        )
        self.assertEqual(
            new_nodes7,
            [
                TextNode("hello", TextType.BOLD),
                TextNode(", ", TextType.TEXT),
                TextNode("I am", TextType.ITALIC),
                TextNode(" the ", TextType.TEXT),
                TextNode("world", TextType.IMAGE, "https://www.world.com/image"),
                TextNode("click here to see more", TextType.LINK, "https://www.world.com"),
            ],
        )

    def test_textblock(self):
        text = 'This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)'
        new_nodes = text_to_textnodes(text)
        self.assertListEqual(
            new_nodes,
            [
                TextNode("This is ", TextType.TEXT),
                TextNode("text", TextType.BOLD),
                TextNode(" with an ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
                TextNode(" word and a ", TextType.TEXT),
                TextNode("code block", TextType.CODE),
                TextNode(" and an ", TextType.TEXT),
                TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
                TextNode(" and a ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://boot.dev"),
            ],
        )

if __name__ == "__main__":
    unittest.main()