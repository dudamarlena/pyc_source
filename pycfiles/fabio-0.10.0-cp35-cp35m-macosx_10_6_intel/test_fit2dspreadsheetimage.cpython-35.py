# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/kieffer/workspace/fabio/build/lib.macosx-10.6-intel-3.5/fabio/test/codecs/test_fit2dspreadsheetimage.py
# Compiled at: 2020-04-03 09:02:03
# Size of source mod 2**32: 3311 bytes
"""
Unit tests for the Fit2D spread sheet image format.
"""
from __future__ import print_function, with_statement, division, absolute_import
import unittest, os, logging
from ..utilstest import UtilsTest
logger = logging.getLogger(__name__)
from fabio.fit2dspreadsheetimage import Fit2dSpreadsheetImage
from fabio.utils import testutils
TESTIMAGES = [
 ('example.spr', (512, 512), 86.0, 61204.0, 511.63, 667.148),
 ('example.spr.gz', (512, 512), 86.0, 61204.0, 511.63, 667.148),
 ('example.spr.bz2', (512, 512), 86.0, 61204.0, 511.63, 667.148)]

class TestRealSamples(testutils.ParametricTestCase):
    __doc__ = '\n    Test real samples stored in our archive.\n    '

    @classmethod
    def setUpClass(cls):
        """Prefetch images"""
        download = []
        for datainfo in TESTIMAGES:
            name = datainfo[0]
            if name.endswith('.bz2'):
                download.append(name)
            else:
                if name.endswith('.gz'):
                    download.append(name[:-3] + '.bz2')
                else:
                    download.append(name + '.bz2')

        download = list(set(download))
        for name in download:
            os.path.dirname(UtilsTest.getimage(name))

        cls.im_dir = UtilsTest.resources.data_home

    def test_read(self):
        """ check we can read flat ADSC images"""
        for datainfo in TESTIMAGES:
            with self.subTest(datainfo=datainfo):
                name, shape, mini, maxi, mean, stddev = datainfo
                obj = Fit2dSpreadsheetImage()
                obj.read(os.path.join(self.im_dir, name))
                self.assertAlmostEqual(mini, obj.getmin(), 2, 'getmin')
                self.assertAlmostEqual(maxi, obj.getmax(), 2, 'getmax')
                got_mean = obj.getmean()
                self.assertAlmostEqual(mean, got_mean, 2, 'getmean')
                self.assertAlmostEqual(stddev, obj.getstddev(), 2, 'getstddev')
                self.assertEqual(shape, obj.shape)


def suite():
    loadTests = unittest.defaultTestLoader.loadTestsFromTestCase
    testsuite = unittest.TestSuite()
    testsuite.addTest(loadTests(TestRealSamples))
    return testsuite


if __name__ == '__main__':
    runner = unittest.TextTestRunner()
    runner.run(suite())