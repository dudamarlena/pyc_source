# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/kieffer/workspace/fabio/build/lib.macosx-10.6-intel-3.5/fabio/test/testopenheader.py
# Compiled at: 2019-03-04 08:01:16
# Size of source mod 2**32: 2068 bytes
"""
# Unit tests
Jerome Kieffer, 04/12/2014
"""
from __future__ import print_function, with_statement, division, absolute_import
import unittest, logging
logger = logging.getLogger(__name__)
from fabio.openimage import openheader
from .utilstest import UtilsTest

class Test1(unittest.TestCase):
    __doc__ = 'openheader opening edf'

    def setUp(self):
        self.name = UtilsTest.getimage('F2K_Seb_Lyso0675_header_only.edf.bz2')[:-4]

    def testcase(self):
        """ check openheader can read edf headers"""
        for ext in ['', '.bz2', '.gz']:
            name = self.name + ext
            obj = openheader(name)
            logger.debug(' %s obj = %s' % (name, obj.header))
            self.assertEqual(obj.header['title'], 'ESPIA FRELON Image', 'Error on file %s' % name)


def suite():
    loadTests = unittest.defaultTestLoader.loadTestsFromTestCase
    testsuite = unittest.TestSuite()
    testsuite.addTest(loadTests(Test1))
    return testsuite


if __name__ == '__main__':
    runner = unittest.TextTestRunner()
    runner.run(suite)