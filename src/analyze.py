import sys

from src.azure import analyze_azure, get_analysis, get_json_path
from src.similarity import extract_nouns, count_occurrences
from src.load_xml import load_xml


def analyze(xml_file):
    # read the daisy-XML text and images
    context = load_xml('../res/xml/{}'.format(xml_file))

    for image in context['images']:
        description = analyze_azure(image['src'])
        tags = get_analysis(get_json_path(image['src']))['tags']
        occtags = []

        # now for each tag, we want to know how many times it occurs in the text
        for tag in tags:
            occtags.append({
                'tag': tag['name'],
                'occ': count_occurrences(tag['name'], context['text'])
            })

        # also count the occurrences for the nouns that are already in the description
        nouns = extract_nouns(description)

        for noun in nouns:
            occtags.append({
                'tag': noun,
                'occ': count_occurrences(noun, context['text'])
            })

        # remove duplicates from the list of tags
        occtags = [dict(t) for t in {tuple(d.items()) for d in occtags}]

        # sort the list of tags, most occurrences first, then highest confidence first
        occtags = sorted(occtags, key=lambda k: k['occ'], reverse=True)
        print(occtags)
        print(description)

        # the first words in the occTags array are the most probable to be correct


if __name__ == '__main__':
    # pass the name of an xml file, in DTBook format, placed inside the res/xml folder, as argument to this
    # file to analyze it
    if len(sys.argv) > 1:
        print(sys.argv)
        analyze(sys.argv[1])
    else:
        # have some default file to analyze
        analyze('volcano.xml')
