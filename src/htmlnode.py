from textnode import TextType, TextNode
from helpers import markdown_to_blocks, text_to_textnodes
from blocktype import BlockType, block_to_block_type


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

def text_to_children(text):
    textnodes = text_to_textnodes(text)
    htmlnodes = [text_node_to_html_node(item) for item in textnodes]
    return htmlnodes

def markdown_to_html_node(markdown):
    root = ParentNode('div', list())
    blocks = markdown_to_blocks(markdown)
    for block in blocks:
        block_type = block_to_block_type(block)
        node = None
        if block_type == BlockType.PARAGRAPH:
            text = ' '.join(block.split('\n'))
            if not text:
                node = None
            else:
                children = text_to_children(text)
                node = ParentNode('p',children)
        elif block_type == BlockType.CODE:
            text = '\n'.join(block.split('\n')[1:-1]) + '\n'
            node = LeafNode('code',text)
            node = ParentNode('pre', [node])
        elif block_type == BlockType.HEADING:
            head, text = block.split(' ', maxsplit=1)
            children = text_to_children(text)
            node = ParentNode(f'h{len(head)}', children)
        elif block_type == BlockType.QUOTE:
            lines = block.split('\n')
            lines = [item[2:] if item.startswith('> ') else item for item in lines]
            text = ' '.join(lines)
            children = text_to_children(text)
            node = ParentNode('blockquote', children)
        elif block_type == BlockType.UNORDERED_LIST:
            lines = block.split('\n')
            items = list()
            for line in lines:
                if not line.strip():
                    continue
                text = line[:]
                if text.startswith('- ') or text.startswith('* '):
                    text = text[2:]
                children = text_to_children(text)
                items.append(ParentNode('li',children))
            node = ParentNode('ul', items)
        elif block_type == BlockType.ORDERED_LIST:
            lines = block.split('\n')
            items = list()
            for line in lines:
                if not line.strip():
                    continue
                _, text = line.split('. ',maxsplit=1)
                children = text_to_children(text)
                items.append(ParentNode('li', children))
            node = ParentNode('ol', items)
        if node is not None:
            root.children.append(node) 
    return root 
