# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/kieffer/workspace/fabio/build/lib.macosx-10.6-intel-3.5/fabio/test/codecs/test_jpeg2kimage.py
# Compiled at: 2020-04-03 09:02:03
# Size of source mod 2**32: 5222 bytes
"""
Test JPEG 2000 format
"""
from __future__ import print_function, with_statement, division, absolute_import
import unittest, numpy, logging
try:
    from PIL import Image
except ImportError:
    Image = None

logger = logging.getLogger(__name__)
import fabio
from ... import jpeg2kimage
from ..utilstest import UtilsTest

def isPilUsable():
    if jpeg2kimage.PIL is None:
        return False
        try:
            if hasattr(jpeg2kimage.PIL.Image, 'frombytes'):
                frombytes = jpeg2kimage.PIL.Image.frombytes
            else:
                frombytes = jpeg2kimage.PIL.Image.frombuffer
            frombytes('1', (2, 2), b'', decoder_name='jpeg2k')
        except Exception as e:
            if e.args[0] == 'decoder jpeg2k not available':
                return False

        return True


def isGlymurUsable():
    if jpeg2kimage.glymur is None:
        return False
    import glymur
    if glymur.version.openjpeg_version_tuple < [1, 5, 0]:
        return False
    return True


class TestJpeg2KImage(unittest.TestCase):
    __doc__ = 'Test the class format'

    def setUp(self):
        if not isPilUsable() and not isGlymurUsable():
            self.skipTest('PIL nor glymur are available')

    def loadImage(self, filename):
        image_format = jpeg2kimage.Jpeg2KImage()
        image = image_format.read(filename)
        return image

    def test_open_uint8(self):
        filename = 'binned_data_uint8.jp2'
        filename = UtilsTest.getimage(filename + '.bz2')[:-4]
        image = self.loadImage(filename)
        self.assertEqual(image.data.shape, (120, 120))
        self.assertEqual(image.data.dtype, numpy.uint8)

    def test_open_uint16(self):
        filename = 'binned_data_uint16.jp2'
        filename = UtilsTest.getimage(filename + '.bz2')[:-4]
        image_format = jpeg2kimage.Jpeg2KImage()
        image = image_format.read(filename)
        self.assertEqual(image.data.shape, (120, 120))
        self.assertEqual(image.data.dtype, numpy.uint16)

    def test_open_wrong_format(self):
        filename = 'MultiFrame.edf'
        filename = UtilsTest.getimage(filename + '.bz2')[:-4]
        image_format = jpeg2kimage.Jpeg2KImage()
        try:
            _image = image_format.read(filename)
            self.fail()
        except IOError:
            pass

    def test_open_missing_file(self):
        filename = '___missing_file___.___'
        image_format = jpeg2kimage.Jpeg2KImage()
        try:
            _image = image_format.read(filename)
            self.fail()
        except IOError:
            pass


class TestJpeg2KImage_PIL(TestJpeg2KImage):
    __doc__ = 'Test the class format using a specific decoder'

    def setUp(self):
        if not isPilUsable() and not isGlymurUsable():
            self.skipTest('PIL is not available')

    @classmethod
    def setUpClass(cls):
        cls.old = jpeg2kimage.glymur
        jpeg2kimage.glymur = None

    @classmethod
    def tearDownClass(cls):
        jpeg2kimage.glymur = cls.old
        cls.old = None


class TestJpeg2KImage_glymur(TestJpeg2KImage):
    __doc__ = 'Test the class format using a specific decoder'

    def setUp(self):
        if not isGlymurUsable():
            self.skipTest('glymur is not available')

    @classmethod
    def setUpClass(cls):
        cls.old = jpeg2kimage.PIL
        jpeg2kimage.PIL = None

    @classmethod
    def tearDownClass(cls):
        jpeg2kimage.PIL = cls.old
        cls.old = None


class TestJpeg2KImage_fabio(TestJpeg2KImage):
    __doc__ = 'Test the format inside the fabio framework'

    def loadImage(self, filename):
        """Use the fabio API instead of using the image format"""
        image = fabio.open(filename)
        return image


def suite():
    loader = unittest.defaultTestLoader.loadTestsFromTestCase
    testsuite = unittest.TestSuite()
    testsuite.addTest(loader(TestJpeg2KImage))
    testsuite.addTest(loader(TestJpeg2KImage_PIL))
    testsuite.addTest(loader(TestJpeg2KImage_glymur))
    testsuite.addTest(loader(TestJpeg2KImage_fabio))
    return testsuite


if __name__ == '__main__':
    runner = unittest.TextTestRunner()
    runner.run(suite())