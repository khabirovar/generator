import re
from textnode import TextType, TextNode


def split_nodes_delimiter(old_names, delimiter, text_type):
    new_names = list()
    for name in old_names:
        if name.text_type != TextType.TEXT:
            new_names.append(name)
            continue
        sections = name.text.split(delimiter)
        if len(sections) % 2 == 0:
            raise ValueError('invalid markdown')
        split_nodes = list()
        for i in range(len(sections)):
            if sections[i] == '':
                continue
            if i % 2 == 0:
                split_nodes.append(TextNode(sections[i], TextType.TEXT))
            else:
                split_nodes.append(TextNode(sections[i], text_type))
        new_names.extend(split_nodes)
    return new_names

def extract_markdown_images(text):
    return re.findall(r'!\[([^\[\]]*)\]\(([^\(\)]*)\)', text)

def extract_markdown_links(text):
    return re.findall(r'(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)', text)

def split_nodes_image(old_names):
    new_names = list()
    for name in old_names:
        images = extract_markdown_images(name.text)
        line = name.text[:]
        for img in images:
            alt = img[0]
            url = img[1]
            before, after = line.split(f'![{alt}]({url})', 1)
            if before != '':
                new_names.append(TextNode(before, name.text_type))
            new_names.append(TextNode(alt, TextType.IMAGE, url))
            line = after
        if len(line) > 0:
            new_names.append(TextNode(line, name.text_type))
    return new_names

def split_nodes_link(old_names):
    new_names = list()
    for name in old_names:
        if name.text_type == TextType.IMAGE:
            new_names.append(name)
            continue
        links = extract_markdown_links(name.text)
        line = name.text[:]
        for lnk in links:
            alt = lnk[0]
            url = lnk[1]
            before, after = line.split(f'[{alt}]({url})', 1)
            if before != '':
                new_names.append(TextNode(before, name.text_type))
            new_names.append(TextNode(alt, TextType.LINK, url))
            line = after
        if len(line) > 0:
            new_names.append(TextNode(line, name.text_type))
    return new_names

def text_to_textnodes(text):
    names = split_nodes_delimiter([TextNode(text,TextType.TEXT)], '**', TextType.BOLD)
    names = split_nodes_delimiter(names, '_', TextType.ITALIC)
    names = split_nodes_delimiter(names, '`', TextType.CODE)
    names = split_nodes_image(names)
    names = split_nodes_link(names)
    return names

def markdown_to_blocks(makrdown):
    blocks = makrdown.split('\n\n')
    blocks = [item.strip() for item in blocks]
    return blocks

