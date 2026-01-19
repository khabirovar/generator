import unittest

from htmlnode import HTMLNode, LeafNode, ParentNode, text_node_to_html_node
from htmlnode import markdown_to_blocks, markdown_to_html_node, extract_title
from textnode import TextType, TextNode
from split import text_to_textnodes


class TestHTMLNode(unittest.TestCase):
    def test_empty_props(self):
        node = HTMLNode(props=None)
        self.assertEqual(node.props_to_html(), '')

    def test_simple_props(self):
        props_dict = {
            'href': 'https://example.com',
            'target': '_blank',
        }
        props_text = ' href="https://example.com" target="_blank"'
        node = HTMLNode(props=props_dict)
        self.assertEqual(node.props_to_html(), props_text)

    def test_single_props(self):
        props_dict = {
            'test': 'testtest',
        }
        props_text = ' test="testtest"'
        node = HTMLNode(props=props_dict)
        self.assertEqual(node.props_to_html(), props_text)

class TestLeafNode(unittest.TestCase):
    def test_leaf_to_html_p(self):
        node = LeafNode('p', 'Example.com')
        self.assertEqual(node.to_html(), '<p>Example.com</p>')

    def test_leaf_with_props(self):
        props_dict = {
            'href': 'https://example.com',
            'target': '_blank',
        }
        props_text = ' href="https://example.com" target="_blank"'
        node = LeafNode('a', 'Example.com', props_dict)
        self.assertEqual(node.to_html(), f'<a{props_text}>Example.com</a>')

class TestParentNode(unittest.TestCase):
    def test_to_html_with_children(self):
        child_node = LeafNode('span', 'child')
        parent_node = ParentNode('div', [child_node])
        self.assertEqual(parent_node.to_html(), '<div><span>child</span></div>')

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode('b', 'grandchild')
        child_node = ParentNode('span', [grandchild_node])
        parent_node = ParentNode('div', [child_node])
        self.assertEqual(
            parent_node.to_html(),
            '<div><span><b>grandchild</b></span></div>',
        )

class TestTextToHML(unittest.TestCase):
    def test_text(self):
        node = TextNode("This is a text node", TextType.TEXT)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")

    def test_bold(self):
        node = TextNode("bold text", TextType.BOLD)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "b")
        self.assertEqual(html_node.value, "bold text")

    def test_paragraphs(self):
        md = """
This is **bolded** paragraph
text in a p
tag here

This is another paragraph with _italic_ text and `code` here

"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
        )

    def test_codeblock(self):
        md = """
```
This is text that _should_ remain
the **same** even with inline stuff
```
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><pre><code>This is text that _should_ remain\nthe **same** even with inline stuff\n</code></pre></div>",
        )

    def test_markdown_to_blocks(self):
        md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )



    def test_title_extractor(self):
        md = "# Title"
        self.assertEqual(extract_title(md), "Title")
        
        md = "# Title\nSome other text"
        self.assertEqual(extract_title(md), "Title")


