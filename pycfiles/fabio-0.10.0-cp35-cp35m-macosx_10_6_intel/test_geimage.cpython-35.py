# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/kieffer/workspace/fabio/build/lib.macosx-10.6-intel-3.5/fabio/test/codecs/test_geimage.py
# Compiled at: 2020-04-03 09:02:03
# Size of source mod 2**32: 2725 bytes
"""
# Unit tests

# builds on stuff from ImageD11.test.testpeaksearch
28/11/2014
"""
from __future__ import print_function, with_statement, division, absolute_import
import unittest, os, logging
from ..utilstest import UtilsTest
logger = logging.getLogger(__name__)
from fabio.GEimage import GEimage
TESTIMAGES = 'GE_aSI_detector_image_1529      2048 2048 1515 16353 1833.0311 56.9124\n                GE_aSI_detector_image_1529.gz   2048 2048 1515 16353 1833.0311 56.9124\n                GE_aSI_detector_image_1529.bz2  2048 2048 1515 16353 1833.0311 56.9124'

class TestGE(unittest.TestCase):

    def setUp(self):
        """
        download images
        """
        self.GE = UtilsTest.getimage('GE_aSI_detector_image_1529.bz2')

    def test_read(self):
        for line in TESTIMAGES.split('\n'):
            vals = line.split()
            name = vals[0]
            dim1, dim2 = [int(x) for x in vals[1:3]]
            shape = (dim2, dim1)
            mini, maxi, mean, stddev = [float(x) for x in vals[3:]]
            obj = GEimage()
            obj.read(os.path.join(os.path.dirname(self.GE), name))
            self.assertAlmostEqual(mini, obj.getmin(), 4, 'getmin')
            self.assertAlmostEqual(maxi, obj.getmax(), 4, 'getmax')
            self.assertAlmostEqual(mean, obj.getmean(), 4, 'getmean')
            self.assertAlmostEqual(stddev, obj.getstddev(), 4, 'getstddev')
            self.assertEqual(shape, obj.shape)


def suite():
    loadTests = unittest.defaultTestLoader.loadTestsFromTestCase
    testsuite = unittest.TestSuite()
    testsuite.addTest(loadTests(TestGE))
    return testsuite


if __name__ == '__main__':
    runner = unittest.TextTestRunner()
    runner.run(suite())