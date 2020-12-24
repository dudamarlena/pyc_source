# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/dktrkranz/Laboratorio/Vari/xtree/tests/test_tar.py
# Compiled at: 2012-12-15 07:57:47
import unittest
from common import Common
from XTree import Tar

class GzipFile(unittest.TestCase, Common):

    def test_tar1(self):
        files = ('gzip1.flat/bar|1|a', 'gzip1.flat/bar|22|bb', 'gzip1.flat/bar|333|ccc',
                 'gzip1.flat/bar|foo1', 'gzip1.flat/bar|foo2', 'gzip1.flat/foo|bar1',
                 'gzip1.flat/foo|bar2')
        with self.Silence():
            g = Tar.Tar('tests/tar/gzip1.tar.gz')
            processed = self.list_files(g.flat_dir)
        self.assertEqual(set(files), processed)

    def test_tar2(self):
        files = ('tests/tar/gzip2.tar.flat/bar|foo1', 'tests/tar/gzip2.tar.flat/bar|foo2',
                 'tests/tar/gzip2.tar.flat/baz', 'tests/tar/gzip2.tar.flat/foo|bar1',
                 'tests/tar/gzip2.tar.flat/foo|bar2')
        with self.Silence():
            g = Tar.Tar('tests/tar/gzip2.tar.gz')
            processed = self.list_files(g.flat_dir)
        self.assertEqual(set(files), processed)

    def test_tar_separator(self):
        files = ('gzip1.flat/bar#1#a', 'gzip1.flat/bar#22#bb', 'gzip1.flat/bar#333#ccc',
                 'gzip1.flat/bar#foo1', 'gzip1.flat/bar#foo2', 'gzip1.flat/foo#bar1',
                 'gzip1.flat/foo#bar2')
        with self.Silence():
            g = Tar.Tar('tests/tar/gzip1.tar.gz', '#')
            processed = self.list_files(g.flat_dir)
        self.assertEqual(set(files), processed)

    def test_tar_no_separator(self):
        files = ('gzip1.flat/a', 'gzip1.flat/bar1', 'gzip1.flat/bar2', 'gzip1.flat/bb',
                 'gzip1.flat/ccc', 'gzip1.flat/foo1', 'gzip1.flat/foo2')
        with self.Silence():
            g = Tar.Tar('tests/tar/gzip1.tar.gz', False)
            processed = self.list_files(g.flat_dir)
        self.assertEqual(set(files), processed)

    def test_tar_no_separator_exit(self):
        try:
            with self.Silence():
                g = Tar.Tar('tests/tar/gzip3.tar.gz', False)
                processed = self.list_files(g.flat_dir)
        except SystemExit:
            pass
        else:
            self.fail('SystemExit exception expected')

    def test_tar_bad_separator(self):
        try:
            with self.Silence():
                g = Tar.Tar('tests/tar/gzip4.tar.gz')
                processed = self.list_files(g.flat_dir)
        except SystemExit:
            pass
        else:
            self.fail('SystemExit exception expected')

    def test_tar_is_gzip(self):
        try:
            with self.Silence():
                g = Tar.Tar('tests/zip/zip1.zip')
                processed = self.list_files(g.flat_dir)
        except SystemExit:
            pass
        else:
            self.fail('SystemExit exception expected')


class Bzip2File(unittest.TestCase, Common):

    def test_tar1(self):
        files = ('bzip1.flat/bar|1|a', 'bzip1.flat/bar|22|bb', 'bzip1.flat/bar|333|ccc',
                 'bzip1.flat/bar|foo1', 'bzip1.flat/bar|foo2', 'bzip1.flat/foo|bar1',
                 'bzip1.flat/foo|bar2')
        with self.Silence():
            b = Tar.Tar('tests/tar/bzip1.tar.bz2')
            processed = self.list_files(b.flat_dir)
        self.assertEqual(set(files), processed)

    def test_tar2(self):
        files = ('tests/tar/bzip2.tar.flat/bar|foo1', 'tests/tar/bzip2.tar.flat/bar|foo2',
                 'tests/tar/bzip2.tar.flat/baz', 'tests/tar/bzip2.tar.flat/foo|bar1',
                 'tests/tar/bzip2.tar.flat/foo|bar2')
        with self.Silence():
            b = Tar.Tar('tests/tar/bzip2.tar.bz2')
            processed = self.list_files(b.flat_dir)
        self.assertEqual(set(files), processed)

    def test_tar_separator(self):
        files = ('bzip1.flat/bar#1#a', 'bzip1.flat/bar#22#bb', 'bzip1.flat/bar#333#ccc',
                 'bzip1.flat/bar#foo1', 'bzip1.flat/bar#foo2', 'bzip1.flat/foo#bar1',
                 'bzip1.flat/foo#bar2')
        with self.Silence():
            b = Tar.Tar('tests/tar/bzip1.tar.bz2', '#')
            processed = self.list_files(b.flat_dir)
        self.assertEqual(set(files), processed)

    def test_tar_no_separator(self):
        files = ('bzip1.flat/a', 'bzip1.flat/bar1', 'bzip1.flat/bar2', 'bzip1.flat/bb',
                 'bzip1.flat/ccc', 'bzip1.flat/foo1', 'bzip1.flat/foo2')
        with self.Silence():
            b = Tar.Tar('tests/tar/bzip1.tar.bz2', False)
            processed = self.list_files(b.flat_dir)
        self.assertEqual(set(files), processed)

    def test_tar_no_separator_exit(self):
        try:
            with self.Silence():
                b = Tar.Tar('tests/tar/bzip3.tar.bz2', False)
                processed = self.list_files(b.flat_dir)
        except SystemExit:
            pass
        else:
            self.fail('SystemExit exception expected')

    def test_tar_bad_separator(self):
        try:
            with self.Silence():
                b = Tar.Tar('tests/tar/bzip4.tar.bz2')
                processed = self.list_files(b.flat_dir)
        except SystemExit:
            pass
        else:
            self.fail('SystemExit exception expected')

    def test_tar_is_bzip2(self):
        try:
            with self.Silence():
                b = Tar.Tar('tests/zip/zip1.zip')
                processed = self.list_files(b.flat_dir)
        except SystemExit:
            pass
        else:
            self.fail('SystemExit exception expected')


if __name__ == '__main__':
    unittest.main()