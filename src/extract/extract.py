import sys
from src.extract.extract_daisy import extract_daisy
from src.extract.wikipedia import extract_wikipedia
from src.keywords import extract_keywords


def extract(filename):
    extension = filename.lower().split('.')[-1]
    print('Extracting data from file {} with extension {}'.format(filename, extension))

    if extension == 'xml':
        return extract_daisy(filename)
    elif extension == 'tsv' or extension == 'gz':
        return extract_wikipedia(filename)
    else:
        print('Unsupported file extension: {}'.format(extension))
        return None


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print('Usage: python extract.py filename')
        exit(0)
    result = extract(sys.argv[1])
    print(result)

    constrained = result.get_constrained_text(250)
    print(constrained)
    print(extract_keywords(constrained))
