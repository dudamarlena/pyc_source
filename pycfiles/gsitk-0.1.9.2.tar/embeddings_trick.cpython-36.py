# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/src/app/gsitk/preprocess/embeddings_trick.py
# Compiled at: 2018-02-19 13:40:23
# Size of source mod 2**32: 931 bytes
"""
Implements the embeddings trick. Substitutes a word outside of vocabulary for
the most close to it. It provides an enhancement of vocabulary.
"""
from sklearn.base import TransformerMixin
from gsitk.features.word2vec import Word2VecFeatures

class EmbeddingsTricker(TransformerMixin):

    def __init__(self, model_path, w2v_format, vocabulary):
        w2v = Word2VecFeatures(model_path, w2v_format)
        self.wv = w2v.model
        self.vocab = set(vocabulary)

    def fit(self, X, y=None):
        return self

    def closest_word(self, w):
        return self.wv.most_similar(w, topn=1)[0][0]

    def transform(self, X, y=None):
        for i, x_i in enumerate(X):
            for j, word in enumerate(x_i):
                if word not in self.vocab:
                    closest = self.closest_word(word)
                    X[i][j] = closest

        return X