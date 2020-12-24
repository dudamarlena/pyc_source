# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/test/filters/test_stopwords_filter.py
# Compiled at: 2018-08-07 00:31:23
# Size of source mod 2**32: 601 bytes
"""Stopwords filter testcase"""
from unittest import TestCase
from purewords.filters import StopwordsFilter

class TestStopwordsFilter(TestCase):

    def setUp(self):
        stopwords_set = set(['的', '啦'])
        self.filter = StopwordsFilter(stopwords_set)

    def test_stopwords_filter(self):
        sentence = '我講話很喜歡加的啦，' + '你知道的啦，我家有養一隻狗的啦。'
        answer = '我講話很喜歡加，你知道，我家有養一隻狗。'
        self.assertEqual(answer, self.filter(sentence))