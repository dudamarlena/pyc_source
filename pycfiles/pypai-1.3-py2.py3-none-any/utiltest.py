# uncompyle6 version 3.6.7
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.6-universal/egg/pypagseguro/utiltest.py
# Compiled at: 2011-01-06 19:06:57
import unittest, doctest, util

class utilTest(unittest.TestCase):
    """Testes para util"""

    def testutil(self):
        """util"""
        pass


class DocTest(unittest.TestCase):
    """Roda o doctest de util"""

    def testdoc(self):
        """doctest de util"""
        t = doctest.testmod(util)
        self.assertEqual(t[0], 0)
        if not t[0] == 0:
            print doctest.__doc__


if __name__ == '__main__':
    unittest.main()