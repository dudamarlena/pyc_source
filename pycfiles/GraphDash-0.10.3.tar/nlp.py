# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: graphdash/nlp.py
# Compiled at: 2019-04-25 09:26:58
import re, stop_words

class Cleaner(object):

    def __init__(self, removed_chars):
        self._regexp = re.compile(('[{0}]').format(removed_chars))

    def clean(self, word):
        """Removes any character from removed_chars in the string."""
        return self._regexp.sub('', word)


class StopWords(object):

    def __init__(self, language):
        self._stop_words = set(stop_words.get_stop_words(language))

    def __contains__(self, word):
        return word in self._stop_words

    def __iter__(self):
        return iter(self._stop_words)