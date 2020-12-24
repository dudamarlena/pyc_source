# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/test_performance/test_schulze_stv.py
# Compiled at: 2012-04-23 22:56:43
from pyvotecore.schulze_stv import SchulzeSTV
import unittest, time

class TestSchulzeSTV(unittest.TestCase):

    def test_10_candidates_5_winners(self):
        startTime = time.time()
        input = [{'count': 1, 'ballot': {'A': 9, 'B': 1, 'C': 1, 'D': 9, 'E': 9, 'F': 2, 'G': 9, 'H': 9, 'I': 9, 'J': 9}}, {'count': 1, 'ballot': {'A': 3, 'B': 2, 'C': 3, 'D': 1, 'E': 9, 'F': 9, 'G': 9, 'H': 9, 'I': 9, 'J': 9}}, {'count': 1, 'ballot': {'A': 9, 'B': 9, 'C': 9, 'D': 9, 'E': 1, 'F': 9, 'G': 9, 'H': 9, 'I': 9, 'J': 9}}]
        SchulzeSTV(input, required_winners=5, ballot_notation='ranking').as_dict()
        self.assert_(time.time() - startTime < 8)

    def test_10_candidates_9_winners(self):
        startTime = time.time()
        input = [{'count': 1, 'ballot': {'A': 9, 'B': 1, 'C': 1, 'D': 9, 'E': 9, 'F': 2, 'G': 9, 'H': 9, 'I': 9, 'J': 9}}, {'count': 1, 'ballot': {'A': 3, 'B': 2, 'C': 3, 'D': 1, 'E': 9, 'F': 9, 'G': 9, 'H': 9, 'I': 9, 'J': 9}}, {'count': 1, 'ballot': {'A': 9, 'B': 9, 'C': 9, 'D': 9, 'E': 1, 'F': 9, 'G': 9, 'H': 9, 'I': 9, 'J': 9}}]
        SchulzeSTV(input, required_winners=9, ballot_notation='ranking').as_dict()
        self.assert_(time.time() - startTime < 2)

    def test_10_candidates_10_winners(self):
        startTime = time.time()
        input = [{'count': 1, 'ballot': {'A': 9, 'B': 1, 'C': 1, 'D': 9, 'E': 9, 'F': 2, 'G': 9, 'H': 9, 'I': 9, 'J': 9}}, {'count': 1, 'ballot': {'A': 3, 'B': 2, 'C': 3, 'D': 1, 'E': 9, 'F': 9, 'G': 9, 'H': 9, 'I': 9, 'J': 9}}, {'count': 1, 'ballot': {'A': 9, 'B': 9, 'C': 9, 'D': 9, 'E': 1, 'F': 9, 'G': 9, 'H': 9, 'I': 9, 'J': 9}}]
        output = SchulzeSTV(input, required_winners=10, ballot_notation='ranking').as_dict()
        self.assertAlmostEqual(startTime, time.time(), 1)
        self.assertEqual(output, {'winners': set(['A', 'C', 'B', 'E', 'D', 'G', 'F', 'I', 'H', 'J']), 
           'candidates': set(['A', 'C', 'B', 'E', 'D', 'G', 'F', 'I', 'H', 'J'])})


if __name__ == '__main__':
    unittest.main()