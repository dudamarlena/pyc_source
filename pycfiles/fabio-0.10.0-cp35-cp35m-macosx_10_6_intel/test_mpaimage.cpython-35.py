# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/kieffer/workspace/fabio/build/lib.macosx-10.6-intel-3.5/fabio/test/codecs/test_mpaimage.py
# Compiled at: 2020-04-03 09:02:03
# Size of source mod 2**32: 2555 bytes
"""Multiwire Unit tests"""
from __future__ import print_function, with_statement, division, absolute_import
import unittest, logging
logger = logging.getLogger(__name__)
import fabio
from ..utilstest import UtilsTest

class TestMpa(unittest.TestCase):
    __doc__ = '\n    Test classe for multiwire (mpa) images\n    '
    TESTIMAGES = [
     ('mpa_test.mpa', 1024, 1024, 0, 1295, 0.859, 18.9393)]

    def test_read(self):
        """
        Test the reading of multiwire images
        """
        for imageData in self.TESTIMAGES:
            name, dim1, dim2, mini, maxi, mean, stddev = imageData
            shape = (dim2, dim1)
            logger.debug('Processing: %s' % name)
            path = UtilsTest.getimage(name + '.bz2')[:-4]
            obj = fabio.mpaimage.MpaImage()
            obj.read(path)
            self.assertAlmostEqual(mini, obj.getmin(), 2, 'getmin [%s,%s]' % (mini, obj.getmin()))
            self.assertAlmostEqual(maxi, obj.getmax(), 2, 'getmax [%s,%s]' % (maxi, obj.getmax()))
            self.assertAlmostEqual(mean, obj.getmean(), 2, 'getmean [%s,%s]' % (mean, obj.getmean()))
            self.assertAlmostEqual(stddev, obj.getstddev(), 2, 'getstddev [%s,%s]' % (stddev, obj.getstddev()))
            self.assertEqual(shape, obj.shape)


def suite():
    loadTests = unittest.defaultTestLoader.loadTestsFromTestCase
    testsuite = unittest.TestSuite()
    testsuite.addTest(loadTests(TestMpa))
    return testsuite


if __name__ == '__main__':
    runner = unittest.TextTestRunner()
    runner.run(suite())