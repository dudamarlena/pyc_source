# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/lib.linux-i686-2.6/m_lib/hash/ZODBhash.py
# Compiled at: 2016-07-25 12:23:18
"""(g)dbm-compatible interface to ZODB"""
import sys
try:
    from ZODB import FileStorage, DB, POSException
except ImportError:
    del sys.modules[__name__]
    raise

__all__ = [
 'error', 'open']
error = POSException.POSError

class ZODBhash:

    def __init__(self, file, flag, mode=438, trans_threshold=1000):
        create = flag == 'n'
        self.read_only = read_only = flag == 'r'
        self._closed = 0
        self.trans_threshold = trans_threshold
        self._transcount = 0
        storage = FileStorage.FileStorage(file, create=create, read_only=read_only)
        db = DB(storage)
        self.conn = conn = db.open()
        self.dbroot = conn.root()

    def __del__(self):
        self.close()

    def keys(self):
        return self.dbroot.keys()

    def __len__(self):
        return len(self.dbroot)

    def has_key(self, key):
        return self.dbroot.has_key(key)

    def get(self, key, default=None):
        if self.dbroot.has_key(key):
            return self[key]
        return default

    def __getitem__(self, key):
        return self.dbroot[key]

    def __setitem__(self, key, value):
        self.dbroot[key] = value
        self._add_tran()

    def __delitem__(self, key):
        del self.dbroot[key]
        self._add_tran()

    def close(self):
        if self._closed:
            return
        if not self.read_only:
            get_transaction().commit()
            self.conn.db().close()
        self.conn.close()
        self._closed = 1

    def _add_tran(self):
        self._transcount = self._transcount + 1
        if self._transcount == self.trans_threshold:
            self._transcount = 0
            get_transaction().commit()


def open(file, flag, mode=438):
    return ZODBhash(file, flag, mode)