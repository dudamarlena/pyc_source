# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/kieffer/workspace/fabio/build/lib.macosx-10.6-intel-3.5/fabio/test/codecs/test_xsdimage.py
# Compiled at: 2020-04-03 09:02:03
# Size of source mod 2**32: 3677 bytes
"""
# Unit tests

# builds on stuff from ImageD11.test.testpeaksearch
"""
from __future__ import print_function, with_statement, division, absolute_import
import unittest, numpy, logging
logger = logging.getLogger(__name__)
import fabio.xsdimage
from ..utilstest import UtilsTest
TESTIMAGES = 'XSDataImage.xml     512 512        86 61204     511.63    667.15\n                XSDataImageInv.xml  512 512  -0.2814 0.22705039 2.81e-08  0.010'

class TestXSD(unittest.TestCase):

    def setUp(self):
        if fabio.xsdimage.etree is None:
            self.skipTest('etree is not available')
        self.fn = {}
        for i in ['XSDataImage.edf', 'XSDataImage.xml', 'XSDataImageInv.xml']:
            self.fn[i] = UtilsTest.getimage(i + '.bz2')[:-4]

    def test_read(self):
        """Test reading of XSD images"""
        for line in TESTIMAGES.split('\n'):
            vals = line.split()
            name = vals[0]
            dim1, dim2 = [int(x) for x in vals[1:3]]
            shape = (dim2, dim1)
            mini, maxi, mean, stddev = [float(x) for x in vals[3:]]
            obj = fabio.xsdimage.xsdimage()
            obj.read(self.fn[name])
            self.assertAlmostEqual(mini, obj.getmin(), 2, 'getmin')
            self.assertAlmostEqual(maxi, obj.getmax(), 2, 'getmax')
            self.assertAlmostEqual(mean, obj.getmean(), 2, 'getmean')
            logger.info('%s %s %s' % (name, stddev, obj.getstddev()))
            self.assertAlmostEqual(stddev, obj.getstddev(), 2, 'getstddev')
            self.assertEqual(shape, obj.shape)

    def test_same(self):
        """ test if an image is the same as the EDF equivalent"""
        xsd = fabio.open(self.fn['XSDataImage.xml'])
        edf = fabio.open(self.fn['XSDataImage.edf'])
        self.assertAlmostEqual(0, abs(xsd.data - edf.data).max(), 1, 'images are the same')

    def test_invert(self):
        """ Tests that 2 matrixes are invert """
        m1 = fabio.open(self.fn['XSDataImage.xml'])
        m2 = fabio.open(self.fn['XSDataImageInv.xml'])
        delta = abs(numpy.matrix(m1.data) * numpy.matrix(m2.data) - numpy.identity(m1.data.shape[0])).max()
        if delta >= 0.001:
            logger.error('Matrices are not invert of each other !!! prod = %s', numpy.matrix(m1.data) * numpy.matrix(m2.data))
        self.assertTrue(delta < 0.001, 'matrices are invert of each other')


def suite():
    loadTests = unittest.defaultTestLoader.loadTestsFromTestCase
    testsuite = unittest.TestSuite()
    testsuite.addTest(loadTests(TestXSD))
    return testsuite


if __name__ == '__main__':
    runner = unittest.TextTestRunner()
    runner.run(suite())