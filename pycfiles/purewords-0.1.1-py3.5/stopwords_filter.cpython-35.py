# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/purewords/filters/stopwords_filter.py
# Compiled at: 2018-08-07 00:28:04
# Size of source mod 2**32: 257 bytes
"""Stopwords filter"""
from .pattern_replace_filter import PatternReplaceFilter

class StopwordsFilter(PatternReplaceFilter):

    def __init__(self, stopwords_set):
        super(StopwordsFilter, self).__init__(list(stopwords_set))