# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/kieffer/workspace/fabio/build/lib.macosx-10.6-intel-3.5/fabio/test/codecs/test_pixiimage.py
# Compiled at: 2020-04-03 09:02:03
# Size of source mod 2**32: 4960 bytes
"""
Deep test to check IOError exceptions
"""
from __future__ import print_function, with_statement, division, absolute_import
import unittest, os, logging
logger = logging.getLogger(__name__)
import fabio
from ..utilstest import UtilsTest
from ..test_frames import _CommonTestFrames

class TestPixiImage(_CommonTestFrames):
    __doc__ = 'Test the class format'

    @classmethod
    def setUpClass(cls):
        cls.create_fake_images()
        super(TestPixiImage, cls).setUpClass()

    @classmethod
    def getMeta(cls):

        class Meta(object):
            pass

        meta = Meta()
        meta.image = None
        meta.filename = cls.multi_frame
        meta.nframes = 3
        return meta

    @classmethod
    def create_fake_images(cls):
        """Create PiXi image.

        This images was generated using our Python code as specification.
        Then it's not a very good way to test our code.
        """
        frame1 = b'\x01\x00' * 476 + b'\x00\x00' * 476 * 511
        frame2 = b'\x02\x00' * 476 + b'\x00\x00' * 476 * 511
        frame3 = b'\x03\x00' * 476 + b'\x00\x00' * 476 * 511
        header = b'\n\xb8\x03\x00' + b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
        cls.single_frame = os.path.join(UtilsTest.tempdir, 'pixi_1frame.dat')
        with open(cls.single_frame, 'wb') as (f):
            f.write(header)
            f.write(frame1)
        cls.multi_frame = os.path.join(UtilsTest.tempdir, 'pixi_3frame.dat')
        with open(cls.multi_frame, 'wb') as (f):
            f.write(header)
            f.write(frame1)
            f.write(header)
            f.write(frame2)
            f.write(header)
            f.write(frame3)
        template = os.path.join(UtilsTest.tempdir, 'pixi_series.dat') + '$%04d'
        cls.file_series = template % 0
        frames = [frame1, frame2, frame3]
        for num, frame in enumerate(frames):
            filename = template % num
            with open(filename, 'wb') as (f):
                f.write(header)
                f.write(frame)

    def test_single_frame(self):
        image = fabio.open(self.single_frame)
        self.assertEqual(image.nframes, 1)
        self.assertEqual(image.data.shape, (512, 476))
        self.assertEqual(image.data[(0, 0)], 1)
        self.assertEqual(image.data[(1, 1)], 0)

    def test_multi_frame(self):
        image = fabio.open(self.multi_frame)
        self.assertEqual(image.nframes, 3)
        self.assertEqual(image.data.shape, (512, 476))
        self.assertEqual(image.data[(0, 0)], 1)
        self.assertEqual(image.data[(1, 1)], 0)
        frame = image.getframe(0)
        self.assertEqual(frame.data[(0, 0)], 1)
        self.assertEqual(frame.data[(1, 1)], 0)
        frame = image.getframe(1)
        self.assertEqual(frame.data[(0, 0)], 2)
        self.assertEqual(frame.data[(1, 1)], 0)
        frame = image.getframe(2)
        self.assertEqual(frame.data[(0, 0)], 3)
        self.assertEqual(frame.data[(1, 1)], 0)

    def test_file_series(self):
        image = fabio.open(self.file_series)
        self.assertEqual(image.data.shape, (512, 476))
        self.assertEqual(image.data[(0, 0)], 1)
        self.assertEqual(image.data[(1, 1)], 0)
        frame = image.getframe(0)
        self.assertEqual(frame.data[(0, 0)], 1)
        self.assertEqual(frame.data[(1, 1)], 0)
        frame = image.getframe(1)
        self.assertEqual(frame.data[(0, 0)], 2)
        self.assertEqual(frame.data[(1, 1)], 0)
        frame = image.getframe(2)
        self.assertEqual(frame.data[(0, 0)], 3)
        self.assertEqual(frame.data[(1, 1)], 0)
        frame = frame.getframe(0)
        self.assertEqual(frame.data[(0, 0)], 1)
        self.assertEqual(frame.data[(1, 1)], 0)


def suite():
    loader = unittest.defaultTestLoader.loadTestsFromTestCase
    testsuite = unittest.TestSuite()
    testsuite.addTest(loader(TestPixiImage))
    return testsuite


if __name__ == '__main__':
    runner = unittest.TextTestRunner()
    runner.run(suite())