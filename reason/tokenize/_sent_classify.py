import pickle

import numpy as np
from nltk.corpus import treebank_raw
from sklearn.preprocessing import OneHotEncoder
from sklearn.feature_extraction.text import CountVectorizer
#from nltk import classify

from reason.classify import NaiveBayesClassifier


def train_classifier():
    dataset = _get_dataset()
    classifier = NaiveBayesClassifier.train(dataset)
    #with open('sent_classifier.pickle', 'wb') as f:
    #    pickle.dump(classifier, f)


def _evaluate_classifier():
    dataset = _get_dataset()
    size = int(len(dataset) * 0.1)
    train_set, test_set = dataset[size:], dataset[:size]

    #classifier = NaiveBayesClassifier.train(train_set)
    #return classify.accuracy(classifier, test_set)

    classifier = NaiveBayesClassifier()
    classifier.train(train_set)
    print(classifier.classify(test_set[0]))


def _get_dataset():
    sents = treebank_raw.sents()
    tokens = list()
    boundaries = set()
    offset = 0

    for sent in sents:
        tokens.extend(sent)
        offset += len(sent)
        boundaries.add(offset - 1)

    ohe = OneHotEncoder()
    cv = CountVectorizer()

    feature_sets = [
        (punc_features(tokens, i, ohe, cv), (i in boundaries))
        for i in range(1, len(tokens) - 1)
        if tokens[i] in '.?!'
    ]

    return feature_sets


def punc_features(tokens, i, ohe, cv):
    punctuation = np.array([tokens[i]])
    encoded_punctuation = ohe.fit_transform(punctuation.reshape(-1, 1))
    prev_word = np.array([tokens[i - 1].lower()])
    encoded_prev_word = ohe.fit_transform(prev_word.reshape(-1, 1))
    return {
        'next_word_capitalized': tokens[i+1][0].isupper(),
        'punctuation': encoded_punctuation,
        'prev_word': encoded_prev_word,
        'prev_word_is_one_char': len(tokens[i-1]) == 1,
    }


if __name__ == '__main__':
    _evaluate_classifier()
