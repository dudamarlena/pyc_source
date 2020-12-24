# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/purewords/filters/word_replace_filter.py
# Compiled at: 2018-08-07 00:28:00
# Size of source mod 2**32: 576 bytes
"""Word replace base filter"""
import re
from .base_filter import BaseFilter

class WordReplaceFilter(BaseFilter):

    def __init__(self, replace_dictionary={}):
        self.replace_dictionary = replace_dictionary

    def add_replacement(self, word, replacement=''):
        self.replace_dictionary[word] = replacement

    def __call__(self, sentence):
        for pattern, replacement in self.replace_dictionary.items():
            sentence = re.sub(pattern, replacement, sentence)

        return sentence