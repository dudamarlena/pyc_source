# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python2.7/dist-packages/panipuri/backends/FilesystemDataframeCache.py
# Compiled at: 2014-04-28 07:28:51
from CacheBackend import CacheBackend
import os, errno

class FilesystemDataframeCache(CacheBackend):
    """
    A backend for caching dataframes *only*. No other types will work.

    Pandas must be available if you use this backend.
    """
    import pandas

    def __init__(self, filename):
        self._datadir = filename
        try:
            os.makedirs(self._datadir)
        except OSError as exc:
            if exc.errno == errno.EEXIST and os.path.isdir(self._datadir):
                pass
            else:
                raise

    def _path(self, key):
        return os.path.join(self._datadir, key)

    def put(self, key, val):
        if type(val) == self.pandas.DataFrame:
            val.to_csv(self._path(key))
        else:
            raise ValueError('This cache can only handle dataframes. You passed in a ' + str(type(val)))

    def get(self, key):
        try:
            df = self.pandas.read_csv(self._path(key))
            return df
        except IOError as e:
            raise KeyError('key ' + key + ' not found')