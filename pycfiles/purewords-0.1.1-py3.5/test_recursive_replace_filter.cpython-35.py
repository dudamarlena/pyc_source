# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/test/filters/test_recursive_replace_filter.py
# Compiled at: 2018-08-07 00:31:21
# Size of source mod 2**32: 530 bytes
"""recursive replace filter testcase"""
from unittest import TestCase
from purewords.filters import RecursiveReplaceFilter

class TestRecursiveReplaceFilterClass(TestCase):

    def setUp(self):
        self.pattern = 'AA'
        self.replacement = 'A'
        self.filter = RecursiveReplaceFilter(self.pattern, self.replacement)

    def test_call(self):
        sentence = 'AAAA'
        result = self.filter(sentence)
        self.assertEqual(result, 'A')