from textnode import TextNode

def main():
    print("# hello world")
    text_node = TextNode("This is some anchor text", "link", "https://www.boot.dev")
    print(text_node)

if __name__ == '__main__':
    main()
