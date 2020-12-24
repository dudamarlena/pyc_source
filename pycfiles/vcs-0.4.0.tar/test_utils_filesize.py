# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/lukasz/develop/workspace/.pythonpath/vcs/tests/test_utils_filesize.py
# Compiled at: 2013-04-27 15:11:11
from __future__ import with_statement
from vcs.utils.filesize import filesizeformat
from vcs.utils.compat import unittest

class TestFilesizeformat(unittest.TestCase):

    def test_bytes(self):
        self.assertEqual(filesizeformat(10), '10 B')

    def test_kilobytes(self):
        self.assertEqual(filesizeformat(2048), '2 KB')

    def test_megabytes(self):
        self.assertEqual(filesizeformat(2411724.8), '2.3 MB')

    def test_gigabytes(self):
        self.assertEqual(filesizeformat(13872744366.08), '12.92 GB')

    def test_that_function_respects_sep_paramtere(self):
        self.assertEqual(filesizeformat(1, ''), '1B')


if __name__ == '__main__':
    unittest.main()