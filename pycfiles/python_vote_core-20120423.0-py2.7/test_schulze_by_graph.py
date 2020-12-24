# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/test_functionality/test_schulze_by_graph.py
# Compiled at: 2012-04-23 20:44:26
from pyvotecore.schulze_by_graph import SchulzeMethodByGraph, SchulzeNPRByGraph
import unittest

class TestSchulzeMethodByGraph(unittest.TestCase):

    def test_simple_example(self):
        input = {('a', 'b'): 4, 
           ('b', 'a'): 3, 
           ('a', 'c'): 4, 
           ('c', 'a'): 3, 
           ('b', 'c'): 4, 
           ('c', 'b'): 3}
        output = SchulzeMethodByGraph(input).as_dict()
        self.assertEqual(output, {'candidates': set(['a', 'b', 'c']), 
           'pairs': input, 
           'strong_pairs': {('a', 'b'): 4, 
                            ('a', 'c'): 4, 
                            ('b', 'c'): 4}, 
           'winner': 'a'})


class TestSchulzeNPRByGraph(unittest.TestCase):

    def test_simple_example(self):
        input = {('a', 'b'): 8, 
           ('b', 'a'): 3, 
           ('a', 'c'): 3, 
           ('c', 'a'): 4, 
           ('b', 'c'): 6, 
           ('c', 'b'): 3}
        output = SchulzeNPRByGraph(input, winner_threshold=3).as_dict()
        self.assertEqual(output, {'candidates': set(['a', 'b', 'c']), 
           'rounds': [{'winner': 'a'}, {'winner': 'b'}, {'winner': 'c'}], 'order': [
                   'a', 'b', 'c']})

    def test_complex_example(self):
        input = {('a', 'b'): 4, 
           ('b', 'a'): 3, 
           ('a', 'c'): 4, 
           ('c', 'a'): 3, 
           ('b', 'c'): 4, 
           ('c', 'b'): 3, 
           ('a', 'd'): 4, 
           ('d', 'a'): 4, 
           ('b', 'd'): 4, 
           ('d', 'b'): 4, 
           ('c', 'd'): 4, 
           ('d', 'c'): 4}
        output = SchulzeNPRByGraph(input, winner_threshold=3, tie_breaker=['a', 'd', 'c', 'b']).as_dict()
        self.assertEqual(output, {'candidates': set(['a', 'b', 'c', 'd']), 
           'tie_breaker': [
                         'a', 'd', 'c', 'b'], 
           'rounds': [{'winner': 'a', 'tied_winners': set(['a', 'd'])}, {'winner': 'd', 'tied_winners': set(['b', 'd'])}, {'winner': 'b'}], 'order': [
                   'a', 'd', 'b']})


if __name__ == '__main__':
    unittest.main()