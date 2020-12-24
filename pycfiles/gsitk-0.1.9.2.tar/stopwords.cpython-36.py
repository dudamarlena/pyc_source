# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/src/app/gsitk/preprocess/stopwords.py
# Compiled at: 2018-06-29 11:33:59
# Size of source mod 2**32: 835 bytes
"""
Remove stopwords.
"""
from sklearn.base import TransformerMixin
from nltk.corpus import stopwords

class StopWordsRemover(TransformerMixin):

    def __init__(self, type='nltk', language='english'):
        self.type = type
        self.language = language
        if self.type == 'nltk':
            self.stop_words = stopwords.words(self.language)
        else:
            raise NotImplementedError

    def fit(self, X, y=None, **fit_params):
        return self

    def remove_stopwords(self, tokens, stop_words):
        return ' '.join([tok for tok in tokens if tok not in stop_words])

    def transform(self, X, y=None, **fit_params):
        transformed = []
        for x in X:
            tokens = self.remove_stopwords(x.split(' '), self.stop_words)
            transformed.append(tokens)

        return transformed