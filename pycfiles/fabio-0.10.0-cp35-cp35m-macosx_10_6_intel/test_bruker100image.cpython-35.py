# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/kieffer/workspace/fabio/build/lib.macosx-10.6-intel-3.5/fabio/test/codecs/test_bruker100image.py
# Compiled at: 2020-04-03 09:02:03
# Size of source mod 2**32: 3955 bytes
"""
#bruker100 Unit tests

19/01/2015
"""
from __future__ import print_function, with_statement, division, absolute_import
import unittest, os, logging
logger = logging.getLogger(__name__)
from fabio.bruker100image import Bruker100Image
from fabio.openimage import openimage
from ..utilstest import UtilsTest
TESTIMAGES = 'NaCl_10_01_0009.sfrm         512 512 -30 5912 34.4626 26.189\n                NaCl_10_01_0009.sfrm.gz      512 512 -30 5912 34.4626 26.189\n                NaCl_10_01_0009.sfrm.bz2     512 512 -30 5912 34.4626 26.189'
REFIMAGE = 'NaCl_10_01_0009.npy.bz2'

class TestBruker100(unittest.TestCase):
    __doc__ = ' check some read data from bruker version100 detector'

    def setUp(self):
        """
        download images
        """
        UtilsTest.getimage(REFIMAGE)
        self.im_dir = os.path.dirname(UtilsTest.getimage(TESTIMAGES.split()[0] + '.bz2'))

    def test_read(self):
        """ check we can read bruker100 images"""
        for line in TESTIMAGES.split('\n'):
            vals = line.split()
            name = vals[0]
            dim1, dim2 = [int(x) for x in vals[1:3]]
            shape = (dim2, dim1)
            mini, maxi, mean, stddev = [float(x) for x in vals[3:]]
            obj = Bruker100Image()
            obj.read(os.path.join(self.im_dir, name))
            self.assertAlmostEqual(mini, obj.getmin(), 2, 'getmin')
            self.assertAlmostEqual(maxi, obj.getmax(), 2, 'getmax')
            self.assertAlmostEqual(mean, obj.getmean(), 2, 'getmean')
            self.assertAlmostEqual(stddev, obj.getstddev(), 2, 'getstddev')
            self.assertEqual(shape, obj.shape)

    def test_same(self):
        """ check we can read bruker100 images"""
        ref = openimage(os.path.join(self.im_dir, REFIMAGE))
        for line in TESTIMAGES.split('\n'):
            obt = openimage(os.path.join(self.im_dir, line.split()[0]))
            self.assertTrue(abs(ref.data - obt.data).max() == 0, 'data are the same')

    def test_write(self):
        fname = TESTIMAGES.split()[0]
        obt = openimage(os.path.join(self.im_dir, fname))
        name = os.path.basename(fname)
        obj = Bruker100Image(data=obt.data, header=obt.header)
        obj.write(os.path.join(UtilsTest.tempdir, name))
        other = openimage(os.path.join(UtilsTest.tempdir, name))
        self.assertEqual(abs(obt.data - other.data).max(), 0, 'data are the same')
        for key in obt.header:
            self.assertTrue(key in other.header, 'Key %s is in header' % key)
            self.assertEqual(obt.header[key], other.header[key], 'value are the same for key %s' % key)

        os.unlink(os.path.join(UtilsTest.tempdir, name))


def suite():
    loadTests = unittest.defaultTestLoader.loadTestsFromTestCase
    testsuite = unittest.TestSuite()
    testsuite.addTest(loadTests(TestBruker100))
    return testsuite


if __name__ == '__main__':
    runner = unittest.TextTestRunner()
    runner.run(suite())