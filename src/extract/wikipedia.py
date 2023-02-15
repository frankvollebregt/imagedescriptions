import pandas as pd
import random
from src.util.imageincontext import ImageInContext


# Extract images and their respective contexts from a given Wikipedia WIT data file
# See https://github.com/google-research-datasets/wit
def extract_wikipedia(filename):
    data = pd.read_csv(filename, sep='\t', compression='gzip')
    nl_data = data.loc[data['language'] == 'nl']
    stripped_data = nl_data.loc[~(
            nl_data['page_title'].str.contains('Lijst')
            | nl_data['context_page_description'].str.contains('gemeente')
            | nl_data['context_page_description'].str.contains('county')
            | nl_data['context_page_description'].str.contains('County')
            | nl_data['context_page_description'].str.contains('parish'))]
    stripped_data = stripped_data[stripped_data['section_title'].isnull()]
    stripped_data = stripped_data[~stripped_data['caption_alt_text_description'].isnull()]

    # for now, a random article
    agreed = False
    while not agreed:
        print('getting article...')
        index = random.randint(0, len(stripped_data) - 1)
        entry = stripped_data.iloc[index]
        res = input('is it OK to use document with title {}?\nThe context has {} words.\nurl: {}\n (y/n)'.format(entry['page_title'], len(entry['context_page_description'].split()), entry['page_url']))
        if res == 'y' or res == 'yes':
            agreed = True

    return ImageInContext(
        entry['image_url'],
        entry['context_page_description'],
        entry['page_title'],
        entry['caption_alt_text_description'],
        entry['page_url']
    )
