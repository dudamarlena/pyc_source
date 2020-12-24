# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/kieffer/workspace/fabio/build/lib.macosx-10.6-intel-3.5/fabio/test/codecs/test_fit2dimage.py
# Compiled at: 2020-04-03 09:02:03
# Size of source mod 2**32: 3407 bytes
"""Test for FabIO reader for Fit2D binary images
"""
from __future__ import with_statement, print_function, division, absolute_import
__authors__ = [
 'Jérôme Kieffer']
__contact__ = 'jerome.kiefer@esrf.fr'
__license__ = 'MIT'
__copyright__ = '2016-2016 European Synchrotron Radiation Facility'
__date__ = '07/03/2019'
import unittest, numpy, logging
logger = logging.getLogger(__name__)
import fabio
from fabio.fit2dimage import fit2dimage
from ..utilstest import UtilsTest

class TestFit2DImage(unittest.TestCase):
    __doc__ = ' A few random clicks to make a test mask '

    def setUp(self):
        """
        download images
        """
        self.filename = UtilsTest.getimage('fit2d.f2d.bz2')[:-4]
        self.tiffilename = UtilsTest.getimage('fit2d.tif.bz2')[:-4]

    def test_read(self):
        """ Check it reads a mask OK """
        i = fit2dimage()
        i.read(self.filename)
        self.assertEqual(i.shape, (28, 25))
        self.assertEqual(i.bpp, 4)
        self.assertEqual(i.bytecode, numpy.float32)
        self.assertEqual(i.data.shape, (28, 25))

    def test_match(self):
        """ test edf and msk are the same """
        i = fabio.open(self.filename)
        j = fabio.open(self.tiffilename)
        i.read(self.filename)
        self.assertEqual(i.data.shape, j.data.shape)
        diff = j.data - numpy.flipud(i.data)
        sumd = abs(diff).sum(dtype=float)
        self.assertEqual(sumd, 0)

    def test_mask(self):
        img = fabio.open(UtilsTest.getimage('Pilatus1M.f2d.bz2'))
        cbf = fabio.open(UtilsTest.getimage('Pilatus1M.cbf.bz2'))
        msk = fabio.open(UtilsTest.getimage('Pilatus1M.msk.bz2'))
        diff = abs(img.data.astype('int32') - cbf.data)
        self.assertEqual(diff.sum(), 0)
        diff = abs(msk.data.astype('int32') - img.header['data_mask'].astype('int32'))
        self.assertEqual(diff.sum(), 0)


def suite():
    loadTests = unittest.defaultTestLoader.loadTestsFromTestCase
    testsuite = unittest.TestSuite()
    testsuite.addTest(loadTests(TestFit2DImage))
    return testsuite


if __name__ == '__main__':
    runner = unittest.TextTestRunner()
    runner.run(suite())