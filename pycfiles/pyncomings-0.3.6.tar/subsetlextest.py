# uncompyle6 version 3.6.7
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.5-i386/egg/pyncomb/subsetlextest.py
# Compiled at: 2010-10-16 14:06:58
__doc__ = 'Unit testing for the subsetlex module.\n\nBy Sebastian Raaphorst, 2009.'
import unittest
from . import subsetlex
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
        for S in subsetlex.all(self.B):
            self.assertEqual(subsetlex.rank(self.B, S), rk)
            self.assertEqual(subsetlex.unrank(self.B, rk), S)
            rk += 1

        self.assertEqual(rk, 1 << v)


if __name__ == '__main__':
    unittest.main()