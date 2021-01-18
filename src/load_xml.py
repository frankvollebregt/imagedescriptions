import xml.etree.ElementTree as ET


def load_xml(xml_path):
    tree = ET.parse(xml_path)
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
                    res = recursive_read(c2, {'text': '', 'images': []})
                    res['text'] = " ".join(res['text'].split())
                    res['images'] = parse_images(res['images'])
                    return res
            break


# recursively reads the body of the book, returning its text as a string
def recursive_read(document, res):
    # handle all tags within bodymatter
    if strip_tag(document.tag) == 'bodymatter':
        for part in document:
            res = recursive_read(part, res)
    elif strip_tag(document.tag) == 'imggroup':
        res['images'].append(document)
    # process contents of headers
    elif 'h' in strip_tag(document.tag) and len(strip_tag(document.tag)) == 2:
        if len(document) > 0:
            for part in document:
                res = recursive_read(part, res)
        else:
            if document.text is not None:
                res['text'] = res['text'] + document.text
            if document.tail is not None:
                res['text'] = res['text'] + document.tail
    # handle all tags within a level
    elif 'level' in strip_tag(document.tag):
        for part in document:
            res = recursive_read(part, res)
    # process contents of paragraphs and other bodies of text
    elif strip_tag(document.tag) == 'p' or strip_tag(document.tag) == 'em' or strip_tag(document.tag) == 'byline':
        if document.text is not None:
            res['text'] = res['text'] + document.text
        if len(document) > 0:
            for part in document:
                res = recursive_read(part, res)
        if document.tail is not None:
            res['text'] = res['text'] + document.tail
    # skip over 'unknown' tags, but process their children where possible
    else:
        # print('encountered unhandled tag {}'.format(strip_tag(document.tag)))
        if len(document) > 0:
            for part in document:
                res = recursive_read(part, res)

    return res


def parse_images(images):
    res = []

    # each image group should have an img and may have a caption
    for image in images:
        obj = {}
        for child in image:
            if strip_tag(child.tag) == 'img':
                obj['src'] = child.attrib['src']
                obj['alt'] = child.attrib['alt']
            if strip_tag(child.tag) == 'caption':
                obj['caption'] = child.text
        res.append(obj)
    return res


def strip_tag(tag):
    if '}' in tag:
        tag = tag[tag.index('}') + 1:]
    return tag
