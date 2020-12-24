# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/test_functionality/test_plurality.py
# Compiled at: 2012-04-23 20:44:30
from pyvotecore.plurality import Plurality
import unittest

class TestPlurality(unittest.TestCase):

    def test_no_ties(self):
        input = [{'count': 26, 'ballot': 'c1'}, {'count': 22, 'ballot': 'c2'}, {'count': 23, 'ballot': 'c3'}]
        output = Plurality(input).as_dict()
        self.assertEqual(output, {'candidates': set(['c1', 'c2', 'c3']), 
           'tallies': {'c3': 23, 'c2': 22, 'c1': 26}, 'winner': 'c1'})

    def test_plurality_alternate_ballot_format(self):
        input = [{'count': 26, 'ballot': ['c1']}, {'count': 22, 'ballot': ['c2']}, {'count': 23, 'ballot': ['c3']}]
        output = Plurality(input).as_dict()
        self.assertEqual(output, {'candidates': set(['c1', 'c2', 'c3']), 
           'tallies': {'c3': 23, 'c2': 22, 'c1': 26}, 'winner': 'c1'})

    def test_irrelevant_ties(self):
        input = [{'count': 26, 'ballot': 'c1'}, {'count': 23, 'ballot': 'c2'}, {'count': 23, 'ballot': 'c3'}]
        output = Plurality(input).as_dict()
        self.assertEqual(output, {'candidates': set(['c1', 'c2', 'c3']), 
           'tallies': {'c3': 23, 'c2': 23, 'c1': 26}, 'winner': 'c1'})

    def test_relevant_ties(self):
        input = [{'count': 26, 'ballot': 'c1'}, {'count': 26, 'ballot': 'c2'}, {'count': 23, 'ballot': 'c3'}]
        output = Plurality(input).as_dict()
        self.assertEqual(output['tallies'], {'c1': 26, 'c2': 26, 'c3': 23})
        self.assertEqual(output['tied_winners'], set(['c1', 'c2']))
        self.assert_(output['winner'] in output['tied_winners'])
        self.assertEqual(len(output['tie_breaker']), 3)


if __name__ == '__main__':
    unittest.main()