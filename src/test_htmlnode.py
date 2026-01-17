import unittest

from htmlnode import HTMLNode, LeafNode, ParentNode, text_node_to_html_node
from textnode import TextType, TextNode


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
