from nltk.tokenize import word_tokenize
from nltk import pos_tag


def extract_nouns(string):
    is_noun = lambda pos: pos[:2] == 'NN'

    words = word_tokenize(string)
    nouns = [word for (word, pos) in pos_tag(words) if is_noun(pos)]

    return nouns


def count_occurrences(target, text):
    # first, split the text in a list of words
    words = word_tokenize(text)

    count = 0
    for word in words:
        if word == target:
            count += 1

    return count
