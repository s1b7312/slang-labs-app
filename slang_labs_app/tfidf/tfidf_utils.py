
import re
import string

from typing import List, Dict
from collections import Counter


def remove_punctuations(s: str) -> str:
    # remove "apostrophe s"
    # s.replace('\'s', ' ')

    # remove punctuations
    s = re.sub(f'[{string.punctuation}]', ' ', s)

    return s


def get_word_counts(doc: List[str]) -> Dict[str, int]:
    """
    Get word counts for a document
    :param doc: list of processed tokens
    :return:
    """
    counts = Counter(doc)
    return counts


def get_vocab(sentences: List[str]) -> Dict[str, int]:

    vocab = {}
    index = 0

    for s in sentences:
        s = remove_punctuations(s)
        # stemming / lemmatization etc.

        s = s.split()
        for w in s:
            if w not in vocab:
                vocab[w] = index
                index += 1

    return vocab
