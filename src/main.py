from textnode import TextNode, TextType

def main():
    testtype = TextType.LINK
    testnode = TextNode("This is some anchor text", testtype, "https://www.boot.dev")
    print(testnode.__repr__())

main()