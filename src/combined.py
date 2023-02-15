import sys
import json
from azure.azure import analyze_azure
from extract.extract import extract
from keywords import extract_keywords_exportable
from translate import translate_to_dutch, lookup_translation


def append_to_json(data, path):
    with open(path, 'r+') as file:
        current_json = json.load(file)
        print(current_json)
        current_json.append(data)
        print('new json is {}'.format(current_json))
        file.seek(0)
        file.write(json.dumps(current_json))
        file.truncate()
    return


def full_analysis(filename):
    image_in_context = extract(filename)
    print(image_in_context)
    url = image_in_context.image
    azure_result = analyze_azure(url)
    print(azure_result)

    keywords = extract_keywords_exportable(image_in_context.text)

    dutch_description = translate_to_dutch(azure_result.description)

    for tag_obj in azure_result.tags:
        word = tag_obj['tag']
        print(word)

        # consult the look-up table before asking Azure
        lookup_word = lookup_translation(word)
        if lookup_word == -1:
            dutch_word = translate_to_dutch(word)
            tag_obj['tag'] = dutch_word
        else:
            tag_obj['tag'] = lookup_word

            # now we need to end up with a JSON dictionary that corresponds with the data required in the front end
    result_object = {
        "ctx_title": image_in_context.title,
        "ctx_url": image_in_context.page_url,
        "ctx_caption": image_in_context.caption,
        "ctx": image_in_context.text,
        "ctx_tags": keywords,
        "img": image_in_context.image,
        "img_caption": dutch_description,
        "img_tags": azure_result.tags
    }

    return result_object


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print('Usage: python combined.py [filename]')
        exit(0)
    res = full_analysis(sys.argv[1])

    # Appends to the JSON object located in the webpage project. Update the path accordingly when running this code
    append_to_json(res, 'image_description_tool/data.json')
