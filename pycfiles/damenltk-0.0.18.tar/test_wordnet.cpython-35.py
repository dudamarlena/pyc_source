# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/davidam/git/damenltk/source/test/test_wordnet.py
# Compiled at: 2019-10-30 01:06:48
# Size of source mod 2**32: 1660 bytes
import unittest
from nltk.corpus import wordnet

class TddInPythonExample(unittest.TestCase):

    def test_synonims_definition_method_returns_correct_result(self):
        syns = wordnet.synsets('program')
        s = syns[0].definition()
        self.assertEqual('a series of steps to be carried out or goals to be accomplished', s)

    def test_synonims_lemmas_method_returns_correct_result(self):
        syns = wordnet.synsets('program')
        s = syns[0].lemmas()[0].name()
        self.assertEqual('plan', s)

    def test_similarity_method_returns_correct_result(self):
        w1 = wordnet.synset('ship.n.01')
        w2 = wordnet.synset('boat.n.01')
        self.assertTrue(w1.wup_similarity(w2) > 0.5)


if __name__ == '__main__':
    unittest.main()