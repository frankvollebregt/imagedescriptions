import os
import sys
import requests
import matplotlib.pyplot as plt
from PIL import Image
from io import BytesIO


def analyze_azure(image_path):
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

    # Set image_path to the local path of an image that you want to analyze.
    image_path = "../res/img/{}".format(image_path)

    # Read the image into a byte array
    image_data = open(image_path, "rb").read()
    headers = {'Ocp-Apim-Subscription-Key': subscription_key,
               'Content-Type': 'application/octet-stream'}
    params = {'visualFeatures': 'Categories,Description,Color'}

    # post a request to Azure, thereby analyzing the image
    response = requests.post(
        analyze_url, headers=headers, params=params, data=image_data)
    response.raise_for_status()

    # The 'analysis' object contains various fields that describe the image. The most
    # relevant (=highest confidence) caption for the image is obtained from the 'description' property.
    analysis = response.json()
    print(analysis)
    image_caption = analysis["description"]["captions"][0]["text"].capitalize()

    # Display the image and overlay it with the caption.
    image = Image.open(BytesIO(image_data))
    plt.imshow(image)
    plt.axis("off")
    _ = plt.title(image_caption, size="x-large", y=-0.1)
    plt.show()

    return image_caption


if __name__ == '__main__':
    analyze_azure('dog.jpg')
