# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/kieffer/workspace/fabio/build/lib.macosx-10.6-intel-3.5/fabio/test/codecs/test_raxisimage.py
# Compiled at: 2020-04-03 09:02:03
# Size of source mod 2**32: 4323 bytes
"""
# Unit tests for raxis images
28/11/2014
"""
from __future__ import print_function, with_statement, division
import unittest, os, logging
logger = logging.getLogger(__name__)
import fabio
from fabio.raxisimage import raxisimage
from ..utilstest import UtilsTest
TESTIMAGES = 'mgzn-20hpt.img     2300 1280 16 15040  287.82 570.72\n                mgzn-20hpt.img.bz2 2300 1280 16 15040  287.82 570.72\n                mgzn-20hpt.img.gz  2300 1280 16 15040  287.82 570.72'

class TestRaxisImage(unittest.TestCase):

    def setUp(self):
        """
        download images
        """
        self.mar = UtilsTest.getimage('mgzn-20hpt.img.bz2')[:-4]

    def test_read(self):
        """
        Test the reading of Mar345 images
        """
        for line in TESTIMAGES.split('\n'):
            vals = line.strip().split()
            name = vals[0]
            logger.debug('Testing file %s' % name)
            dim1, dim2 = [int(x) for x in vals[1:3]]
            shape = (dim2, dim1)
            mini, maxi, mean, stddev = [float(x) for x in vals[3:]]
            obj = raxisimage()
            obj.read(os.path.join(os.path.dirname(self.mar), name))
            self.assertAlmostEqual(mini, obj.getmin(), 2, 'getmin [%s,%s]' % (mini, obj.getmin()))
            self.assertAlmostEqual(maxi, obj.getmax(), 2, 'getmax [%s,%s]' % (maxi, obj.getmax()))
            self.assertAlmostEqual(mean, obj.getmean(), 2, 'getmean [%s,%s]' % (mean, obj.getmean()))
            self.assertAlmostEqual(stddev, obj.getstddev(), 2, 'getstddev [%s,%s]' % (stddev, obj.getstddev()))
            self.assertEqual(shape, obj.shape)

    def _test_write(self):
        self.skipTest('Write is not implemented')
        for line in TESTIMAGES.split('\n'):
            logger.debug('Processing file: %s' % line)
            vals = line.split()
            name = vals[0]
            obj = raxisimage()
            obj.read(os.path.join(os.path.dirname(self.mar), name))
            obj.write(os.path.join(UtilsTest.tempdir, name))
            other = raxisimage()
            other.read(os.path.join(UtilsTest.tempdir, name))
            self.assertEqual(abs(obj.data - other.data).max(), 0, 'data are the same')
            for key in obj.header:
                if key == 'filename':
                    pass
                else:
                    self.assertTrue(key in other.header, 'Key %s is in header' % key)
                    self.assertEqual(obj.header[key], other.header[key], 'value are the same for key %s: [%s|%s]' % (key, obj.header[key], other.header[key]))

            os.unlink(os.path.join(UtilsTest.tempdir, name))

    def test_memoryleak(self):
        """
        This test takes a lot of time, so only in debug mode.
        """
        N = 1000
        if logger.getEffectiveLevel() == logging.DEBUG:
            logger.debug('Testing for memory leak')
            for _ in range(N):
                _img = fabio.open(self.mar)


def suite():
    loadTests = unittest.defaultTestLoader.loadTestsFromTestCase
    testsuite = unittest.TestSuite()
    testsuite.addTest(loadTests(TestRaxisImage))
    return testsuite


if __name__ == '__main__':
    runner = unittest.TextTestRunner()
    runner.run(suite())