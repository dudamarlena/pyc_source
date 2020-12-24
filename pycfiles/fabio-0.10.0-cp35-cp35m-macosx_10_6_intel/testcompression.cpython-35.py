# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/kieffer/workspace/fabio/build/lib.macosx-10.6-intel-3.5/fabio/test/testcompression.py
# Compiled at: 2019-03-04 08:01:16
# Size of source mod 2**32: 5885 bytes
from __future__ import with_statement, print_function, division
__authors__ = [
 'Jérôme Kieffer']
__contact__ = 'Jerome.Kieffer@esrf.fr'
__license__ = 'MIT'
__copyright__ = '2011-2016 ESRF'
__date__ = '29/10/2018'
import unittest, numpy, logging
logger = logging.getLogger(__name__)
from fabio import compression

class TestByteOffset(unittest.TestCase):
    __doc__ = '\n    test the byte offset compression and decompression\n    '

    def setUp(self):
        self.ds = numpy.array([0, 1, 2, 127, 0, 1, 2, 128, 0, 1, 2, 32767, 0, 1, 2, 32768, 0, 1, 2, 2147483647, 0, 1, 2, 2147483648, 0, 1, 2, 128, 129, 130, 32767, 32768, 128, 129, 130, 32768, 2147483647, 2147483648])
        self.ref = b'\x00\x01\x01}\x81\x01\x01~\x80\x80\xff\x01\x01\x80\xfd\x7f\x80\x01\x80\x01\x01\x80\xfe\x7f\x80\x00\x80\x00\x80\xff\xff\x01\x01\x80\x00\x80\xfd\xff\xff\x7f\x80\x00\x80\x01\x00\x00\x80\x01\x01\x80\x00\x80\xfe\xff\xff\x7f\x80\x00\x80\x00\x00\x00\x80\x00\x00\x00\x80\xff\xff\xff\xff\x01\x01~\x01\x01\x80}\x7f\x01\x80\x80\x80\x01\x01\x80~\x7f\x80\x00\x80\xff\x7f\xff\x7f\x01'

    def tearDown(self):
        unittest.TestCase.tearDown(self)
        self.ds = self.ref = None

    def testComp(self):
        """
        """
        ds = numpy.array([0, 128])
        ref = b'\x00\x80\x80\x00'
        self.assertEqual(ref, compression.compByteOffset_numpy(ds), 'test +128')
        ds = numpy.array([0, -128])
        ref = b'\x00\x80\x80\xff'
        self.assertEqual(ref, compression.compByteOffset_numpy(ds), 'test -128')
        ds = numpy.array([10, -128])
        ref = b'\n\x80v\xff'
        self.assertEqual(ref, compression.compByteOffset_numpy(ds), 'test +10 -128')
        self.assertEqual(self.ref, compression.compByteOffset_numpy(self.ds), 'test larger')
        ds = numpy.array([0, 128], dtype='int32')
        ref = b'\x00\x80\x80\x00'
        self.assertEqual(ref, compression.compByteOffset_cython(ds), 'test +128')
        ds = numpy.array([0, -128], dtype='int32')
        ref = b'\x00\x80\x80\xff'
        self.assertEqual(ref, compression.compByteOffset_cython(ds), 'test -128')
        ds = numpy.array([10, -128], dtype='int32')
        ref = b'\n\x80v\xff'
        self.assertEqual(ref, compression.compByteOffset_cython(ds), 'test +10 -128')
        self.assertEqual(self.ref, compression.compByteOffset_cython(self.ds), 'test larger')
        ds = numpy.array([0, 128], dtype='int64')
        ref = b'\x00\x80\x80\x00'
        self.assertEqual(ref, compression.compByteOffset_cython(ds), 'test +128')
        ds = numpy.array([0, -128], dtype='int64')
        ref = b'\x00\x80\x80\xff'
        self.assertEqual(ref, compression.compByteOffset_cython(ds), 'test -128')
        ds = numpy.array([10, -128], dtype='int64')
        ref = b'\n\x80v\xff'
        self.assertEqual(ref, compression.compByteOffset_cython(ds), 'test +10 -128')
        self.assertEqual(self.ref, compression.compByteOffset_cython(self.ds), 'test larger')

    def testSC(self):
        """test that datasets are unchanged after various compression/decompressions"""
        obt_np = compression.decByteOffset_numpy(compression.compByteOffset_numpy(self.ds))
        self.assertEqual(abs(self.ds - obt_np).max(), 0.0, 'numpy-numpy algo')
        obt_cy = compression.decByteOffset_cython(compression.compByteOffset_numpy(self.ds))
        self.assertEqual(abs(self.ds - obt_cy).max(), 0.0, 'cython-numpy algo')
        obt_cy2 = compression.decByteOffset_cython(compression.compByteOffset_numpy(self.ds), self.ds.size)
        self.assertEqual(abs(self.ds - obt_cy2).max(), 0.0, 'cython2-numpy algo_orig')
        obt_np = compression.decByteOffset_numpy(compression.compByteOffset_cython(self.ds))
        self.assertEqual(abs(self.ds - obt_np).max(), 0.0, 'numpy-numpy algo')
        obt_cy = compression.decByteOffset_cython(compression.compByteOffset_cython(self.ds))
        self.assertEqual(abs(self.ds - obt_cy).max(), 0.0, 'cython-numpy algo')
        obt_cy2 = compression.decByteOffset_cython(compression.compByteOffset_cython(self.ds), self.ds.size)
        self.assertEqual(abs(self.ds - obt_cy2).max(), 0.0, 'cython2-numpy algo_orig')


def suite():
    loadTests = unittest.defaultTestLoader.loadTestsFromTestCase
    testsuite = unittest.TestSuite()
    testsuite.addTest(loadTests(TestByteOffset))
    return testsuite


if __name__ == '__main__':
    runner = unittest.TextTestRunner()
    runner.run(suite())