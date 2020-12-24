# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/evax/bitten/tools/tests.py
# Compiled at: 2010-07-27 02:21:18
import os, unittest, shutil, tempfile
from bitten.recipe import Context
from evax.bitten.tools.check import check
from evax.bitten.tools.lcov import lcov

class EvaxBittenToolsTestCase(unittest.TestCase):

    def setUp(self):
        self.basedir = os.path.realpath(tempfile.mkdtemp())
        self.ctxt = Context(self.basedir)

    def tearDown(self):
        shutil.rmtree(self.basedir)


class CheckTestCase(EvaxBittenToolsTestCase):

    def test_missing_param_reports(self):
        self.assertRaises(AssertionError, check, self.ctxt)


class LCovTestCase(EvaxBittenToolsTestCase):

    def test_missing_param_directory(self):
        self.assertRaises(AssertionError, lcov, self.ctxt)


def get_suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(CheckTestCase, 'test'))
    suite.addTest(unittest.makeSuite(LCovTestCase, 'test'))
    return suite


if __name__ == '__main__':
    unittest.main(defaultTest='get_suite')