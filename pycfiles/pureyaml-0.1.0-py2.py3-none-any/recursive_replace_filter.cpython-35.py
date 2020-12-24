# uncompyle6 version 3.6.7
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/purewords/filters/recursive_replace_filter.py
# Compiled at: 2018-08-07 00:28:06
# Size of source mod 2**32: 505 bytes
__doc__ = 'recursive replace base filter '
import re
from .base_filter import BaseFilter

class RecursiveReplaceFilter(BaseFilter):

    def __init__(self, pattern='', replacement=''):
        self.pattern = pattern
        self.replacement = replacement

    def __call__(self, sentence):
        while re.search(self.pattern, sentence) is not None:
            sentence = re.sub(self.pattern, self.replacement, sentence)

        return sentence