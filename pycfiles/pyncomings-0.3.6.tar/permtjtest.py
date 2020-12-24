# uncompyle6 version 3.6.7
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.5-i386/egg/pyncomb/permtjtest.py
# Compiled at: 2010-10-16 14:06:27
__doc__ = 'Unit testing for the permtj module.\n\nBy Sebastian Raaphorst, 2009.'
import unittest
from . import permtj
from . import combfuncs

class Tester(unittest.TestCase):
    """Unit testing class for this module.
    We perform all operations and check their interactions for correctness."""

    def setUp(self):
        self.n = 5

    def testall(self):
        """Test the interactions between all functions."""
        rk = 0
        for P in permtj.all(self.n):
            self.assertEqual(permtj.rank(self.n, P), rk)
            self.assertEqual(permtj.unrank(self.n, rk), P)
            rk += 1

        self.assertEqual(rk, reduce(lambda x, y: x * y, range(1, self.n + 1), 1))


if __name__ == '__main__':
    unittest.main()