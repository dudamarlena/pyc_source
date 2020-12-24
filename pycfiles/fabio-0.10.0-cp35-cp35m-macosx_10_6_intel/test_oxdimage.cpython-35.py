# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/kieffer/workspace/fabio/build/lib.macosx-10.6-intel-3.5/fabio/test/codecs/test_oxdimage.py
# Compiled at: 2020-04-03 09:02:03
# Size of source mod 2**32: 6775 bytes
"""
# Unit tests for OXD image (Oxford diffraction now Rigaku)
"""
from __future__ import print_function, with_statement, division, absolute_import
__author__ = 'Jerome Kieffer'
__license__ = 'MIT'
__date__ = '2016-11-23'
__contact__ = 'jerome.kieffer@esrf.fr'
import unittest, os, logging
logger = logging.getLogger(__name__)
import fabio
from fabio.OXDimage import OXDimage
from ..utilstest import UtilsTest
TESTIMAGES = [
 ('b191_1_9_1.img', 512, 512, -500, 11975, 25.7, 90.2526, 'Sapphire2'),
 ('b191_1_9_1_uncompressed.img', 512, 512, -500, 11975, 25.7, 90.2526, 'Sapphire2'),
 ('100nmfilmonglass_1_1.img', 1024, 1024, -172, 460, 44.2, 63.0245, 'Sapphire3'),
 ('pilatus300k.rod_img', 487, 619, -2, 173075, 27.315, 538.938, 'Pilatus')]

class TestOxd(unittest.TestCase):

    def setUp(self):
        self.fn = {}
        for vals in TESTIMAGES:
            name = vals[0]
            self.fn[name] = UtilsTest.getimage(name + '.bz2')[:-4]

        for i in self.fn:
            if not os.path.exists(self.fn[i]):
                raise AssertionError

    def tearDown(self):
        unittest.TestCase.tearDown(self)
        self.fn = {}

    def test_read(self):
        """Test reading of compressed OXD images"""
        for vals in TESTIMAGES:
            name = vals[0]
            dim1, dim2 = vals[1:3]
            shape = (dim2, dim1)
            mini, maxi, mean, stddev = vals[3:7]
            detector_type = vals[7]
            obj = OXDimage()
            obj.read(self.fn[name])
            self.assertEqual(shape, obj.shape)
            self.assertAlmostEqual(mini, obj.getmin(), 2, 'getmin on ' + name)
            self.assertAlmostEqual(maxi, obj.getmax(), 2, 'getmax on ' + name)
            self.assertAlmostEqual(mean, obj.getmean(), 2, 'getmean on ' + name)
            self.assertAlmostEqual(stddev, obj.getstddev(), 2, 'getstddev on ' + name)
            self.assertIn(detector_type, obj.header['Detector type'], 'detector type on ' + name)

    def test_write(self):
        """Test writing with self consistency at the fabio level"""
        for vals in TESTIMAGES:
            name = vals[0]
            obj = OXDimage()
            obj.read(self.fn[name])
            if obj.header.get('Compression') not in ('NO ', 'TY1'):
                logger.info('Skip write test for now')
                continue
                obj.write(os.path.join(UtilsTest.tempdir, name))
                other = OXDimage()
                other.read(os.path.join(UtilsTest.tempdir, name))
                self.assertEqual(abs(obj.data - other.data).max(), 0, 'data are not the same for %s' % name)
                for key in obj.header:
                    if key == 'filename':
                        pass
                    else:
                        self.assertTrue(key in other.header, 'Key %s is in header' % key)
                        self.assertEqual(obj.header[key], other.header[key], "metadata '%s' are not the same for %s" % (key, name))

                os.unlink(os.path.join(UtilsTest.tempdir, name))


class TestOxdSame(unittest.TestCase):

    def setUp(self):
        self.fn = {}
        for i in ['b191_1_9_1.img', 'b191_1_9_1_uncompressed.img']:
            self.fn[i] = UtilsTest.getimage(i + '.bz2')[:-4]

        for i in self.fn:
            if not os.path.exists(self.fn[i]):
                raise AssertionError

    def tearDown(self):
        unittest.TestCase.tearDown(self)
        self.fn = {}

    def test_same(self):
        """test if images are actually the same"""
        o1 = fabio.open(self.fn['b191_1_9_1.img'])
        o2 = fabio.open(self.fn['b191_1_9_1_uncompressed.img'])
        for attr in ['getmin', 'getmax', 'getmean', 'getstddev']:
            a1 = getattr(o1, attr)()
            a2 = getattr(o2, attr)()
            self.assertEqual(a1, a2, 'testing %s: %s | %s' % (attr, a1, a2))


class TestOxdBig(unittest.TestCase):
    __doc__ = 'class to test bugs if OI is large (lot of exceptions 16 bits)'

    def setUp(self):
        self.fn = {}
        for i in ['d80_60s.img', 'd80_60s.edf']:
            self.fn[i] = UtilsTest.getimage(i + '.bz2')[:-4]

        for i in self.fn:
            self.assertTrue(os.path.exists(self.fn[i]), self.fn[i])

    def tearDown(self):
        unittest.TestCase.tearDown(self)
        self.fn = {}

    def test_same(self):
        df = [fabio.open(i).data for i in self.fn.values()]
        self.assertEqual(abs(df[0] - df[1]).max(), 0, 'Data are the same')


class TestConvert(unittest.TestCase):

    def setUp(self):
        self.fn = {}
        for i in ['face.msk']:
            self.fn[i] = UtilsTest.getimage(i + '.bz2')[:-4]

        for i in self.fn:
            self.assertTrue(os.path.exists(self.fn[i]), self.fn[i])

    def tearDown(self):
        unittest.TestCase.tearDown(self)
        self.fn = {}

    def test_convert(self):
        fn = self.fn['face.msk']
        dst = os.path.join(UtilsTest.tempdir, 'face.oxd')
        fabio.open(fn).convert('oxd').save(dst)
        self.assertTrue(os.path.exists(dst), 'destination file exists')
        os.unlink(dst)


def suite():
    loadTests = unittest.defaultTestLoader.loadTestsFromTestCase
    testsuite = unittest.TestSuite()
    testsuite.addTest(loadTests(TestOxd))
    testsuite.addTest(loadTests(TestOxdSame))
    testsuite.addTest(loadTests(TestOxdBig))
    testsuite.addTest(loadTests(TestConvert))
    return testsuite


if __name__ == '__main__':
    runner = unittest.TextTestRunner()
    runner.run(suite())