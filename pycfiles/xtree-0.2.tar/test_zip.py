# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/dktrkranz/Laboratorio/Vari/xtree/tests/test_zip.py
# Compiled at: 2012-12-15 07:39:08
import unittest
from common import Common
from XTree import Zip

class ZipFile(unittest.TestCase, Common):

    def test_zip1(self):
        files = ('zip1.flat/bar|1|a', 'zip1.flat/bar|22|bb', 'zip1.flat/bar|333|ccc',
                 'zip1.flat/bar|foo1', 'zip1.flat/bar|foo2', 'zip1.flat/foo|bar1',
                 'zip1.flat/foo|bar2')
        with self.Silence():
            z = Zip.Zip('tests/zip/zip1.zip')
            processed = self.list_files(z.flat_dir)
        self.assertEqual(set(files), processed)

    def test_zip2(self):
        files = ('tests/zip/zip2.flat/bar|foo1', 'tests/zip/zip2.flat/bar|foo2', 'tests/zip/zip2.flat/baz',
                 'tests/zip/zip2.flat/foo|bar1', 'tests/zip/zip2.flat/foo|bar2')
        with self.Silence():
            z = Zip.Zip('tests/zip/zip2.zip')
            processed = self.list_files(z.flat_dir)
        self.assertEqual(set(files), processed)

    def test_zip_separator(self):
        files = ('zip1.flat/bar#1#a', 'zip1.flat/bar#22#bb', 'zip1.flat/bar#333#ccc',
                 'zip1.flat/bar#foo1', 'zip1.flat/bar#foo2', 'zip1.flat/foo#bar1',
                 'zip1.flat/foo#bar2')
        with self.Silence():
            z = Zip.Zip('tests/zip/zip1.zip', '#')
            processed = self.list_files(z.flat_dir)
        self.assertEqual(set(files), processed)

    def test_zip_no_separator(self):
        files = ('zip1.flat/a', 'zip1.flat/bar1', 'zip1.flat/bar2', 'zip1.flat/bb',
                 'zip1.flat/ccc', 'zip1.flat/foo1', 'zip1.flat/foo2')
        with self.Silence():
            z = Zip.Zip('tests/zip/zip1.zip', False)
            processed = self.list_files(z.flat_dir)
        self.assertEqual(set(files), processed)

    def test_zip_no_separator_exit(self):
        try:
            with self.Silence():
                z = Zip.Zip('tests/zip/zip3.zip', False)
                processed = self.list_files(z.flat_dir)
        except SystemExit:
            pass
        else:
            self.fail('SystemExit exception expected')

    def test_zip_bad_separator(self):
        try:
            with self.Silence():
                z = Zip.Zip('tests/zip/zip4.zip')
                processed = self.list_files(z.flat_dir)
        except SystemExit:
            pass
        else:
            self.fail('SystemExit exception expected')

    def test_zip_is_zip(self):
        try:
            with self.Silence():
                z = Zip.Zip('tests/tar/gzip1.tar.gz')
                processed = self.list_files(z.flat_dir)
        except SystemExit:
            pass
        else:
            self.fail('SystemExit exception expected')


if __name__ == '__main__':
    unittest.main()