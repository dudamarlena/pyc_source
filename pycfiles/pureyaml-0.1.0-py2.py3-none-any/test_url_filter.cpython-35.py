# uncompyle6 version 3.6.7
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/test/filters/test_url_filter.py
# Compiled at: 2018-08-07 00:31:31
# Size of source mod 2**32: 598 bytes
__doc__ = 'Url filter testcases'
from unittest import TestCase
from purewords.filters import url_filter

class TestUrlFilterClass(TestCase):

    def setUp(self):
        self.filter = url_filter

    def test_url_filter(self):
        sentence = '我們的官網是http://www.yoctol.com.tw' + '，有問題可以寄信至service@yoctol.com' + '或寄信到email@yoctol.edu.tw'
        answer = '我們的官網是_url_，有問題可以寄信至_url_或寄信到_url_'
        self.assertEqual(answer, self.filter(sentence))