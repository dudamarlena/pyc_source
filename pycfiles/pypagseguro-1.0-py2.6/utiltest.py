# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
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