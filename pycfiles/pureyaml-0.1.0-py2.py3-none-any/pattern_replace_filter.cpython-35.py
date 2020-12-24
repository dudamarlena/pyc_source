# uncompyle6 version 3.6.7
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/purewords/filters/pattern_replace_filter.py
# Compiled at: 2018-08-07 00:28:08
# Size of source mod 2**32: 480 bytes
__doc__ = 'Pattern replace base filter'
import re
from .base_filter import BaseFilter

class PatternReplaceFilter(BaseFilter):

    def __init__(self, patterns=[], replacement=''):
        self.patterns = patterns
        self.replacement = replacement

    def add_pattern(self, pattern):
        self.patterns.append(pattern)

    def __call__(self, sentence):
        return re.sub('|'.join(self.patterns), self.replacement, sentence)