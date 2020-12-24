# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/purewords/filters/pattern_replace_filter.py
# Compiled at: 2018-08-07 00:28:08
# Size of source mod 2**32: 480 bytes
"""Pattern replace base filter"""
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