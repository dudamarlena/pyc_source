# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/kieffer/workspace/fabio/build/lib.macosx-10.6-intel-3.5/fabio/test/testheadernotsingleton.py
# Compiled at: 2019-03-04 08:01:16
# Size of source mod 2**32: 2440 bytes
"""
# Unit tests

# builds on stuff from ImageD11.test.testpeaksearch
28/11/2014
"""
from __future__ import print_function, with_statement, division, absolute_import
import unittest, os, logging
logger = logging.getLogger(__name__)
import fabio, shutil
from .utilstest import UtilsTest

class TestHeaderNotSingleton(unittest.TestCase):

    def setUp(self):
        """
        download images
        """
        self.file1 = UtilsTest.getimage('mb_LP_1_001.img.bz2')[:-4]

    def testheader(self):
        file2 = self.file1.replace('mb_LP_1_001.img', 'mb_LP_1_002.img')
        self.assertTrue(os.path.exists(self.file1))
        if not os.path.exists(file2):
            shutil.copy(self.file1, file2)
        image1 = fabio.open(self.file1)
        image2 = fabio.open(file2)
        self.assertEqual(self.abs_norm(image1.filename), self.abs_norm(self.file1))
        self.assertEqual(self.abs_norm(image2.filename), self.abs_norm(file2))
        self.assertNotEqual(image1.filename, image2.filename)

    def abs_norm(self, fn):
        return os.path.normcase(os.path.abspath(fn))

    def tearDown(self):
        unittest.TestCase.tearDown(self)
        self.file1 = None


def suite():
    loadTests = unittest.defaultTestLoader.loadTestsFromTestCase
    testsuite = unittest.TestSuite()
    testsuite.addTest(loadTests(TestHeaderNotSingleton))
    return testsuite


if __name__ == '__main__':
    runner = unittest.TextTestRunner()
    runner.run(suite())