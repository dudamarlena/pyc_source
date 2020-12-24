# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/test_functionality/test_irv.py
# Compiled at: 2012-04-23 20:44:31
from pyvotecore.irv import IRV
import unittest

class TestInstantRunoff(unittest.TestCase):

    def test_irv_no_ties(self):
        input = [{'count': 26, 'ballot': ['c1', 'c2', 'c3']}, {'count': 20, 'ballot': ['c2', 'c3', 'c1']}, {'count': 23, 'ballot': ['c3', 'c1', 'c2']}]
        output = IRV(input).as_dict()
        self.assertEqual(output, {'candidates': set(['c1', 'c2', 'c3']), 
           'quota': 35, 
           'winner': 'c3', 
           'rounds': [{'tallies': {'c3': 23.0, 'c2': 20.0, 'c1': 26.0}, 'loser': 'c2'}, {'tallies': {'c3': 43.0, 'c1': 26.0}, 'winner': 'c3'}]})

    def test_irv_ties(self):
        input = [{'count': 26, 'ballot': ['c1', 'c2', 'c3']}, {'count': 20, 'ballot': ['c2', 'c3', 'c1']}, {'count': 20, 'ballot': ['c3', 'c1', 'c2']}]
        output = IRV(input).as_dict()
        self.assertEqual(output['quota'], 34)
        self.assertEqual(len(output['rounds']), 2)
        self.assertEqual(len(output['rounds'][0]), 3)
        self.assertEqual(output['rounds'][0]['tallies'], {'c1': 26, 'c2': 20, 'c3': 20})
        self.assertEqual(output['rounds'][0]['tied_losers'], set(['c2', 'c3']))
        self.assert_(output['rounds'][0]['loser'] in output['rounds'][0]['tied_losers'])
        self.assertEqual(len(output['rounds'][1]['tallies']), 2)
        self.assert_('winner' in output['rounds'][1])
        self.assertEqual(len(output['tie_breaker']), 3)

    def test_irv_landslide(self):
        input = [{'count': 56, 'ballot': ['c1', 'c2', 'c3']}, {'count': 20, 'ballot': ['c2', 'c3', 'c1']}, {'count': 20, 'ballot': ['c3', 'c1', 'c2']}]
        output = IRV(input).as_dict()
        self.assertEqual(output, {'candidates': set(['c1', 'c2', 'c3']), 
           'quota': 49, 
           'winner': 'c1', 
           'rounds': [{'tallies': {'c3': 20.0, 'c2': 20.0, 'c1': 56.0}, 'winner': 'c1'}]})


if __name__ == '__main__':
    unittest.main()