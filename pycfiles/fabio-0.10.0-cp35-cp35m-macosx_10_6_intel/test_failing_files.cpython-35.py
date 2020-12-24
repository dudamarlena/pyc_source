# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/kieffer/workspace/fabio/build/lib.macosx-10.6-intel-3.5/fabio/test/test_failing_files.py
# Compiled at: 2020-04-03 09:02:03
# Size of source mod 2**32: 3864 bytes
"""Test failing files
"""
from __future__ import print_function, with_statement, division, absolute_import
import unittest, os, io, fabio, shutil
from .utilstest import UtilsTest

class TestFailingFiles(unittest.TestCase):
    __doc__ = 'Test failing files'

    @classmethod
    def setUpClass(cls):
        cls.tmp_directory = os.path.join(UtilsTest.tempdir, cls.__name__)
        os.makedirs(cls.tmp_directory)
        cls.createResources(cls.tmp_directory)

    @classmethod
    def createResources(cls, directory):
        cls.txt_filename = os.path.join(directory, 'test.txt')
        with io.open(cls.txt_filename, 'w+t') as (f):
            f.write('Kikoo')
        cls.bad_edf_filename = os.path.join(directory, 'bad_edf.edf')
        with io.open(cls.bad_edf_filename, 'w+b') as (f):
            f.write(b'\r{')
            f.write(b'\x00\xff\x99' * 10)
        cls.bad_edf2_filename = os.path.join(directory, 'bad_edf2.edf')
        with io.open(cls.bad_edf2_filename, 'w+b') as (f):
            f.write(b'\n{\n\n}\n')
            f.write(b'\xff\x00\x99' * 10)
        cls.bad_msk_filename = os.path.join(directory, 'bad_msk.msk')
        with io.open(cls.bad_msk_filename, 'w+b') as (f):
            f.write(b'M\x00\x00\x00A\x00\x00\x00S\x00\x00\x00K\x00\x00\x00')
            f.write(b'\x00\xff\x99' * 10)
        cls.bad_dm3_filename = os.path.join(directory, 'bad_dm3.dm3')
        with io.open(cls.bad_dm3_filename, 'w+b') as (f):
            f.write(b'\x00\x00\x00\x03')
            f.write(b'\x00\xff\x99' * 10)
        cls.bad_npy_filename = os.path.join(directory, 'bad_numpy.npy')
        with io.open(cls.bad_npy_filename, 'w+b') as (f):
            f.write(b'\x93NUMPY')
            f.write(b'\x00\xff\x99' * 10)
        cls.missing_filename = os.path.join(directory, 'test.missing')

    @classmethod
    def tearDownClass(cls):
        shutil.rmtree(cls.tmp_directory)

    def test_missing_file(self):
        self.assertRaises(IOError, fabio.open, self.missing_filename)

    def test_wrong_format(self):
        self.assertRaises(IOError, fabio.open, self.txt_filename)

    def test_wrong_edf(self):
        self.assertRaises(IOError, fabio.open, self.bad_edf_filename)

    def test_wrong_edf2(self):
        self.assertRaises(IOError, fabio.open, self.bad_edf_filename)

    def test_wrong_msk(self):
        self.assertRaises(ValueError, fabio.open, self.bad_msk_filename)

    def test_wrong_dm3(self):
        self.assertRaises(ValueError, fabio.open, self.bad_dm3_filename)

    def test_wrong_numpy(self):
        self.assertRaises(ValueError, fabio.open, self.bad_npy_filename)


def suite():
    loadTests = unittest.defaultTestLoader.loadTestsFromTestCase
    testsuite = unittest.TestSuite()
    testsuite.addTest(loadTests(TestFailingFiles))
    return testsuite


if __name__ == '__main__':
    runner = unittest.TextTestRunner()
    runner.run(suite())