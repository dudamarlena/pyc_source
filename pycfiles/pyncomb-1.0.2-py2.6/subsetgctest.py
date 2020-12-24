# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.5-i386/egg/pyncomb/subsetgctest.py
# Compiled at: 2010-10-16 14:06:43
"""Unit testing for the subsetgc module.

By Sebastian Raaphorst, 2009."""
import unittest
from . import subsetgc
from . import combfuncs

class Tester(unittest.TestCase):
    """Unit testing class for this module.
    We perform all operations over a given base set and check their
    interactions for correctness."""

    def setUp(self):
        self.B = combfuncs.createLookup(['a', 'b', 'c', 'd', 'e'])

    def testall(self):
        """Test the interactions between all functions."""
        v = self.B if type(self.B) == int else len(self.B[1])
        rk = 0
        for S in subsetgc.all(self.B):
            self.assertEqual(subsetgc.rank(self.B, S), rk)
            self.assertEqual(subsetgc.unrank(self.B, rk), S)
            rk += 1

        self.assertEqual(rk, 1 << v)


if __name__ == '__main__':
    unittest.main()