# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/kieffer/workspace/fabio/build/lib.macosx-10.6-intel-3.5/fabio/test/codecs/test_dm3image.py
# Compiled at: 2020-04-03 09:02:03
# Size of source mod 2**32: 2999 bytes
"""
# Unit tests

# builds on stuff from ImageD11.test.testpeaksearch

Updated by Jerome Kieffer (jerome.kieffer@esrf.eu), 2011

"""
from __future__ import print_function, with_statement, division, absolute_import
__date__ = '07/03/2019'
__author__ = 'jerome Kieffer'
import unittest, os, logging
logger = logging.getLogger(__name__)
import fabio
from fabio.dm3image import Dm3Image
from ..utilstest import UtilsTest
TESTIMAGES = [
 ('ref_d20x_310mm.dm3', (2048, 2048), -31842.354, 23461.672, 569.38782, 1348.4183),
 ('ref_d20x_310mm.dm3.gz', (2048, 2048), -31842.354, 23461.672, 569.38782, 1348.4183),
 ('ref_d20x_310mm.dm3.bz2', (2048, 2048), -31842.354, 23461.672, 569.38782, 1348.4183)]

class TestDm3Image(unittest.TestCase):
    __doc__ = '\n    '

    def setUp(self):
        """ Download images """
        self.im_dir = os.path.dirname(UtilsTest.getimage('ref_d20x_310mm.dm3.bz2'))

    def test_read(self):
        """ check we can read dm3 images"""
        for info in TESTIMAGES:
            name, shape, mini, maxi, mean, stddev = info
            fname = os.path.join(self.im_dir, name)
            obj1 = Dm3Image()
            obj1.read(fname)
            obj2 = fabio.open(fname)
            for obj in (obj1, obj2):
                self.assertAlmostEqual(mini, obj.getmin(), 2, 'getmin')
                self.assertAlmostEqual(maxi, obj.getmax(), 2, 'getmax')
                got_mean = obj.getmean()
                self.assertAlmostEqual(mean, got_mean, 2, 'getmean exp %s != got %s' % (mean, got_mean))
                self.assertAlmostEqual(stddev, obj.getstddev(), 2, 'getstddev')
                self.assertEqual(shape, obj.shape)


def suite():
    loadTests = unittest.defaultTestLoader.loadTestsFromTestCase
    testsuite = unittest.TestSuite()
    testsuite.addTest(loadTests(TestDm3Image))
    return testsuite


if __name__ == '__main__':
    runner = unittest.TextTestRunner()
    runner.run(suite())