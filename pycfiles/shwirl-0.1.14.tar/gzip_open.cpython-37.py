# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/vohl/Documents/code/shwirl/shwirl/extern/vispy/ext/gzip_open.py
# Compiled at: 2018-10-01 14:58:41
# Size of source mod 2**32: 614 bytes
from gzip import GzipFile

class gzip_open(GzipFile):

    def __enter__(self):
        if hasattr(GzipFile, '__enter__'):
            return GzipFile.__enter__(self)
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        if hasattr(GzipFile, '__exit__'):
            return GzipFile.__exit__(self, exc_type, exc_value, traceback)
        return self.close()