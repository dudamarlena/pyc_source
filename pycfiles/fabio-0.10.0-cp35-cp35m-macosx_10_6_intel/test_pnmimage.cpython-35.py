# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/kieffer/workspace/fabio/build/lib.macosx-10.6-intel-3.5/fabio/test/codecs/test_pnmimage.py
# Compiled at: 2020-04-03 09:02:03
# Size of source mod 2**32: 3031 bytes
"""

Test for PNM images.

Jerome Kieffer, 04/12/2014
"""
__author__ = 'Jerome Kieffer'
__date__ = '07/03/2019'
import os, unittest, numpy, logging
logger = logging.getLogger(__name__)
from fabio.pnmimage import pnmimage
from fabio.openimage import openimage
from ..utilstest import UtilsTest

class TestPNM(unittest.TestCase):
    __doc__ = 'basic test'
    results = 'image0001.pgm  1024 1024  0  28416 353.795654296875   2218.0290682517543'

    def setUp(self):
        """Download files"""
        self.fn = {}
        for j in self.results.split('\n'):
            i = j.split()[0]
            self.fn[i] = UtilsTest.getimage(i + '.bz2')[:-4]

        for i in self.fn:
            if not os.path.exists(self.fn[i]):
                raise AssertionError

    def test_read(self):
        """ check we can read pnm images"""
        vals = self.results.split()
        name = vals[0]
        dim1, dim2 = [int(x) for x in vals[1:3]]
        shape = (dim2, dim1)
        mini, maxi, mean, stddev = [float(x) for x in vals[3:]]
        obj = openimage(self.fn[name])
        self.assertAlmostEqual(mini, obj.getmin(), 4, 'getmin')
        self.assertAlmostEqual(maxi, obj.getmax(), 4, 'getmax')
        self.assertAlmostEqual(mean, obj.getmean(), 4, 'getmean')
        self.assertAlmostEqual(stddev, obj.getstddev(), 4, 'getstddev')
        self.assertEqual(shape, obj.shape)

    def test_write(self):
        pnmfile = os.path.join(UtilsTest.tempdir, 'pnmfile.pnm')
        shape = (9, 11)
        size = shape[0] * shape[1]
        data = numpy.random.randint(0, 65000, size=size).reshape(shape)
        pnmimage(data=data).save(pnmfile)
        with openimage(pnmfile) as (pnm):
            self.assertTrue(numpy.allclose(data, pnm.data), 'data are the same')
        if os.path.exists(pnmfile):
            os.unlink(pnmfile)


def suite():
    loadTests = unittest.defaultTestLoader.loadTestsFromTestCase
    testsuite = unittest.TestSuite()
    testsuite.addTest(loadTests(TestPNM))
    return testsuite


if __name__ == '__main__':
    runner = unittest.TextTestRunner()
    runner.run(suite())