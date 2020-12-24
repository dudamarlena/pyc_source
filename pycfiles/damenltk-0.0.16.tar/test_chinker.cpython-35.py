# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/davidam/git/damenltk/source/test/test_chinker.py
# Compiled at: 2019-10-30 07:33:46
# Size of source mod 2**32: 1549 bytes
import unittest, nltk

class TddInPythonExample(unittest.TestCase):

    def test_chinker_returns_correct_result(self):
        grammar = '\n        NP:\n        {<.*>+}          # Chunk everything\n        }<VBD|IN>+{      # Chink sequences of VBD and IN\n        '
        sentence = [('the', 'DT'), ('little', 'JJ'), ('yellow', 'JJ'),
         ('dog', 'NN'), ('barked', 'VBD'), ('at', 'IN'), ('the', 'DT'), ('cat', 'NN')]
        result = '\n(S\n   (NP the/DT little/JJ yellow/JJ dog/NN)\n   barked/VBD\n   at/IN\n   (NP the/DT cat/NN))\n'
        cp = nltk.RegexpParser(grammar)
        self.assertEqual(cp.parse(sentence), result)