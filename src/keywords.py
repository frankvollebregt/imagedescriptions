from keybert import KeyBERT
from flair.embeddings import TransformerDocumentEmbeddings


def extract_keywords(text):
    bertje = TransformerDocumentEmbeddings('GroNLP/bert-base-dutch-cased')
    kw_model = KeyBERT(model=bertje)

    # get the stop words
    with open('res/stopwords.txt') as file:
        stop_words = file.readlines()
        stop_words = [word.strip() for word in stop_words]
        # now use the keyword model to extract keywords
        res = kw_model.extract_keywords(text, keyphrase_ngram_range=(1, 1), stop_words=stop_words)
        return res


def extract_keywords_exportable(text):
    raw_keywords = extract_keywords(text)
    print(raw_keywords)
    return [{'tag': x[0], 'score': x[1]} for x in raw_keywords]


if __name__ == '__main__':
    text = """
        Paste your text for analysis here
    """
    print(extract_keywords(text))
