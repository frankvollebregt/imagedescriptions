import os
import sys
import requests
import uuid


def translate_to_dutch(sentence):
    print('Translating {}'.format(sentence))

    if 'COMPUTER_TRANSLATION_SUBSCRIPTION_KEY' in os.environ:
        subscription_key = os.environ['COMPUTER_TRANSLATION_SUBSCRIPTION_KEY']
    else:
        print(
            "\nSet the COMPUTER_TRANSLATION_SUBSCRIPTION_KEY environment variable.\n**Restart your shell or IDE for changes to take effect.**")
        sys.exit()

    endpoint = 'https://api.cognitive.microsofttranslator.com/'

    analyze_url = endpoint + "translate"

    headers = {
        'Ocp-Apim-Subscription-Key': subscription_key,
        'Content-type': 'application/json',
        'X-ClientTraceId': str(uuid.uuid4())
    }

    params = {
        'api-version': '3.0',
        'from': 'en',
        'to': 'nl'
    }

    body = [{
        'text': sentence
    }]

    # post a request to Azure, thereby analyzing the image
    response = requests.post(
        analyze_url, headers=headers, params=params, json=body)
    response.raise_for_status()

    analysis = response.json()

    print('Translation {}'.format(analysis[0]['translations'][0]['text']))
    return analysis[0]['translations'][0]['text']


def lookup_translation(word):
    if word.find(' ') is not -1:
        print('not a single word')
        return -1
    else:
        if word == 'text':
            return 'tekst'
        elif word == 'sign':
            return 'bord'
        else:
            return -1


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print('Usage: python translate.py "sentence"')
        exit(0)

    sentence_to_translate = sys.argv[1]
    translation = translate_to_dutch(sentence_to_translate)
