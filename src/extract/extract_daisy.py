import xml.etree.ElementTree as ET
from src.util.imageincontext import ImageInContext


# Extract images and their respective contexts from a given Daisy DTBook file
# By traversing the XML tree
def extract_daisy(filename):
    tree = ET.parse(filename)
    doc = tree.getroot()

    if 'dtbook' not in doc.tag:
        print('Not a valid DTBook file: {}'.format(doc.tag))
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
                    res = recursive_read(c2)
                    return res
            break

    print('Extract Daisy is not implemented yet!')
    return None


# recursively reads the body of the book, returning its text as a string
def recursive_read(document, image_in_context=ImageInContext()):
    # handle all tags within bodymatter
    if strip_tag(document.tag) == 'bodymatter':
        for part in document:
            image_in_context = recursive_read(part, image_in_context)
    # process contents of headers
    elif 'h' in strip_tag(document.tag) and len(strip_tag(document.tag)) == 2:
        if len(document) > 0:
            for part in document:
                image_in_context = recursive_read(part, image_in_context)
        else:
            if document.text is not None:
                image_in_context.add_title(document.text)
            if document.tail is not None:
                image_in_context.add_title(document.tail)
    # handle all tags within a level
    elif 'level' in strip_tag(document.tag):
        for part in document:
            image_in_context = recursive_read(part, image_in_context)
    # process contents of paragraphs and other bodies of text
    elif strip_tag(document.tag) == 'p' or strip_tag(document.tag) == 'em' or strip_tag(document.tag) == 'byline':
        if document.text is not None:
            image_in_context.add_text(document.text)
        if len(document) > 0:
            for part in document:
                image_in_context = recursive_read(part, image_in_context)
        if document.tail is not None:
            image_in_context.add_text(document.tail)
    elif strip_tag(document.tag) == 'caption':
        if document.text is not None:
            image_in_context.add_caption(document.text)
        if document.tail is not None:
            image_in_context.add_caption(document.tail)
    elif strip_tag(document.tag) == 'img':
        if document.attrib is not None and document.attrib['src'] is not None:
            image_in_context.add_image(document.attrib['src'])
    # skip over 'unknown' tags, but process their children where possible
    else:
        print('encountered unhandled tag {}'.format(strip_tag(document.tag)))
        if len(document) > 0:
            for part in document:
                image_in_context = recursive_read(part, image_in_context)

    return image_in_context


def strip_tag(tag):
    if '}' in tag:
        tag = tag[tag.index('}') + 1:]
    return tag
