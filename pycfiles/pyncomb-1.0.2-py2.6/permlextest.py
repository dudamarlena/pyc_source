# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.5-i386/egg/pyncomb/permlextest.py
# Compiled at: 2010-10-16 14:06:11
"""Unit testing for the permlex module.

By Sebastian Raaphorst, 2009."""
import unittest
from . import permlex
from . import combfuncs

class Tester(unittest.TestCase):
    """Unit testing class for this module.
    We perform all operations and check their interactions for correctness."""

    def setUp(self):
        self.n = 5

    def testall(self):
        """Test the interactions between all functions."""
        rk = 0
        for P in permlex.all(self.n):
            self.assertEqual(permlex.rank(self.n, P), rk)
            self.assertEqual(permlex.unrank(self.n, rk), P)
            rk += 1

        self.assertEqual(rk, reduce(lambda x, y: x * y, range(1, self.n + 1), 1))


if __name__ == '__main__':
    unittest.main()