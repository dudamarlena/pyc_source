# uncompyle6 version 3.6.7
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.5-i386/egg/pyncomb/tuplelextest.py
# Compiled at: 2010-10-16 14:07:15
__doc__ = 'Unit testing for the tuplelex module.\n\nBy Sebastian Raaphorst, 2009.'
import unittest
from . import tuplelex
from . import combfuncs

class Tester(unittest.TestCase):
    """Unit testing class for this module.
    We perform all operations over a given base set and check their
    interactions for correctness."""

    def setUp(self):
        self.base = [
         'a', 'b', 'c']
        self.k = 3
        self.B = combfuncs.createLookup(self.base)

    def testall(self):
        """Test the interactions between all functions."""
        count = len(self.base) ** self.k
        rk = 0
        for T in tuplelex.all(self.B, self.k):
            self.assertEqual(tuplelex.rank(self.B, T), rk)
            self.assertEqual(tuplelex.unrank(self.B, self.k, rk), T)
            rk += 1

        self.assertEqual(rk, count)


if __name__ == '__main__':
    unittest.main()