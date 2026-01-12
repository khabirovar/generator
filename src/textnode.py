from enum import Enum

class TextType(Enum):
    PLAIN_TEXT = 'plain text'
    BOLD_TEXT = 'bold text'
    ITALIC_TEXT = 'italic text'
    CODE_TEXT = 'code text'
    LINK_TEXT = 'link text'
    IMAGE_TEXT = 'image text'

class TextNode():
    def __init__(self, text, text_type, url):
        self.text = text
        self.text_type = text_type
        self.url = url

    def __eq__(self, other):
        condition = self.text == other.text
        condition = condition and self.text_type == other.text_type
        condition = condition and self.url == self.url
        if condition:
            return True
        return False

    def __repr__(self):
        return f'TextNode({self.text}, {self.text_type}, {self.url})'

