import sys

from src.azure import analyze_azure, get_analysis, get_json_path
from src.similarity import extract_nouns, count_occurrences, compute_similarity
from src.load_xml import load_xml
from nltk.corpus import wordnet


def analyze(xml_file):
    # read the daisy-XML text and images
    context = load_xml('../res/xml/{}'.format(xml_file))

    for image in context['images']:
        description = analyze_azure(image['src'])
        tags = get_analysis(get_json_path(image['src']))['tags']
        print(tags)
        tagsWithSyns = [wordnet.synsets(tag['name']) for tag in tags]
        tagsWithSyns = [item for sublist in tagsWithSyns for item in sublist]
        tagsWithSyns = [item.name().split('.')[0].replace('_', ' ') for item in tagsWithSyns]
        tagsWithSyns = list(set(tagsWithSyns))
        print('with syns {}'.format(tagsWithSyns))

        occtags = []

        # now for each tag, we want to know how many times it occurs in the text
        for tag in tagsWithSyns:
            occtags.append({
                'tag': tag,
                'occ': count_occurrences(tag, context['text'])
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

        # only consider alternatives that actually occur in the text
        occtags = [tag for tag in occtags if tag['occ'] > 0]

        alternatives = {}

        # now for each tag, find out which noun it'll most likely be replacing
        for tag in occtags:
            # find out which noun this tag is a candidate replacement for
            highestsim = 0
            highestnoun = None
            for noun in nouns:
                sim = compute_similarity(noun, tag['tag'])

                if sim > highestsim:
                    highestsim = sim
                    highestnoun = noun

            if highestnoun in alternatives:
                alternatives[highestnoun].append(tag)
            else:
                alternatives[highestnoun] = [tag]

        # the first words in the occTags array are the most probable to be correct
        print(alternatives)


if __name__ == '__main__':
    # pass the name of an xml file, in DTBook format, placed inside the res/xml folder, as argument to this
    # file to analyze it
    if len(sys.argv) > 1:
        print(sys.argv)
        analyze(sys.argv[1])
    else:
        # have some default file to analyze
        analyze('volcano.xml')
