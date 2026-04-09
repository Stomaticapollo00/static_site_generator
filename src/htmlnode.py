
class HTMLNode:
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def __repr__(self):
        children_str = "None"
        if self.children is not None:
            children_str = ", ".join(str(child) for child in self.children)
        return f"HTMLNode({self.tag}; {self.value}; {children_str}; {self.props_to_html()})"
    
    def to_html(self):
        raise NotImplementedError
    
    def props_to_html(self):
        if self.props is None:
            return ""
        return "".join(f' {key}="{value}"' for key, value in self.props.items())

class LeafNode(HTMLNode):
    def __init__(self, tag, value, props=None):
        super().__init__(tag, value, None, props)
    
    def to_html(self):
        if self.value is None and self.tag != "img":
            raise ValueError("LeafNode was created with no text value")
        if self.tag is None:
            return self.value
        if self.tag == "img":
            if self.props is None or "src" not in self.props or "alt" not in self.props:
                raise ValueError("Image LeafNode was created with no source and/or no alt text")
            return f'<img src="{self.props["src"]}" alt="{self.props["alt"]}" />'
        return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"
  
    def __repr__(self):
        return f"LeafNode({self.tag}; {self.value}; {self.props_to_html()})"

class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None):
        super().__init__(tag, None, children, props)
    
    def to_html(self):
        if self.tag is None:
            raise ValueError("ParentNode was created with no HTML Tag")
        if self.children is None:
            raise ValueError("ParentNode was created with no child node(s)")
        children_html = "".join(child.to_html() for child in self.children)
        return f"<{self.tag}{self.props_to_html()}>{children_html}</{self.tag}>"