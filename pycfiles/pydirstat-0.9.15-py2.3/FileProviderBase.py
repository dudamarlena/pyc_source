# uncompyle6 version 3.7.4
# Python bytecode 2.3 (62011)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\dirstat\FileProviderBase.py
# Compiled at: 2006-10-06 11:17:02
import posixpath

class StatInfoBase(object):
    __module__ = __name__

    def __init__(self, url):
        self._url = url

    def st_dev(self):
        return 0

    def st_mode(self):
        return 0

    def st_nlink(self):
        return 0

    def st_mtime(self):
        return 0

    def st_size(self):
        return 0

    def st_blocks(self):
        return 0

    def st_dev(self):
        return 0

    def is_dir(self):
        return False

    def is_reg(self):
        return False

    def is_lnk(self):
        return False

    def is_blk(self):
        return False

    def is_chr(self):
        return False

    def is_fifo(self):
        return False

    def is_sock(self):
        return False


class FileProviderBase(object):
    r"""The base of all classes of FileProvider.

    This class does quite nothing. It's purpose is to provide basic
    default implementation for a FileProvider. posixpath
    (/ style path) is used even on windows (\ style path).

    It can't walk."""
    __module__ = __name__
    supports_unicode_filenames = False

    def __init__(self, url):
        self._url = url

    def walk(self):
        return []

    def split(self, path):
        return posixpath.split(path)

    def join(self, *args):
        return posixpath.join(*args)

    def abspath(self, path):
        return path

    def stat(self, url):
        return StatInfoBase(file)

    def get_clean_name(self, file):
        return file