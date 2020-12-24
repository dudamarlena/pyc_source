# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/dktrkranz/Laboratorio/Vari/xtree/tests/test_dir.py
# Compiled at: 2012-12-15 07:49:30
import unittest
from common import Common
from XTree import Dir

class ZipFile(unittest.TestCase, Common):

    def test_dir(self):
        files = ('tests/dir/dir1.flat/bar|1|a', 'tests/dir/dir1.flat/bar|22|bb', 'tests/dir/dir1.flat/bar|333|ccc',
                 'tests/dir/dir1.flat/bar|foo1', 'tests/dir/dir1.flat/bar|foo2',
                 'tests/dir/dir1.flat/foo|bar1', 'tests/dir/dir1.flat/foo|bar2')
        with self.Silence():
            d = Dir.Dir('tests/dir/dir1')
            processed = self.list_files(d.flat_dir)
        self.assertEqual(set(files), processed)

    def test_dir_separator(self):
        files = ('tests/dir/dir1.flat/bar#1#a', 'tests/dir/dir1.flat/bar#22#bb', 'tests/dir/dir1.flat/bar#333#ccc',
                 'tests/dir/dir1.flat/bar#foo1', 'tests/dir/dir1.flat/bar#foo2',
                 'tests/dir/dir1.flat/foo#bar1', 'tests/dir/dir1.flat/foo#bar2')
        with self.Silence():
            d = Dir.Dir('tests/dir/dir1', '#')
            processed = self.list_files(d.flat_dir)
        self.assertEqual(set(files), processed)

    def test_dir_no_separator(self):
        files = ('tests/dir/dir1.flat/a', 'tests/dir/dir1.flat/bar1', 'tests/dir/dir1.flat/bar2',
                 'tests/dir/dir1.flat/bb', 'tests/dir/dir1.flat/ccc', 'tests/dir/dir1.flat/foo1',
                 'tests/dir/dir1.flat/foo2')
        with self.Silence():
            d = Dir.Dir('tests/dir/dir1', False)
            processed = self.list_files(d.flat_dir)
        self.assertEqual(set(files), processed)

    def test_dir_no_separator_exit(self):
        try:
            with self.Silence():
                d = Dir.Dir('tests/dir/dir2', False)
                processed = self.list_files(d.flat_dir)
        except SystemExit:
            pass
        else:
            self.fail('SystemExit exception expected')

    def test_dir_bad_separator(self):
        try:
            with self.Silence():
                d = Dir.Dir('tests/dir/dir3')
                processed = self.list_files(d.flat_dir)
        except SystemExit:
            pass
        else:
            self.fail('SystemExit exception expected')

    def test_dir_is_dir(self):
        try:
            with self.Silence():
                d = Dir.Dir('tests/tar/gzip1.tar.gz')
                processed = self.list_files(d.flat_dir)
        except SystemExit:
            pass
        else:
            self.fail('SystemExit exception expected')


if __name__ == '__main__':
    unittest.main()