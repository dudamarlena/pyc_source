# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/hadoop/nlpy/nlpy/rep/word2vec.py
# Compiled at: 2014-11-06 00:32:57
from gensim.models.word2vec import *
from nlpy.util import external_resource

class Word2VecRepresentation:

    def __init__(self, model_path=None):
        """
      :type model_path: str
      """
        if not model_path:
            model_path = external_resource('rep/GoogleNews-vectors-negative300.bin.gz')
        self._model = Word2Vec.load_word2vec_format(model_path, binary=True)

    def similar_words(self, word):
        """
        :type word: str
        :rtype: list of str
        """
        similar_words = self._model.most_similar(positive=[word])
        return zip(*similar_words)[0]

    def similarity(self, word1, word2):
        """
        :type word: str
        :rtype: float
        """
        return self._model.similarity(word1, word2)

    def scored_similar_words(self, word, N=1000):
        """
        :type word: str
        :type N: int
        :rtype: list of (str, float)
        """
        return self._model.build_vocab().most_similar(positive=[word], topn=N)