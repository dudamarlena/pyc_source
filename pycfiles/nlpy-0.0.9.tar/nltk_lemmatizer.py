# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/hadoop/nlpy/nlpy/basic/nltk_lemmatizer.py
# Compiled at: 2014-11-06 19:43:44
from nltk.stem.wordnet import WordNetLemmatizer

class NLTKEnglishLemmatizer(object):

    def __init__(self):
        self._lemmatizer = WordNetLemmatizer()

    def lemmatize(self, word, pos='n'):
        """
        :type word: str
        :rtype: str
        """
        word = word.decode('utf-8')
        return self._lemmatizer.lemmatize(word, pos)