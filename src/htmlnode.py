
class HTMLNode:
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def __repr__(self):
        return f"HTMLNode({self.tag}; {self.value}; {(",".join(map(str, self.children)) if self.children is not None else "None")}; {self.props_to_html()})"
    
    def to_html(self):
        raise NotImplementedError
    
    def props_to_html(self):
        props_string = ""
        if self.props is not None:
            for key, value in self.props.items():
                props_string += f' {key}="{value}"'
        return props_string

class LeafNode(HTMLNode):
    def __init__(self, tag, value, props=None):
        super().__init__(tag, value, None, props)
    
    def to_html(self):
        if self.value is None:
            raise ValueError
        elif self.tag is None:
            return self.value
        else:
            match self.tag:
                case "a":
                    return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"
                case _:
                    return f"<{self.tag}>{self.value}</{self.tag}>"
  
    def __repr__(self):
        return f"LeafNode({self.tag}; {self.value}; {self.props_to_html()})"