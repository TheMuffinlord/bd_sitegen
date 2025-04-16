class HTMLNode():
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        raise NotImplementedError("not implemented for HTMLNode class, idiot")
    
    def props_to_html(self):
        if self.props != None:
            all_props = " "
            count = 1
            for prop in self.props:
                if count > 1:
                    all_props += " "
                all_props += f'{prop}="{self.props[prop]}"'
                count += 1    
            return all_props
        return ""
    
    def __repr__(self):
        return f"HTMLNode({self.tag}, {self.value}, {self.children}, {self.props})"
    
class LeafNode(HTMLNode):
    def __init__(self, tag, value, props=None):
        super().__init__(tag, value, None, props)

    def to_html(self):
        if self.value == None:
            raise ValueError("Leaf Node missing value")
        elif self.tag == None:
            return str(self.value)
        else:
            return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"
        
class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None):
        super().__init__(tag, None, children, props)

    def to_html(self):
        if self.tag == None:
            raise ValueError("Parent node missing tag")
        elif self.children == None:
            raise ValueError("Parent node has no children")
        else:
            parent_html = f"<{self.tag}{self.props_to_html()}>"
            for child in self.children:
                parent_html += child.to_html()
            return parent_html + f"</{self.tag}>"