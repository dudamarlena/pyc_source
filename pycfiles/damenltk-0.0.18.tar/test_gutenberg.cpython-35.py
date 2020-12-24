# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/davidam/git/damenltk/source/test/test_gutenberg.py
# Compiled at: 2019-10-30 01:06:48
# Size of source mod 2**32: 1204 bytes
import unittest
from nltk.book import *

class TddInPythonExample(unittest.TestCase):

    def test_length_text3_returns_correct_result(self):
        length = len(text3)
        self.assertTrue(length > 4000)

    def test_count_in_returns_correct_result(self):
        self.assertTrue(text5.count('in') > 0)