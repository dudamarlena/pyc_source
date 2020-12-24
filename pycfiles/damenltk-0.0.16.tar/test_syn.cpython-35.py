# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/davidam/git/damenltk/source/test/test_syn.py
# Compiled at: 2019-10-30 01:06:48
# Size of source mod 2**32: 1942 bytes
import unittest, nltk
from nltk.corpus import wordnet

class TddInPythonExample(unittest.TestCase):

    def test_syn_returns_correct_result(self):
        syns = wordnet.synsets('program')
        self.assertEqual(syns[0].name(), 'plan.n.01')
        self.assertEqual(syns[0].lemmas()[0].name(), 'plan')
        self.assertEqual(syns[0].definition(), 'a series of steps to be carried out or goals to be accomplished')
        self.assertEqual(syns[0].examples(), ['they drew up a six-step plan', 'they discussed plans for a new bond issue'])

    def test_antonym_returns_correct_result(self):
        antonyms = []
        for syn in wordnet.synsets('good'):
            for l in syn.lemmas():
                if l.antonyms():
                    antonyms.append(l.antonyms()[0].name())

        self.assertEqual(['evil', 'evilness', 'bad', 'badness', 'bad', 'evil', 'ill'], antonyms)