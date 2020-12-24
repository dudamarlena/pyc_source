# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/test_functionality/test_ranked_pairs.py
# Compiled at: 2012-04-23 20:44:25
from pyvotecore.ranked_pairs import RankedPairs
import unittest

class TestRankedPairs(unittest.TestCase):

    def test_no_cycle(self):
        input = [{'count': 80, 'ballot': [['c1', 'c2'], ['c3']]}, {'count': 50, 'ballot': [['c2'], ['c3', 'c1']]}, {'count': 40, 'ballot': [['c3'], ['c1'], ['c2']]}]
        output = RankedPairs(input, ballot_notation='grouping').as_dict()
        self.assertEqual(output, {'candidates': set(['c3', 'c2', 'c1']), 
           'pairs': {('c1', 'c2'): 40, 
                     ('c1', 'c3'): 80, 
                     ('c2', 'c1'): 50, 
                     ('c2', 'c3'): 130, 
                     ('c3', 'c1'): 40, 
                     ('c3', 'c2'): 40}, 
           'strong_pairs': {('c2', 'c3'): 130, 
                            ('c1', 'c3'): 80, 
                            ('c2', 'c1'): 50}, 
           'winner': 'c2'})

    def test_cycle(self):
        input = [{'count': 80, 'ballot': [['c1'], ['c2'], ['c3']]}, {'count': 50, 'ballot': [['c2'], ['c3'], ['c1']]}, {'count': 40, 'ballot': [['c3'], ['c1'], ['c2']]}]
        output = RankedPairs(input, ballot_notation='grouping').as_dict()
        self.assertEqual(output, {'candidates': set(['c3', 'c2', 'c1']), 
           'pairs': {('c1', 'c3'): 80, 
                     ('c1', 'c2'): 120, 
                     ('c2', 'c1'): 50, 
                     ('c2', 'c3'): 130, 
                     ('c3', 'c1'): 90, 
                     ('c3', 'c2'): 40}, 
           'strong_pairs': {('c2', 'c3'): 130, 
                            ('c1', 'c2'): 120, 
                            ('c3', 'c1'): 90}, 
           'rounds': [{'pair': ('c2', 'c3'), 'action': 'added'}, {'pair': ('c1', 'c2'), 'action': 'added'}, {'pair': ('c3', 'c1'), 'action': 'skipped'}], 'winner': 'c1'})

    def test_tied_pairs(self):
        input = [{'count': 100, 'ballot': [['chocolate'], ['vanilla']]}, {'count': 100, 'ballot': [['vanilla'], ['strawberry']]}, {'count': 1, 'ballot': [['strawberry'], ['chocolate']]}]
        output = RankedPairs(input, ballot_notation='grouping').as_dict()
        self.assertEqual(output['pairs'], {('vanilla', 'strawberry'): 200, 
           ('strawberry', 'vanilla'): 1, 
           ('chocolate', 'vanilla'): 101, 
           ('vanilla', 'chocolate'): 100, 
           ('strawberry', 'chocolate'): 101, 
           ('chocolate', 'strawberry'): 100})
        self.assertEqual(output['strong_pairs'], {('chocolate', 'vanilla'): 101, 
           ('vanilla', 'strawberry'): 200, 
           ('strawberry', 'chocolate'): 101})
        self.assertEqual(output['rounds'][1]['tied_pairs'], set([('chocolate', 'vanilla'), ('strawberry', 'chocolate')]))


if __name__ == '__main__':
    unittest.main()