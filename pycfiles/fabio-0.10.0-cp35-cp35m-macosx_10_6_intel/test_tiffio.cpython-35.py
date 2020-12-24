# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/kieffer/workspace/fabio/build/lib.macosx-10.6-intel-3.5/fabio/test/test_tiffio.py
# Compiled at: 2019-03-04 08:01:16
# Size of source mod 2**32: 3261 bytes
"""
Test to check TiffIO
"""
from __future__ import print_function, with_statement, division, absolute_import
import unittest, os, logging, numpy
logger = logging.getLogger(__name__)
from .utilstest import UtilsTest
from ..TiffIO import TiffIO

class TestTiffIO(unittest.TestCase):
    __doc__ = 'Test the class format'

    def write(self, filename):
        tif = TiffIO(filename, mode='wb+')
        dtype = numpy.uint16
        data = numpy.arange(10000).astype(dtype)
        data.shape = (100, 100)
        tif.writeImage(data, info={'Title': '1st'})
        tif = None

    def test_write(self):
        filename = '%s.tiff' % self.id()
        filename = os.path.join(UtilsTest.tempdir, filename)
        self.write(filename)

    def test_append(self):
        filename = '%s.tiff' % self.id()
        filename = os.path.join(UtilsTest.tempdir, filename)
        self.write(filename)
        tif = TiffIO(filename, mode='rb+')
        dtype = numpy.uint16
        data = numpy.arange(100).astype(dtype)
        data.shape = (10, 10)
        tif.writeImage((data * 2).astype(dtype), info={'Title': '2nd'})
        self.assertEqual(tif.getNumberOfImages(), 2)
        tif = None

    def test_read(self):
        filename = '%s.tiff' % self.id()
        filename = os.path.join(UtilsTest.tempdir, filename)
        self.write(filename)
        tif = TiffIO(filename)
        self.assertEqual(tif.getNumberOfImages(), 1)
        for i in range(tif.getNumberOfImages()):
            info = tif.getInfo(i)
            for key in info:
                if key not in ('colormap', ):
                    logger.info('%s = %s', key, info[key])
                elif info['colormap'] is not None:
                    logger.info('RED   %s = %s', key, info[key][0:10, 0])
                    logger.info('GREEN %s = %s', key, info[key][0:10, 1])
                    logger.info('BLUE  %s = %s', key, info[key][0:10, 2])

            data = tif.getImage(i)[0, 0:10]
            logger.info('data [0, 0:10] = %s', data)


def suite():
    loader = unittest.defaultTestLoader.loadTestsFromTestCase
    testsuite = unittest.TestSuite()
    testsuite.addTest(loader(TestTiffIO))
    return testsuite


if __name__ == '__main__':
    runner = unittest.TextTestRunner()
    runner.run(suite())