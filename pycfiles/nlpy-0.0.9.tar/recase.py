# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/hadoop/nlpy/nlpy/basic/recase.py
# Compiled at: 2014-11-12 02:23:17
from nlpy.util import internal_resource, LineIterator
_FREQ_DATA_PATH = internal_resource('general/en_us_with_coca_1m_bigram_words.txt')

class FreqRecaser(object):

    def __init__(self):
        """
        Initialize recase map.
        """
        self._recase_map = {}
        for line in LineIterator(_FREQ_DATA_PATH):
            _, word = line.split('\t')
            low_word = word.lower()
            if low_word not in self._recase_map:
                self._recase_map[low_word] = word

    def recase(self, word):
        """
        :param word: word
        :return: recased word
        """
        low_word = word.lower()
        if low_word not in self._recase_map:
            return word
        else:
            return self._recase_map[low_word]