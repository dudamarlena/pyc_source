# uncompyle6 version 3.6.7
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/purewords/filters/stopwords_filter.py
# Compiled at: 2018-08-07 00:28:04
# Size of source mod 2**32: 257 bytes
__doc__ = 'Stopwords filter'
from .pattern_replace_filter import PatternReplaceFilter

class StopwordsFilter(PatternReplaceFilter):

    def __init__(self, stopwords_set):
        super(StopwordsFilter, self).__init__(list(stopwords_set))