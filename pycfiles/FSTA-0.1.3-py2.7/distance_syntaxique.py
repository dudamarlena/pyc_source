# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-armv7l/egg/FSTA/distance_syntaxique.py
# Compiled at: 2016-12-25 04:43:34
from nltk.tokenize import WordPunctTokenizer
tokenizer = WordPunctTokenizer()
from nltk.corpus import stopwords
french_stopwords = set(stopwords.words('french'))
french_stopwords.add("'")
from nltk.metrics import *
import itertools

def text_to_vector(text):
    tokens = tokenizer.tokenize(text)
    tokens = [ token for token in tokens if token.lower() not in french_stopwords ]
    return tokens


def distance_syntaxique(text1, text2):
    v1 = text_to_vector(text1)
    v2 = text_to_vector(text2)
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