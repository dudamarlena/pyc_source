# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/test_functionality/test_schulze_npr.py
# Compiled at: 2012-04-23 20:44:37
from pyvotecore.schulze_npr import SchulzeNPR
import unittest

class TestSchulzeNPR(unittest.TestCase):

    def test_single_voter(self):
        input = [{'count': 1, 'ballot': {'A': 1, 'B': 2, 'C': 3, 'D': 4, 'E': 5}}]
        output = SchulzeNPR(input, winner_threshold=5, ballot_notation='ranking').as_dict()
        self.assertEqual(output, {'order': [
                   'A', 'B', 'C', 'D', 'E'], 
           'candidates': set(['A', 'B', 'C', 'D', 'E']), 
           'rounds': [{'winner': 'A'}, {'winner': 'B'}, {'winner': 'C'}, {'winner': 'D'}, {'winner': 'E'}]})

    def test_nonproportionality(self):
        input = [{'count': 2, 'ballot': {'A': 1, 'B': 2, 'C': 3, 'D': 4, 'E': 5}}, {'count': 1, 'ballot': {'A': 5, 'B': 4, 'C': 3, 'D': 2, 'E': 1}}]
        output = SchulzeNPR(input, winner_threshold=5, ballot_notation='ranking').as_dict()
        self.assertEqual(output, {'order': [
                   'A', 'B', 'C', 'D', 'E'], 
           'candidates': set(['A', 'B', 'C', 'D', 'E']), 
           'rounds': [{'winner': 'A'}, {'winner': 'B'}, {'winner': 'C'}, {'winner': 'D'}, {'winner': 'E'}]})


if __name__ == '__main__':
    unittest.main()