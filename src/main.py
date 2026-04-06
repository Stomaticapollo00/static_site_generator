from textnode import TextNode, TextType
from htmlnode import LeafNode, ParentNode

def main():
    testtype = TextType.LINK
    testnode = TextNode("This is some anchor text", testtype, "https://www.boot.dev")
    print(testnode.__repr__())

main()