import unittest

from textnode import TextNode, TextType


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)
    
    def test_textnode(self):
        node = TextNode("This is a text node", TextType.ITALIC, "google.com")
        node2 = TextNode("This is a text node", TextType.CODE)
        self.assertEqual(node.text, "This is a text node")
        self.assertEqual(node.text_type, TextType.ITALIC)
        self.assertEqual(node.url, "google.com")
        self.assertEqual(node2.text, "This is a text node")
        self.assertEqual(node2.text_type.value, "code")
        self.assertEqual(node2.url, None)
        self.assertNotEqual(node, node2)

    def test_repr(self):
        node = TextNode("This is a text node", TextType.ITALIC, "google.com")
        self.assertEqual(node.__repr__(), "TextNode(This is a text node, italic, google.com)")

if __name__ == "__main__":
    unittest.main()