# uncompyle6 version 3.6.7
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.5-i386/egg/pyncomb/ksubsetlextest.py
# Compiled at: 2010-10-16 14:05:20
__doc__ = 'Unit testing for the ksubsetlex module.\n\nBy Sebastian Raaphorst, 2009.'
import unittest
from . import combfuncs
from . import ksubsetlex

class Tester(unittest.TestCase):
    """Unit testing class for this module.
    We perform all operations over a given base set and check their
    interactions for correctness."""

    def setUp(self):
        self.B = combfuncs.createLookup(['a', 'b', 'c', 'd', 'e'])
        self.k = 3

    def testall(self):
        """Test the interactions between all functions."""
        v = self.B if type(self.B) == int else len(self.B[1])
        rk = 0
        for K in ksubsetlex.all(self.B, self.k):
            self.assertEqual(ksubsetlex.rank(self.B, K), rk)
            self.assertEqual(ksubsetlex.unrank(self.B, self.k, rk), K)
            rk += 1

        self.assertEqual(rk, combfuncs.binom(v, self.k))


if __name__ == '__main__':
    unittest.main()