# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/davidam/git/damenltk/source/test/test_sentencesimilarity.py
# Compiled at: 2019-10-30 01:06:48
# Size of source mod 2**32: 1249 bytes
import unittest, nltk
from app.sentencesimilarity import SentenceSimilarity

class TddInPythonExample(unittest.TestCase):

    def test_sentencesimilarity_method_returns_correct_result(self):
        s = SentenceSimilarity()
        self.assertTrue(s.sentence_similarity('This is a good sentence'.split(), 'This is a bad sentence'.split()) > 0.6)