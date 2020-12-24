# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\entransit\common\blob.py
# Compiled at: 2008-03-07 16:10:40
"""
$Id: __init__.py 732 2005-01-21 19:43:40Z sidnei $
"""
import os

class Blob(object):
    """To access the underlying file, call Blob.open(dir) where 'dir' is
    the directory where the tarfile was extracted to.
    """
    __module__ = __name__
    __slots__ = ('name', )

    def __init__(self, name):
        self.name = name

    def open(self, path):
        return open(os.path.join(path, self.name), mode='rb')