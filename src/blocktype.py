import re
from enum import Enum


class BlockType(Enum):
    PARAGRAPH = 'paragraph'
    HEADING = 'heading'
    CODE = 'code'
    QUOTE = 'quote'
    UNORDERED_LIST = 'unordered_list'
    ORDERED_LIST = 'ordered_list'

def block_to_block_type(block):
    lines = block.split('\n')
    if len(re.findall( r'^#{1,6} ', lines[0])) > 0:
        return BlockType.HEADING
    elif len(lines) > 1 and lines[0].startswith('```') and lines[-1].startswith('```'):
        return BlockType.CODE
    elif earch_line_start_with(lines, '> '):
        return BlockType.QUOTE
    elif earch_line_start_with(lines, '- '):
        return BlockType.UNORDERED_LIST
    elif lines[0].startswith('1. '):
        count = 1
        for line in lines:
            prefix = f'{count}. '
            if not line.startswith(prefix):
                return BlockType.PARAGRAPH
            count += 1
        return BlockType.ORDERED_LIST
    return BlockType.PARAGRAPH

def earch_line_start_with(lines, prefix):
    for line in lines:
        if not line.startswith(prefix):
            return False
    return True

