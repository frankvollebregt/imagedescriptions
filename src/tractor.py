from src.azure import analyze_azure, get_analysis, get_json_path
from src.similarity import extract_nouns, count_occurrences
from src.load_xml import load_xml

# read the daisy-XML text and images
context = load_xml('../res/xml/volcano.xml')

for image in context['images']:
    description = analyze_azure(image['src'])
    tags = get_analysis(get_json_path(image['src']))['tags']
    occTags = []

    # now for each tag, we want to know how many times it occurs in the text
    for tag in tags:
        occTags.append({
            'tag': tag['name'],
            'occ': count_occurrences(tag['name'], context['text'])
        })

    # also count the occurrences for the nouns that are already in the description
    nouns = extract_nouns(description)

    for noun in nouns:
        occTags.append({
            'tag': noun,
            'occ': count_occurrences(noun, context['text'])
        })

    # remove duplicates from the list of tags
    occTags = [dict(t) for t in {tuple(d.items()) for d in occTags}]

    # sort the list of tags, most occurrences first, then highest confidence first
    occTags = sorted(occTags, key=lambda k: k['occ'], reverse=True)
    print(occTags)
    print(description)

    # the first words in the occTags array are the most probable to be correct

