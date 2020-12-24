# uncompyle6 version 3.6.7
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/test/filters/test_blank_filter.py
# Compiled at: 2018-08-07 00:31:11
# Size of source mod 2**32: 410 bytes
__doc__ = 'Blank filter testcase'
from unittest import TestCase
from purewords.filters import blank_filter

class TestBlankFilterClass(TestCase):

    def setUp(self):
        self.filter = blank_filter

    def test_blank_filter(self):
        sentence = 'Hello I am ______ blank!!'
        answer = 'Hello I am _ blank!!'
        self.assertEqual(answer, self.filter(sentence))