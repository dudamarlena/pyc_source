# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/davidam/git/damenltk/source/test/test_bigrams_trigrams.py
# Compiled at: 2019-10-30 01:06:48
# Size of source mod 2**32: 2155 bytes
import unittest
from nltk.corpus import reuters
from nltk import bigrams, trigrams
from collections import Counter, defaultdict

class TddInPythonExample(unittest.TestCase):

    def test_first_sentence_method_returns_correct_result(self):
        first_sentence = reuters.sents()[0]
        self.assertEqual(first_sentence[0:3], ['ASIAN', 'EXPORTERS', 'FEAR'])

    def test_bigrams_method_returns_correct_result(self):
        first_sentence = reuters.sents()[0]
        b = list(bigrams(first_sentence))
        self.assertEqual(b[0:3], [('ASIAN', 'EXPORTERS'), ('EXPORTERS', 'FEAR'), ('FEAR', 'DAMAGE')])

    def test_trigrams_method_returns_correct_result(self):
        first_sentence = reuters.sents()[0]
        t = list(trigrams(first_sentence))
        self.assertEqual(t[0:3], [('ASIAN', 'EXPORTERS', 'FEAR'), ('EXPORTERS', 'FEAR', 'DAMAGE'), ('FEAR', 'DAMAGE', 'FROM')])

    def test_trigrams_pad_method_returns_correct_result(self):
        first_sentence = reuters.sents()[0]
        t = list(trigrams(first_sentence, pad_left=True, pad_right=True))
        self.assertEqual(t[0:3], [(None, None, 'ASIAN'), (None, 'ASIAN', 'EXPORTERS'), ('ASIAN', 'EXPORTERS', 'FEAR')])


if __name__ == '__main__':
    unittest.main()