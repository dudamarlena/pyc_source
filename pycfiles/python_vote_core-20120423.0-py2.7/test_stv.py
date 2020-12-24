# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/test_functionality/test_stv.py
# Compiled at: 2012-04-23 20:44:39
from pyvotecore.stv import STV
import unittest

class TestSTV(unittest.TestCase):

    def test_stv_landslide(self):
        input = [{'count': 56, 'ballot': ['c1', 'c2', 'c3']}, {'count': 40, 'ballot': ['c2', 'c3', 'c1']}, {'count': 20, 'ballot': ['c3', 'c1', 'c2']}]
        output = STV(input, required_winners=2).as_dict()
        self.assertEqual(output, {'candidates': set(['c1', 'c2', 'c3']), 
           'quota': 39, 
           'rounds': [
                    {'tallies': {'c3': 20.0, 'c2': 40.0, 'c1': 56.0}, 'winners': set(['c2', 'c1'])}], 
           'winners': set(['c2', 'c1'])})

    def test_stv_everyone_wins(self):
        input = [{'count': 56, 'ballot': ['c1', 'c2', 'c3']}, {'count': 40, 'ballot': ['c2', 'c3', 'c1']}, {'count': 20, 'ballot': ['c3', 'c1', 'c2']}]
        output = STV(input, required_winners=3).as_dict()
        self.assertEqual(output, {'candidates': set(['c1', 'c2', 'c3']), 
           'quota': 30, 
           'rounds': [], 'remaining_candidates': set(['c1', 'c2', 'c3']), 
           'winners': set(['c1', 'c2', 'c3'])})

    def test_stv_wiki_example(self):
        input = [{'count': 4, 'ballot': ['orange']}, {'count': 2, 'ballot': ['pear', 'orange']}, {'count': 8, 'ballot': ['chocolate', 'strawberry']}, {'count': 4, 'ballot': ['chocolate', 'sweets']}, {'count': 1, 'ballot': ['strawberry']}, {'count': 1, 'ballot': ['sweets']}]
        output = STV(input, required_winners=3).as_dict()
        self.assertEqual(output, {'candidates': set(['orange', 'pear', 'chocolate', 'strawberry', 'sweets']), 
           'quota': 6, 
           'rounds': [{'tallies': {'orange': 4.0, 'strawberry': 1.0, 'pear': 2.0, 'sweets': 1.0, 'chocolate': 12.0}, 'winners': set(['chocolate'])}, {'tallies': {'orange': 4.0, 'strawberry': 5.0, 'pear': 2.0, 'sweets': 3.0}, 'loser': 'pear'}, {'tallies': {'orange': 6.0, 'strawberry': 5.0, 'sweets': 3.0}, 'winners': set(['orange'])}, {'tallies': {'strawberry': 5.0, 'sweets': 3.0}, 'loser': 'sweets'}], 'remaining_candidates': set(['strawberry']), 
           'winners': set(['orange', 'strawberry', 'chocolate'])})

    def test_stv_single_ballot(self):
        input = [{'count': 1, 'ballot': ['c1', 'c2', 'c3', 'c4']}]
        output = STV(input, required_winners=3).as_dict()
        self.assertEqual(output, {'candidates': set(['c1', 'c2', 'c3', 'c4']), 
           'quota': 1, 
           'rounds': [{'tallies': {'c1': 1.0}, 'winners': set(['c1'])}, {'note': 'reset', 'tallies': {'c2': 1.0}, 'winners': set(['c2'])}, {'note': 'reset', 'tallies': {'c3': 1.0}, 'winners': set(['c3'])}], 'winners': set(['c1', 'c2', 'c3'])})

    def test_stv_fewer_voters_than_winners(self):
        input = [{'count': 1, 'ballot': ['c1', 'c3', 'c4']}, {'count': 1, 'ballot': ['c2', 'c3', 'c4']}]
        output = STV(input, required_winners=3).as_dict()
        self.assertEqual(output, {'candidates': set(['c1', 'c2', 'c3', 'c4']), 
           'quota': 1, 
           'rounds': [{'tallies': {'c2': 1.0, 'c1': 1.0}, 'winners': set(['c2', 'c1'])}, {'note': 'reset', 'tallies': {'c3': 2.0}, 'winners': set(['c3'])}], 'winners': set(['c1', 'c2', 'c3'])})


if __name__ == '__main__':
    unittest.main()