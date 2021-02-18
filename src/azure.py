import os
import sys
import requests
import matplotlib.pyplot as plt
from PIL import Image
from io import BytesIO
import json


def analyze_azure(image_path):
    image_path = "../res/img/{}".format(image_path)
    analysis = None

    # if the result JSON file already exists, there's no need to consult Azure again
    json_path = "../res/img/{}".format(image_path.split('/')[-1].split('.')[0]+'.json')
    if os.path.exists(json_path):
        print('Analysis already exists!')
        analysis = get_analysis(json_path)
    else:
        print('First time analysis')
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

        # Read the image into a byte array
        image_data = open(image_path, "rb").read()
        headers = {'Ocp-Apim-Subscription-Key': subscription_key,
                   'Content-Type': 'application/octet-stream'}
        params = {'visualFeatures': 'Description,Tags'}

        # post a request to Azure, thereby analyzing the image
        response = requests.post(
            analyze_url, headers=headers, params=params, data=image_data)
        response.raise_for_status()

        # The 'analysis' object contains various fields that describe the image. The most
        # relevant (=highest confidence) caption for the image is obtained from the 'description' property.
        analysis = response.json()

        with open("../res/img/{}".format(image_path.split('/')[-1].split('.')[0]+'.json'), 'w') as file:
            # store analysis as JSON, as to not ask Azure again
            file.write(response.text)

    # show the result regardless
    image_caption = analysis["description"]["captions"][0]["text"].capitalize() + " (" + str(round(analysis["description"]["captions"][0]["confidence"], 3)) + ")"

    # Display the image and overlay it with the caption.
    image_data = open(image_path, "rb").read()
    image = Image.open(BytesIO(image_data))
    plt.imshow(image)
    plt.axis("off")
    _ = plt.title(image_caption, size="x-large", y=-0.1)
    plt.show()

    return image_caption


def get_analysis(json_path):
    with open(json_path, 'r') as file:
        return json.load(file)


def get_json_path(image_path):
    return "../res/img/{}".format(image_path.split('/')[-1].split('.')[0] + '.json')


if __name__ == '__main__':
        for f in os.listdir("C:\\Users\\fravo\\Documents\\Programmeren\\Master Thesis\\imagedescriptions\\res\\img\\reisgids\\"):
            print('### File {} ###'.format(f))
            analyze_azure('reisgids/{}'.format(f))
