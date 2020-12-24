# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/kieffer/workspace/fabio/build/lib.macosx-10.6-intel-3.5/fabio/test/codecs/test_jpegimage.py
# Compiled at: 2020-04-03 09:02:03
# Size of source mod 2**32: 4952 bytes
"""
Test JPEG format
"""
from __future__ import print_function, with_statement, division, absolute_import
import unittest, os, shutil, logging
logger = logging.getLogger(__name__)
import fabio
from ... import jpegimage
from ..utilstest import UtilsTest
TEST_DIRECTORY = None

def setUpModule():
    global TEST_DIRECTORY
    TEST_DIRECTORY = os.path.join(UtilsTest.tempdir, __name__)
    os.makedirs(TEST_DIRECTORY)


def tearDownModule():
    shutil.rmtree(TEST_DIRECTORY)


class TestJpegImage(unittest.TestCase):
    __doc__ = 'Test the class format'

    def setUp(self):
        if jpegimage.Image is None:
            self.skipTest('PIL is not available')

    def test_read_uint8(self):
        filename = UtilsTest.getimage('rand_uint8.jpg.bz2')[:-4]
        image_format = jpegimage.JpegImage()
        image = image_format.read(filename)
        self.assertEqual(image.data.shape, (64, 64))
        self.assertIn('jfif', image.header)

    def test_read_failing_file(self):
        filename = os.path.join(TEST_DIRECTORY, '2.jpg')
        filename_source = UtilsTest.getimage('rand_uint8.jpg.bz2')[:-4]
        with open(filename_source, 'r+b') as (fsource):
            with open(filename, 'w+b') as (ftest):
                ftest.write(fsource.read())
                ftest.seek(1)
                ftest.write(b'.')
        image_format = jpegimage.JpegImage()
        try:
            _image = image_format.read(filename)
            self.fail()
        except IOError:
            pass

    def test_read_empty_file(self):
        filename = os.path.join(TEST_DIRECTORY, '3.jpg')
        f = open(filename, 'wb')
        f.close()
        image_format = jpegimage.JpegImage()
        try:
            _image = image_format.read(filename)
            self.fail()
        except IOError:
            pass

    def test_read_missing_file(self):
        filename = os.path.join(TEST_DIRECTORY, '4.jpg')
        image_format = jpegimage.JpegImage()
        try:
            _image = image_format.read(filename)
            self.fail()
        except IOError:
            pass


class TestPilNotAvailable(unittest.TestCase):

    def setUp(self):
        filename = UtilsTest.getimage('rand_uint8.jpg.bz2')[:-4]
        self.filename = filename
        self.old = jpegimage.Image

    def tearDown(self):
        jpegimage.Image = self.old
        self.filename = None
        self.data = None

    def open_image(self):
        return fabio.open(self.filename)

    def test_with_pil(self):
        if jpegimage.Image is None:
            self.skipTest('PIL is not available')
        image = self.open_image()
        self.assertIsInstance(image, jpegimage.JpegImage)
        self.assertEqual(image.data.shape, (64, 64))
        self.assertIn('jfif', image.header)

    def test_without_pil(self):
        try:
            old = jpegimage.Image
            jpegimage.Image = None
            try:
                _image = self.open_image()
                self.fail()
            except IOError:
                pass

        finally:
            jpegimage.Image = old


class TestJpegImageInsideFabio(unittest.TestCase):
    __doc__ = 'Test the format inside the fabio framework'

    def test_read_uint8(self):
        if jpegimage.Image is None:
            self.skipTest('PIL is not available')
        filename = UtilsTest.getimage('rand_uint8.jpg.bz2')[:-4]
        image = fabio.open(filename)
        self.assertIsInstance(image, jpegimage.JpegImage)
        self.assertEqual(image.data.shape, (64, 64))
        self.assertIn('jfif', image.header)


def suite():
    loader = unittest.defaultTestLoader.loadTestsFromTestCase
    testsuite = unittest.TestSuite()
    testsuite.addTest(loader(TestJpegImage))
    testsuite.addTest(loader(TestJpegImageInsideFabio))
    testsuite.addTest(loader(TestPilNotAvailable))
    return testsuite


if __name__ == '__main__':
    runner = unittest.TextTestRunner()
    runner.run(suite())