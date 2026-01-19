from textnode import TextNode
from helpers import copy_static_to_public

def main():
    print("# hello world")
    text_node = TextNode("This is some anchor text", "link", "https://www.boot.dev")
    print(text_node)
    copy_static_to_public('static', 'public')

if __name__ == '__main__':
    main()
