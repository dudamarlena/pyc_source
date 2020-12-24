# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/davidam/git/damenltk/source/app/detectlanguage.py
# Compiled at: 2019-10-30 01:06:48
# Size of source mod 2**32: 2881 bytes
import sys
from nltk import wordpunct_tokenize
from nltk.corpus import stopwords

class DetectLanguage(object):

    def calculate_languages_ratios(self, text):
        """
        Calculate probability of given text to be written in several languages and
        return a dictionary that looks like {'french': 2, 'spanish': 4, 'english': 0}

        @param text: Text whose language want to be detected
        @type text: str

        @return: Dictionary with languages and unique stopwords seen in analyzed text
        @rtype: dict
        """
        languages_ratios = {}
        tokens = wordpunct_tokenize(text)
        words = [word.lower() for word in tokens]
        for language in stopwords.fileids():
            stopwords_set = set(stopwords.words(language))
            words_set = set(words)
            common_elements = words_set.intersection(stopwords_set)
            languages_ratios[language] = len(common_elements)

        return languages_ratios

    def detect_language(self, text):
        """
        Calculate probability of given text to be written in several languages and return the highest scored.

        It uses a stopwords based approach, counting how many unique stopwords
        are seen in analyzed text.

        @param text: Text whose language want to be detected
        @type text: str
        @return: Most scored language guessed
        @rtype: str
        """
        ratios = self.calculate_languages_ratios(text)
        most_rated_language = max(ratios, key=ratios.get)
        return most_rated_language