# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-armv7l/egg/FSTA/language_analyser.py
# Compiled at: 2017-01-01 13:17:47
import math

class language_analyser(object):
    """ A basic syntaxic analyser class for FSTA
        """

    def getFingerprint(self, text):
        """ Get the Fingerprint of a text
                """
        return text

    def distance(self, text1, text2):
        """ Return the distance between two texts
                """
        if type(self) == language_analyser:
            return abs(len(text1) - len(text2))
        else:
            return (-10 * math.log(self.compare(text1, text2))) ** 0.5

    def compare(self, text1, text2):
        """ Compare two text ;
                        0       :       low semantic similarity
                        0.5     :       medium semantic similarity
                        1       :       high semantic similarity
                """
        return math.exp(-self.distance(text1, text2) ** 2 / 10)

    def compare_texts(self, text, texts):
        """Compare a text with a list of texts and return a tuple 
                        (the index,  the cosine similarity) of the neerer text
                        OBSOLETE
                """
        cosines = []
        for t in texts:
            cosines.append(self.compare(text, t))

        max_cosine = max(cosines)
        max_index = [ i for i, j in enumerate(cosines) if j == max_cosine ]
        return (max_index, max_cosine)

    def get_cosines(self, text, texts):
        """Compare a text with a list of texts and return the list a cosineSimilarity
                """
        cosines = []
        for t in texts:
            cosines.append(self.compare(text, t))

        return cosines