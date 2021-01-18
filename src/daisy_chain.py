from azure import analyze_azure
from load_xml import load_xml


def main():
    context = load_xml('amsterdampolice.xml')

    for image in context['images']:
        description = analyze_azure(image['src'])
        image['description'] = description

    print(context)


if __name__ == '__main__':
    main()