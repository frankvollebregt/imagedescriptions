import os
import sys
import requests
import cv2
from skimage import io
from src.util.azureresult import AzureResult


def analyze_azure(image_url):
    analysis = None

    # Add your (Azure) Computer Vision subscription key and endpoint to your environment variables.
    if 'COMPUTER_VISION_SUBSCRIPTION_KEY' in os.environ:
        subscription_key = os.environ['COMPUTER_VISION_SUBSCRIPTION_KEY']
    else:
        print("\nSet the COMPUTER_VISION_SUBSCRIPTION_KEY environment variable.\n**Restart your shell or IDE for changes to take effect.**")
        sys.exit()

    if 'COMPUTER_VISION_ENDPOINT' in os.environ:
        endpoint = os.environ['COMPUTER_VISION_ENDPOINT']
    else:
        # if no endpoint is set, just use the default endpoint
        endpoint = 'https://image-description.cognitiveservices.azure.com/'

    analyze_url = endpoint + "vision/v3.1/analyze"
    params = {'visualFeatures': 'Categories,Description,Color,Tags'}

    # post a request to Azure, thereby analyzing the image
    print('posting to azure with url: {}'.format(image_url))

    image = io.imread(image_url)
    # encode as binary
    image_data = cv2.imencode('.jpg', image)[1].tostring()

    headers = {'Ocp-Apim-Subscription-Key': subscription_key,
               'Content-Type': 'application/octet-stream'}
    response = requests.post(
        analyze_url, headers=headers, params=params, data=image_data
    )
    response.raise_for_status()

    # The 'analysis' object contains various fields that describe the image. The most
    # relevant (=highest confidence) caption for the image is obtained from the 'description' property.
    analysis = response.json()
    description = analysis['description']['captions'][0]
    tags = [{'tag': x['name'], 'score': x['confidence']} for x in analysis['tags']]
    if len(tags) > 5:
        tags = tags[0:5]
    result = AzureResult(description['text'], tags)

    return result


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print('Usage: python analyze_azure.py url')
        exit(0)
    result = analyze_azure(sys.argv[1])
    print(result.description)
    print(result.tags)
