# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/otazkovac/helpers.py
# Compiled at: 2015-09-22 17:17:30
from sklearn.externals import joblib

def tokenize(input):
    lemmas = input.split()
    tokens = [ list(reversed(lemma.split('/'))) for lemma in lemmas ]
    tokens = list(part for token in tokens for part in token)
    return tokens


def special_unigrams_bigrams(text):
    tokens = tokenize(text)
    for n in range(1, 4):
        for i in range(0, len(tokens) - n):
            yield (' ').join(tokens[i:i + n + 1])

    if len(tokens) > 4:
        yield (' ').join(tokens[:2] + tokens[len(tokens) - 2:])
        yield (' ').join(tokens[:2] + tokens[len(tokens) - 1:])
        yield (' ').join(tokens[:1] + tokens[len(tokens) - 2:])
        yield (' ').join(tokens[:1] + tokens[len(tokens) - 1:])


def load_pipeline(path):
    return joblib.load(path)