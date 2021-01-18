import xml.etree.ElementTree as ET


def read(filename):
    tree = ET.parse(filename)
    doc = tree.getroot()

    if 'dtbook' not in doc.tag:
        print('Not a valid dtbook file: {}'.format(doc.tag))
        exit(0)

    # should contain 'head' and 'book'
    for c1 in doc:
        # dtbook should contain book
        if strip_tag(c1.tag) == 'book':
            book = c1

            for c2 in book:
                tag = strip_tag(c2.tag)
                # book should contain frontmatter and bodymatter
                if tag == 'frontmatter':
                    for c3 in c2:
                        if strip_tag(c3.tag) == 'doctitle':
                            print(c3.text)
                elif tag == 'bodymatter':
                    print('body matter')
                    res = recursive_read(c2, '')
                    print(res)
                    read_images(c2)
            break


# recursively reads the body of the book, returning its text as a string
def recursive_read(document, text):
    # handle all tags within bodymatter
    if strip_tag(document.tag) == 'bodymatter':
        for part in document:
            text = recursive_read(part, text)
    # process contents of headers
    elif 'h' in strip_tag(document.tag) and len(strip_tag(document.tag)) == 2:
        if len(document) > 0:
            for part in document:
                text = recursive_read(part, text)
        else:
            if document.text is not None:
                text += document.text
            if document.tail is not None:
                text += document.tail
    # handle all tags within a level
    elif 'level' in strip_tag(document.tag):
        for part in document:
            text = recursive_read(part, text)
    # process contents of paragraphs and other bodies of text
    elif strip_tag(document.tag) == 'p' or strip_tag(document.tag) == 'em' or strip_tag(document.tag) == 'byline':
        if document.text is not None:
            text += document.text
        if len(document) > 0:
            for part in document:
                text = recursive_read(part, text)
        if document.tail is not None:
            text += document.tail
    # skip over 'unknown' tags, but process their children where possible
    else:
        print('encountered unhandled tag {}'.format(strip_tag(document.tag)))
        if len(document) > 0:
            for part in document:
                text = recursive_read(part, text)

    return text


def read_images(document):
    images = document.findall('imggroup')

    print(images)


def strip_tag(tag):
    if '}' in tag:
        tag = tag[tag.index('}') + 1:]
    return tag
