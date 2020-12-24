# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/kieffer/workspace/fabio/build/lib.macosx-10.6-intel-3.5/fabio/test/codecs/test_numpyimage.py
# Compiled at: 2020-04-03 09:02:03
# Size of source mod 2**32: 3627 bytes
"""
Test for numpy images.
"""
__author__ = 'Jérôme Kieffer'
__date__ = '07/03/2019'
import os, unittest, numpy, logging
logger = logging.getLogger(__name__)
from fabio.numpyimage import NumpyImage
from fabio.openimage import openimage
from ..utilstest import UtilsTest

class TestNumpy(unittest.TestCase):
    __doc__ = 'basic test'

    def setUp(self):
        """Generate files"""
        self.ary = numpy.random.randint(0, 6500, size=99).reshape(11, 9).astype('uint16')
        self.fn = os.path.join(UtilsTest.tempdir, 'numpy.npy')
        self.fn2 = os.path.join(UtilsTest.tempdir, 'numpy2.npy')
        numpy.save(self.fn, self.ary)

    def tearDown(self):
        unittest.TestCase.tearDown(self)
        for i in (self.fn, self.fn2):
            if os.path.exists(i):
                os.unlink(i)

        self.ary = self.fn = self.fn2 = None

    def test_read(self):
        """ check we can read pnm images"""
        obj = openimage(self.fn)
        self.assertEqual(obj.bytecode, numpy.uint16, msg='bytecode is OK')
        self.assertEqual(obj.shape, (11, 9))
        self.assertTrue(numpy.allclose(obj.data, self.ary), 'data')

    def test_write(self):
        """ check we can write numpy images"""
        ref = NumpyImage(data=self.ary)
        ref.save(self.fn2)
        with openimage(self.fn2) as (obj):
            self.assertEqual(obj.bytecode, numpy.uint16, msg='bytecode is OK')
            self.assertEqual(obj.shape, (11, 9))
            self.assertTrue(numpy.allclose(obj.data, self.ary), 'data')

    def test_multidim(self):
        for shape in ((10,), (10, 15), (10, 15, 20), (10, 15, 20, 25)):
            ary = numpy.random.random(shape).astype('float32')
            numpy.save(self.fn, ary)
            with openimage(self.fn) as (obj):
                self.assertEqual(obj.bytecode, numpy.float32, msg='bytecode is OK')
                self.assertEqual(shape[(-1)], obj.shape[(-1)], 'dim1')
                dim2 = 1 if len(shape) == 1 else shape[(-2)]
                self.assertEqual(dim2, obj.shape[(-2)], 'dim2')
                nframes = 1
                if len(shape) > 2:
                    for i in shape[:-2]:
                        nframes *= i

                    self.assertEqual(nframes, obj.nframes, 'nframes')
            if os.path.exists(self.fn):
                os.unlink(self.fn)


def suite():
    loadTests = unittest.defaultTestLoader.loadTestsFromTestCase
    testsuite = unittest.TestSuite()
    testsuite.addTest(loadTests(TestNumpy))
    return testsuite


if __name__ == '__main__':
    runner = unittest.TextTestRunner()
    runner.run(suite())