# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/kieffer/workspace/fabio/build/lib.macosx-10.6-intel-3.5/fabio/test/codecs/test_hdf5image.py
# Compiled at: 2020-04-03 09:02:03
# Size of source mod 2**32: 2936 bytes
"""Test Eiger images
"""
from __future__ import print_function, with_statement, division, absolute_import
import unittest, os, logging
logger = logging.getLogger(__name__)
from fabio.fabioutils import exists
from fabio.openimage import openimage
from fabio.hdf5image import Hdf5Image, h5py
from ..utilstest import UtilsTest

def make_hdf5(name, shape=(50, 99, 101)):
    if h5py is None:
        raise unittest.SkipTest('h5py is not available')
    with h5py.File(name, mode='w') as (h):
        e = h.require_group('entry')
        if len(shape) == 2:
            e.require_dataset('data', shape, compression='gzip', compression_opts=9, dtype='float32')
        elif len(shape) == 3:
            e.require_dataset('data', shape, chunks=(1, ) + shape[1:], compression='gzip', compression_opts=9, dtype='float32')
    return name + '::entry/data'


class TestHdf5(unittest.TestCase):
    __doc__ = 'basic test'

    @classmethod
    def setUpClass(cls):
        super(TestHdf5, cls).setUpClass()
        cls.fn2 = os.path.join(UtilsTest.tempdir, 'eiger2d.h5')
        cls.fn2 = make_hdf5(cls.fn2, (99, 101))
        cls.fn3 = os.path.join(UtilsTest.tempdir, 'eiger3d.h5')
        cls.fn3 = make_hdf5(cls.fn3, (50, 99, 101))

    @classmethod
    def tearDownClass(cls):
        super(TestHdf5, cls).tearDownClass()
        if exists(cls.fn3):
            os.unlink(cls.fn3.split('::')[0])
        if exists(cls.fn2):
            os.unlink(cls.fn2.split('::')[0])

    def test_read(self):
        """ check we can read images from Eiger"""
        e = Hdf5Image()
        e.read(self.fn2)
        self.assertEqual(e.shape, (99, 101))
        self.assertEqual(e.nframes, 1, 'nframes OK')
        self.assertEqual(e.bpp, 4, 'nframes OK')
        e = Hdf5Image()
        e.read(self.fn3)
        self.assertEqual(e.shape, (99, 101))
        self.assertEqual(e.nframes, 50, 'nframes OK')
        self.assertEqual(e.bpp, 4, 'nframes OK')

    def test_open(self):
        """ check we can read images from Eiger"""
        e = openimage(self.fn2)
        self.assertEqual(e.shape, (99, 101))
        self.assertEqual(e.nframes, 1, 'nframes OK')
        self.assertEqual(e.bpp, 4, 'nframes OK')
        e = openimage(self.fn3)
        self.assertEqual(e.shape, (99, 101))
        self.assertEqual(e.nframes, 50, 'nframes OK')
        self.assertEqual(e.bpp, 4, 'nframes OK')


def suite():
    loadTests = unittest.defaultTestLoader.loadTestsFromTestCase
    testsuite = unittest.TestSuite()
    testsuite.addTest(loadTests(TestHdf5))
    return testsuite


if __name__ == '__main__':
    runner = unittest.TextTestRunner()
    runner.run(suite())