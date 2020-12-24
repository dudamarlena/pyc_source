# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/Newville/Codes/xraylarch/tests/test_read_xafsdata.py
# Compiled at: 2017-04-05 21:43:24
""" Tests of Larch Scripts  """
import unittest, time, ast, numpy as np
from sys import version_info
from utils import TestCase
from larch import Interpreter

class TestScripts(TestCase):
    """test read_ascii() for all example xafsdata"""

    def test_read_ascii(self):
        self.runscript('read_ascii.lar', dirname='larch_scripts')
        assert len(self.session.get_errors()) == 0
        actual = self.session.get_symbol('results')
        expected = self.session.get_symbol('expected')
        for fname, ncol, nrow, labels in expected:
            acol, arow, alabs = actual[fname]
            assert acol == ncol
            assert arow == nrow
            assert alabs == labels


if __name__ == '__main__':
    for suite in (TestScripts,):
        suite = unittest.TestLoader().loadTestsFromTestCase(suite)
        unittest.TextTestRunner(verbosity=13).run(suite)