# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/purewords/filters/recursive_replace_filter.py
# Compiled at: 2018-08-07 00:28:06
# Size of source mod 2**32: 505 bytes
"""recursive replace base filter """
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