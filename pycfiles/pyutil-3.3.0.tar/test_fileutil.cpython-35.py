# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/user/code/pyutil/pyutil/test/current/test_fileutil.py
# Compiled at: 2019-06-26 11:58:00
# Size of source mod 2**32: 1078 bytes
import unittest, os
from pyutil import fileutil

class FileUtil(unittest.TestCase):

    def mkdir(self, basedir, path, mode=511):
        fn = os.path.join(basedir, path)
        fileutil.make_dirs(fn, mode)

    def touch(self, basedir, path, mode=None, data='touch\n'):
        fn = os.path.join(basedir, path)
        f = open(fn, 'w')
        f.write(data)
        f.close()
        if mode is not None:
            os.chmod(fn, mode)

    def test_du(self):
        basedir = 'util/FileUtil/test_du'
        fileutil.make_dirs(basedir)
        d = os.path.join(basedir, 'space-consuming')
        self.mkdir(d, 'a/b')
        self.touch(d, 'a/b/1.txt', data='aaaaaaaaaa')
        self.touch(d, 'a/b/2.txt', data='bbbbbbbbbbb')
        self.mkdir(d, 'a/c')
        self.touch(d, 'a/c/1.txt', data='cccccccccccc')
        self.touch(d, 'a/c/2.txt', data='ddddddddddddd')
        used = fileutil.du(basedir)
        self.assertEqual(46, used)