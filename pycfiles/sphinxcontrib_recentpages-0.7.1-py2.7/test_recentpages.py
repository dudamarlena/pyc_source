# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.4-x86_64/egg/tests/test_recentpages.py
# Compiled at: 2012-12-17 09:52:34
import unittest, os, time, sphinxcontrib.recentpages as target
from util import *

class TestRecentpages(unittest.TestCase):

    def setUp(self):
        atime = mtime = time.mktime((2012, 11, 1, 1, 1, 1, 0, 0, -1))
        os.utime(test_root / 'file2.rst', (atime, mtime))
        atime = mtime = time.mktime((2012, 11, 2, 1, 1, 1, 0, 0, -1))
        os.utime(test_root / 'file1.rst', (atime, mtime))
        atime = mtime = time.mktime((2012, 11, 3, 1, 1, 1, 0, 0, -1))
        os.utime(test_root / 'index.rst', (atime, mtime))
        atime = mtime = time.mktime((2012, 11, 4, 1, 1, 1, 0, 0, -1))
        os.utime(test_root / 'file3.rst', (atime, mtime))

    def tearDown(self):
        (test_root / '_build').rmtree(True)

    def test_get_file_list_ordered_by_mtime(self):
        app = TestApp(buildername='html')
        app.build(force_all=True, filenames=[])
        env = app.builder.env
        res = target.get_file_list_ordered_by_mtime(env)
        self.assertEqual([
         ('file3', 1351958461.0, 'file 3'),
         ('index', 1351872061.0, "Welcome to sphinxcontrib-recentpages's documentation!"),
         ('file1', 1351785661.0, 'file 1'),
         ('file2', 1351699261.0, 'file 2')], res)


if __name__ == '__main__':
    unittest.main()