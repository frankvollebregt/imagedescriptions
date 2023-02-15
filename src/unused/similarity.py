from nltk.tokenize import word_tokenize
from nltk import pos_tag
from nltk.corpus import wordnet

# Some experimentation that was not used in the final work, but may still be of interest
# Some functions to find similar words

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


def compute_similarity(noun, tag):
    syns = wordnet.synsets(noun)
    tagsyn = wordnet.synsets(tag)[0]

    # see if any of the synonyms is the tag
    syns_sim = [tagsyn.wup_similarity(syns[index]) for index in range(len(syns))]
    syns_sim = [sim for sim in syns_sim if sim is not None]
    # return the highest score
    return max(syns_sim)
