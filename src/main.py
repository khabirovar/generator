from textnode import TextNode
from htmlnode import copy_static_to_public, generate_page, generate_pages_recursive

def main():
    copy_static_to_public('static', 'public')
    # generate_page('content/index.md', 'template.html', 'public/index.html')
    generate_pages_recursive('content', 'template.html', 'public')


if __name__ == '__main__':
    main()
