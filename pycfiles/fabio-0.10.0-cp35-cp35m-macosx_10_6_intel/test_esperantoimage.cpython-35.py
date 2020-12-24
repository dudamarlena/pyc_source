# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/kieffer/workspace/fabio/build/lib.macosx-10.6-intel-3.5/fabio/test/codecs/test_esperantoimage.py
# Compiled at: 2020-04-03 09:02:03
# Size of source mod 2**32: 2954 bytes
"""Test Esperanto images
"""
from __future__ import print_function, with_statement, division, absolute_import
import fabio.esperantoimage
from ..utilstest import UtilsTest
import unittest, logging
logger = logging.getLogger(__name__)

class TestEsperanto(unittest.TestCase):
    TESTIMAGES = [
     ('sucrose_1s__1_1.esperanto.bz2', 2048, 2048, 0, 65535, 8546.6414, 1500.4198)]

    def test_read(self):
        """
        Test the reading of Mar345 images
        """
        for params in self.TESTIMAGES:
            name = params[0]
            logger.debug('Processing: %s' % name)
            dim1, dim2 = params[1:3]
            shape = (dim2, dim1)
            mini, maxi, mean, stddev = params[3:]
            obj = fabio.esperantoimage.EsperantoImage()
            obj.read(UtilsTest.getimage(name))
            self.assertEqual(shape, obj.shape, 'dim1')

    def test_header(self):
        for params in self.TESTIMAGES:
            name = params[0]
            logger.debug('Processing: %s' % name)
            obj = fabio.esperantoimage.EsperantoImage()
            obj.read(UtilsTest.getimage(name))
            expected_keys = set([
             'IMAGE',
             'SPECIAL_CCD_1',
             'SPECIAL_CCD_2',
             'SPECIAL_CCD_3',
             'SPECIAL_CCD_4',
             'SPECIAL_CCD_5',
             'TIME',
             'MONITOR',
             'PIXELSIZE',
             'TIMESTAMP',
             'GRIDPATTERN',
             'STARTANGLESINDEG',
             'ENDANGLESINDEG',
             'GONIOMODEL_1',
             'GONIOMODEL_2',
             'WAVELENGTH',
             'MONOCHROMATOR',
             'ABSTORUN',
             'HISTORY',
             'ESPERANTO_FORMAT'])
            self.assertEqual(set(obj.header.keys()), expected_keys)


def suite():
    loadTests = unittest.defaultTestLoader.loadTestsFromTestCase
    testsuite = unittest.TestSuite()
    testsuite.addTest(loadTests(TestEsperanto))
    return testsuite


if __name__ == '__main__':
    runner = unittest.TextTestRunner()
    runner.run(suite())