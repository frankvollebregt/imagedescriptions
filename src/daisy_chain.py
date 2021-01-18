from src.load_xml import load_xml
from src.azure import analyze_azure


# 1. Extract the image and corresponding text from the (DTBook) XML file
# 2. Then use Azure (which could be exchanged for a different service to automatically analyze the image
#    and obtain a baseline description
#
#  Note that this is all in English, whereas actual documents will be in Dutch
def main():
    context = load_xml('../res/xml/amsterdampolice.xml')

    for image in context['images']:
        description = analyze_azure(image['src'])
        image['description'] = description

    print(context)


if __name__ == '__main__':
    main()
