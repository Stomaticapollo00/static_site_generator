import unittest

from htmlnode import HTMLNode, LeafNode


class TestTextNode(unittest.TestCase):
    def test_htmlnode(self):
        test_props = {"href": "https://www.google.com", "target": "_blank",}
        node = HTMLNode("tag line", "I am a value", None, test_props)
        node2 = HTMLNode("tag line", "I am a value", [node], test_props)
        self.assertEqual(node2.tag, "tag line")
        self.assertEqual(node2.value, "I am a value")
        self.assertEqual(node2.children, [node])
        self.assertEqual(node2.props, {"href": "https://www.google.com", "target": "_blank",})
        self.assertNotEqual(node, node2)

    def test_to_html(self):
        test_props = {"href": "https://www.google.com", "target": "_blank",}
        node = HTMLNode("tag line", "I am a value", None, test_props)
        with self.assertRaises(NotImplementedError):
            node.to_html()

    def test_props_to_html(self):
        test_props = {"href": "https://www.google.com", "target": "_blank",}
        node = HTMLNode("tag line", "I am a value", None, test_props)
        self.assertEqual(node.props_to_html(), ' href="https://www.google.com" target="_blank"')

    def test_repr(self):
        test_props = {"href": "https://www.google.com", "target": "_blank",}
        node = HTMLNode("tag line", "I am a value", None, test_props)
        node2 = HTMLNode("tag line", "I am a value", [node], test_props)
        self.assertEqual(node.__repr__(), 'HTMLNode(tag line; I am a value; None;  href="https://www.google.com" target="_blank")')
        self.assertEqual(node2.__repr__(), 'HTMLNode(tag line; I am a value; HTMLNode(tag line; I am a value; None;  href="https://www.google.com" target="_blank");  href="https://www.google.com" target="_blank")')

    def test_leafnode(self):
        test_props = {"href": "https://www.google.com", "target": "_blank",}
        node = LeafNode("p", "I am a value", test_props)
        self.assertEqual(node.tag, "p")
        self.assertEqual(node.value, "I am a value")
        self.assertEqual(node.props, {"href": "https://www.google.com", "target": "_blank",})

    def test_leaf_to_html(self):
        node = LeafNode("p", "Hello, world!")
        node2 = LeafNode("b", "Hello, world!")
        node3 = LeafNode("a", "Click me!", {"href": "https://www.google.com"})
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")
        self.assertEqual(node2.to_html(), "<b>Hello, world!</b>")
        self.assertEqual(node3.to_html(), '<a href="https://www.google.com">Click me!</a>')

    def test_leaf_repr(self):
        test_props = {"href": "https://www.google.com", "target": "_blank",}
        node = LeafNode("a", "I am a value", test_props)
        self.assertEqual(node.__repr__(), 'LeafNode(a; I am a value;  href="https://www.google.com" target="_blank")')


if __name__ == "__main__":
    unittest.main()