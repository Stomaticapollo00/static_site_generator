import unittest

from htmlnode import HTMLNode, LeafNode, ParentNode


class TestHTMLNode(unittest.TestCase):
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
        self.assertEqual(node.children, None)
        self.assertEqual(node.props, {"href": "https://www.google.com", "target": "_blank",})

    def test_leaf_to_html(self):
        node = LeafNode("p", "Hello, world!")
        node2 = LeafNode("b", "Hello, world!")
        node3 = LeafNode("a", "Click me!", {"href": "https://www.google.com"})
        node4 = LeafNode("img", "", {"src": "https://www.google.com", "alt": "Im an image!"})
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")
        self.assertEqual(node2.to_html(), "<b>Hello, world!</b>")
        self.assertEqual(node3.to_html(), '<a href="https://www.google.com">Click me!</a>')
        self.assertEqual(node4.to_html(), '<img src="https://www.google.com" alt="Im an image!" />')

    def test_leaf_repr(self):
        test_props = {"href": "https://www.google.com", "target": "_blank",}
        node = LeafNode("a", "I am a value", test_props)
        self.assertEqual(node.__repr__(), 'LeafNode(a; I am a value;  href="https://www.google.com" target="_blank")')

    def test_parentnode(self):
        test_props = {"href": "https://www.google.com", "target": "_blank",}
        child_node = LeafNode("b", "Hello, world!")
        parent_node = ParentNode("p", [child_node], test_props)
        self.assertEqual(parent_node.tag, "p")
        self.assertEqual(parent_node.value, None)
        self.assertEqual(parent_node.children, [child_node])
        self.assertEqual(parent_node.props, {"href": "https://www.google.com", "target": "_blank",})

    def test_parent_to_html_no_children(self):
        parent_node = ParentNode("p", None)
        with self.assertRaises(ValueError):
            parent_node.to_html()

    def test_parent_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        child_node2 = LeafNode("b", "I am bold")
        child_node3 = LeafNode("i", "I am italics")
        children = [child_node2, child_node3, child_node]
        parent_node = ParentNode("div", [child_node])
        parent_node2 = ParentNode("p", children)
        parent_node3 = ParentNode("img", [child_node2], {"img": "https://www.google.com"})
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")
        self.assertEqual(parent_node2.to_html(), "<p><b>I am bold</b><i>I am italics</i><span>child</span></p>")
        self.assertEqual(parent_node3.to_html(), '<img src="https://www.google.com" alt="" /><b>I am bold</b>')

    def test_parent_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        grandchild_node2 = LeafNode("i", "granderchild")
        grandchild_node3 = LeafNode("a", "Click me!", {"href": "https://www.google.com"})
        child_node = ParentNode("span", [grandchild_node])
        child_node2 = ParentNode("p", [grandchild_node2, grandchild_node3])
        parent_node = ParentNode("div", [child_node])
        parent_node2 = ParentNode("div", [child_node, child_node2])
        parent_node3 = ParentNode("a", [child_node], {"href": "https://www.google.com"})
        self.assertEqual(parent_node.to_html(), "<div><span><b>grandchild</b></span></div>")
        self.assertEqual(parent_node2.to_html(), '<div><span><b>grandchild</b></span><p><i>granderchild</i><a href="https://www.google.com">Click me!</a></p></div>')
        self.assertEqual(parent_node3.to_html(), '<a href="https://www.google.com"><span><b>grandchild</b></span></a>')

if __name__ == "__main__":
    unittest.main()