# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/test_functionality/test_plurality_at_large.py
# Compiled at: 2012-04-23 20:44:27
from pyvotecore.plurality_at_large import PluralityAtLarge
import unittest

class TestPluralityAtLarge(unittest.TestCase):

    def test_plurality_at_large_no_ties(self):
        output = PluralityAtLarge([{'count': 26, 'ballot': ['c1', 'c2']}, {'count': 22, 'ballot': ['c1', 'c3']}, {'count': 23, 'ballot': ['c2', 'c3']}], required_winners=2).as_dict()
        self.assertEqual(output, {'candidates': set(['c1', 'c2', 'c3']), 
           'tallies': {'c3': 45, 'c2': 49, 'c1': 48}, 'winners': set(['c2', 'c1'])})

    def test_plurality_at_large_irrelevant_ties(self):
        output = PluralityAtLarge([{'count': 26, 'ballot': ['c1', 'c2']}, {'count': 22, 'ballot': ['c1', 'c3']}, {'count': 22, 'ballot': ['c2', 'c3']}, {'count': 11, 'ballot': ['c4', 'c5']}], required_winners=2).as_dict()
        self.assertEqual(output, {'candidates': set(['c1', 'c2', 'c3', 'c4', 'c5']), 
           'tallies': {'c3': 44, 'c2': 48, 'c1': 48, 'c5': 11, 'c4': 11}, 'winners': set(['c2', 'c1'])})

    def test_plurality_at_large_relevant_ties(self):
        output = PluralityAtLarge([{'count': 30, 'ballot': ['c1', 'c2']}, {'count': 22, 'ballot': ['c3', 'c1']}, {'count': 22, 'ballot': ['c2', 'c3']}, {'count': 4, 'ballot': ['c4', 'c1']}, {'count': 8, 'ballot': ['c3', 'c4']}], required_winners=2).as_dict()
        self.assertEqual(output['tallies'], {'c3': 52, 'c2': 52, 'c1': 56, 'c4': 12})
        self.assertEqual(len(output['tie_breaker']), 4)
        self.assertEqual(output['tied_winners'], set(['c2', 'c3']))
        self.assert_('c1' in output['winners'] and ('c2' in output['winners'] or 'c3' in output['winners']))
        self.assertEqual(len(output), 5)


if __name__ == '__main__':
    unittest.main()