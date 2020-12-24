# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/davidam/git/damenltk/source/test/test_tokenize.py
# Compiled at: 2019-10-30 01:06:48
# Size of source mod 2**32: 1616 bytes
import unittest, nltk

class TddInPythonExample(unittest.TestCase):

    def test_tokenize_method_returns_correct_result(self):
        sentence = "At eight o'clock on Thursday morning Arthur didn't feel very good."
        tokens = nltk.word_tokenize(sentence)
        self.assertEqual(tokens, ['At', 'eight', "o'clock", 'on', 'Thursday', 'morning', 'Arthur', 'did', "n't", 'feel', 'very', 'good', '.'])

    def test_tagged_method_returns_correct_result(self):
        sentence = "At eight o'clock on Thursday morning Arthur didn't feel very good."
        tokens = nltk.word_tokenize(sentence)
        tagged = nltk.pos_tag(tokens)
        self.assertEqual(tagged[0:2], [('At', 'IN'), ('eight', 'CD')])