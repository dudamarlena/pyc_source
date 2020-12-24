# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/davidam/git/damenltk/source/app/stopwords.py
# Compiled at: 2019-10-30 01:06:48
# Size of source mod 2**32: 1470 bytes
import sys
from nltk import wordpunct_tokenize
from nltk.corpus import stopwords
from nltk.tokenize import sent_tokenize, word_tokenize

class StopWords(object):

    def remove(self, string):
        if not string:
            string = 'All work and no play makes jack dull boy. All work and no play makes jack a dull boy.'
        stopWords = set(stopwords.words('english'))
        words = word_tokenize(string)
        wordsFiltered = []
        for w in words:
            if w not in stopWords:
                wordsFiltered.append(w)

        return wordsFiltered