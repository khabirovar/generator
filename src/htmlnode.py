from textnode import TextType, TextNode

class HTMLNode():
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        raise NotImplementedError()

    def props_to_html(self):
        if self.props is None or len(self.props) <= 0:
            return ''
        props = list()
        for key, val in self.props.items():
            props.append(f'{key}="{val}"')
        return ' ' + ' '.join(props)

    def __repr__(self):
        return f'tag: {self.tag}, value: {self.value}, children: {self.children}, props: {self.props}.'

class LeafNode(HTMLNode):
    def __init__(self, tag, value, props=None):
        super().__init__(tag, value, None, props)

    def to_html(self):
        if self.value is None:
            raise ValueError('value is required')
        
        open_tag = ''
        if not self.tag is None and  not self.tag == '':
            open_tag = f'<{self.tag}{self.props_to_html()}>'        
        
        close_tag = '' if self.tag is None or self.tag == '' else f'</{self.tag}>'        
        
        return f'{open_tag}{self.value}{close_tag}'

    def __repr__(self):
        return f'tag: {self.tag}, value: {self.value}, props: {self.props}.'

class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None):
        super().__init__(tag, None, children, props)

    def to_html(self):
        if self.tag is None or self.tag == '':
            raise ValueError('tag is required')
        if self.children is None or len(self.children) <= 0:
            raise ValueError('children is required')
        
        children_html = list()
        for child in self.children:
            children_html.append(child.to_html())
        children_html_line = ''.join(children_html)

        open_tag = f'<{self.tag}{self.props_to_html()}>'
        close_tag = f'</{self.tag}>'
        return f'{open_tag}{children_html_line}{close_tag}'   

def text_node_to_html_node(text_node):
    match text_node.text_type:
        case TextType.TEXT:
            return LeafNode(None, text_node.text)
        case TextType.BOLD:
            return LeafNode('b', text_node.text)
        case TextType.ITALIC:
            return LeafNode('i', text_node.text)
        case TextType.CODE:
            return LeafNode('code', text_node.text)
        case TextType.LINK:
            return LeafNode('a', text_node.text, {'href': text_node.url})
        case TextType.IMAGE:
            return LeafNode('img', '', {'src': text_node.url, 'alt': text_node.text})
        case _:
            raise Exception('Invalid type of text_node')
