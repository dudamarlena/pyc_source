# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/test_functionality/test_tie_breaker.py
# Compiled at: 2012-04-23 20:44:22
from pyvotecore.tie_breaker import TieBreaker
import unittest

class TestTieBreaker(unittest.TestCase):

    def setUp(self):
        self.tieBreaker = TieBreaker(['a', 'b', 'c', 'd'])
        self.tieBreaker.random_ordering = ['a', 'b', 'c', 'd']

    def test_simple_tie(self):
        self.assertEqual(self.tieBreaker.break_ties(set(['b', 'c'])), 'b')

    def test_simple_tie_reverse(self):
        self.assertEqual(self.tieBreaker.break_ties(set(['b', 'c']), reverse=True), 'c')

    def test_tuple_tie(self):
        self.assertEqual(self.tieBreaker.break_ties(set([('c', 'a'), ('b', 'd'), ('c', 'b')])), ('b',
                                                                                                 'd'))

    def test_tuple_tie_reverse(self):
        self.assertEqual(self.tieBreaker.break_ties(set([('c', 'a'), ('b', 'd'), ('c', 'b')]), reverse=True), ('c',
                                                                                                               'b'))


if __name__ == '__main__':
    unittest.main()