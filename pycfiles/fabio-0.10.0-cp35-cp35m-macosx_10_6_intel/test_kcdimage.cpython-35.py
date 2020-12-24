# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/kieffer/workspace/fabio/build/lib.macosx-10.6-intel-3.5/fabio/test/codecs/test_kcdimage.py
# Compiled at: 2020-04-03 09:02:03
# Size of source mod 2**32: 3256 bytes
"""

Test for Nonius Kappa CCD cameras.

"""
from __future__ import print_function, with_statement, division, absolute_import
import unittest, os, logging
logger = logging.getLogger(__name__)
import fabio
from ...kcdimage import kcdimage
from ...openimage import openimage
from ..utilstest import UtilsTest

class TestKcd(unittest.TestCase):
    __doc__ = 'basic test'
    kcdfilename = 'i01f0001.kcd'
    edffilename = 'i01f0001.edf'
    results = 'i01f0001.kcd   625 576  96  66814.0 195.3862972   243.58150990245315'

    def setUp(self):
        """Download files"""
        self.fn = {}
        for i in ['i01f0001.kcd', 'i01f0001.edf']:
            self.fn[i] = UtilsTest.getimage(i + '.bz2')[:-4]

        for i in self.fn:
            if not os.path.exists(self.fn[i]):
                raise AssertionError

    def test_read(self):
        """ check we can read kcd images"""
        vals = self.results.split()
        dim1, dim2 = [int(x) for x in vals[1:3]]
        shape = (dim2, dim1)
        mini, maxi, mean, stddev = [float(x) for x in vals[3:]]
        for ext in ['', '.gz', '.bz2']:
            try:
                obj = openimage(self.fn[self.kcdfilename] + ext)
            except Exception as err:
                logger.error('unable to read: %s', self.fn[self.kcdfilename] + ext)
                raise err

            self.assertAlmostEqual(mini, obj.getmin(), 4, 'getmin' + ext)
            self.assertAlmostEqual(maxi, obj.getmax(), 4, 'getmax' + ext)
            self.assertAlmostEqual(mean, obj.getmean(), 4, 'getmean' + ext)
            self.assertAlmostEqual(stddev, obj.getstddev(), 4, 'getstddev' + ext)
            self.assertEqual(shape, obj.shape, 'shape' + ext)

    def test_same(self):
        """ see if we can read kcd images and if they are the same as the EDF """
        kcd = kcdimage()
        kcd.read(self.fn[self.kcdfilename])
        edf = fabio.open(self.fn[self.edffilename])
        diff = kcd.data.astype('int32') - edf.data.astype('int32')
        self.assertAlmostEqual(abs(diff).sum(dtype=int), 0, 4)


def suite():
    loadTests = unittest.defaultTestLoader.loadTestsFromTestCase
    testsuite = unittest.TestSuite()
    testsuite.addTest(loadTests(TestKcd))
    return testsuite


if __name__ == '__main__':
    runner = unittest.TextTestRunner()
    runner.run(suite())