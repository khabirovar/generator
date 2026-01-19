import sys
from textnode import TextNode
from htmlnode import copy_static_to_public, generate_page, generate_pages_recursive



def main():
    copy_static_to_public('static', 'docs')
    # generate_page('content/index.md', 'template.html', 'public/index.html')
    print(f"Debug: SYS_ARGV={sys.argv}")
    basepath = '/'
    if len(sys.argv) >= 2:
        basepath = sys.argv[1]
    print(f"Debug: basepath={basepath}")
    generate_pages_recursive('content', 'template.html', 'docs', basepath)
    

if __name__ == '__main__':
    main()
