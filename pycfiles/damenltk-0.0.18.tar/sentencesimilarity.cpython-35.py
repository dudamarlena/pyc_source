# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/davidam/git/damenltk/source/app/sentencesimilarity.py
# Compiled at: 2019-10-30 01:06:48
# Size of source mod 2**32: 1851 bytes
from nltk.corpus import brown, stopwords
from nltk.cluster.util import cosine_distance

class SentenceSimilarity(object):

    def sentence_similarity(self, sent1, sent2, stopwords=None):
        if stopwords is None:
            stopwords = []
        sent1 = [w.lower() for w in sent1]
        sent2 = [w.lower() for w in sent2]
        all_words = list(set(sent1 + sent2))
        vector1 = [
         0] * len(all_words)
        vector2 = [0] * len(all_words)
        for w in sent1:
            if w in stopwords:
                pass
            else:
                vector1[all_words.index(w)] += 1

        for w in sent2:
            if w in stopwords:
                pass
            else:
                vector2[all_words.index(w)] += 1

        return 1 - cosine_distance(vector1, vector2)


s = SentenceSimilarity()
print(s.sentence_similarity('Hola Mundo', 'Hola Mundo Crue'))