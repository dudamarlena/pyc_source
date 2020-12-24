# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-armv7l/egg/FSTA/fred_language_analyser.py
# Compiled at: 2016-12-30 04:39:46
from nltk.tokenize import WordPunctTokenizer
from nltk.corpus import stopwords
from nltk.metrics import *
import itertools
from FSTA.language_analyser import *

class fred_language_analyser(language_analyser):
    """ a own analyser based on nltk with an asshole algoritme 
        """

    def __init__(self, language='french'):
        """Initialisation
                        language        :       'french'
                """
        self.tokenizer = WordPunctTokenizer()
        self.stopwords = set(stopwords.words(language))
        self.stopwords.add("'")

    def text_to_vector(self, text):
        tokens = self.tokenizer.tokenize(text)
        tokens = [ token for token in tokens if token.lower() not in self.stopwords ]
        return tokens

    def distance(self, text1, text2):
        v1 = self.text_to_vector(text1)
        v2 = self.text_to_vector(text2)
        v1 = v1[0:6]
        v2 = v2[0:6]
        n = max(len(v1), len(v2))
        if len(v1) > len(v2):
            v1, v2 = v2, v1
        v1_1 = v1 + [None] * (n - len(v1))
        distance = 99
        for v1_2 in itertools.permutations(v1_1):
            d_mot = 0
            for i in range(n):
                try:
                    d_mot += (6 - min(6, edit_distance(v1_2[i], v2[i]))) ** 2
                except:
                    d_mot += 1

            d_mot = 6 * n ** 0.5 - d_mot ** 0.5
            v1_3 = []
            debut = True
            for m in v1_2:
                if m or not debut:
                    debut = False
                    v1_3.append(m)

            v1_4 = []
            debut = True
            for i in range(len(v1_3) - 1, -1, -1):
                if v1_3[i] or not debut:
                    debut = False
                    v1_4.append(v1_3[i])

            d_perm = len(v1_4) - len(v1)
            l = []
            for m in list(filter(lambda x: x, v1_4)):
                l.append(v1.index(m))

            for i in range(len(l) - 1):
                if l[i] < l[(i + 1)]:
                    d_perm += 3

            distance = min(distance, (d_mot ** 2 + d_perm ** 2) ** 0.5)

        return distance