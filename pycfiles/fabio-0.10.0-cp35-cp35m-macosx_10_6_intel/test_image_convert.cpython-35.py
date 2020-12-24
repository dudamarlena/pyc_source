# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/kieffer/workspace/fabio/build/lib.macosx-10.6-intel-3.5/fabio/test/test_image_convert.py
# Compiled at: 2019-03-04 08:01:16
# Size of source mod 2**32: 2048 bytes
"""
Deep test to check IOError exceptions
"""
from __future__ import print_function, with_statement, division, absolute_import
import unittest, os, logging
logger = logging.getLogger(__name__)
from .utilstest import UtilsTest
import fabio

class TestImageConvert(unittest.TestCase):
    __doc__ = 'Test image convertions'

    def test_edf_to_tiff(self):
        tmpdir = os.path.join(UtilsTest.tempdir, self.id())
        os.mkdir(tmpdir)
        filename = UtilsTest.getimage('face.edf')
        output_filename = os.path.join(tmpdir, 'face.tif')
        image = fabio.open(filename)
        image2 = image.convert('tiff')
        image2.save(output_filename)
        self.assertEqual(image.shape, image2.shape)
        image3 = fabio.open(output_filename)
        self.assertEqual(image.shape, image3.shape)


def suite():
    loader = unittest.defaultTestLoader.loadTestsFromTestCase
    testsuite = unittest.TestSuite()
    testsuite.addTest(loader(TestImageConvert))
    return testsuite


if __name__ == '__main__':
    runner = unittest.TextTestRunner()
    runner.run(suite())