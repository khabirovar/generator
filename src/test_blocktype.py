import unittest
from blocktype import *


class TestBlockNode(unittest.TestCase):
    def test_simple_blocknode(self):
        self.assertEqual(block_to_block_type("This is paragraph"), BlockType.PARAGRAPH)
        self.assertEqual(block_to_block_type("## This is heading"), BlockType.HEADING)
        self.assertEqual(block_to_block_type("```\n This is code block \n```"), BlockType.CODE)
        self.assertEqual(block_to_block_type("> This is quote\n> This is quote"), BlockType.QUOTE)
        self.assertEqual(block_to_block_type("- This is unordered list\n- This is unordered list"), BlockType.UNORDERED_LIST)
        self.assertEqual(block_to_block_type("1. This is ordered list\n2. This is ordered list"), BlockType.ORDERED_LIST)

