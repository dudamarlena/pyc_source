# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.8-x86_64/egg/filedb/filedb.py
# Compiled at: 2014-02-04 10:48:18
from errno import ENOENT
from stat import S_IFDIR, S_IFREG
import time, json
from fuse import FuseOSError, Operations

class FileDB(Operations):

    def __init__(self, db, collection):
        self.db = db
        self.collection = self.db[collection]

    def dump_db(self):
        collection = []
        keys = {'_id': 1, 
           'username': 1, 
           'apikey': 1, 
           'password': 1}
        for thing in self.collection.find({}, keys):
            thing['_id'] = str(thing['_id'])
            collection.append(thing)

        return json.dumps(collection) + '\n'

    def getattr(self, path, fh=None):
        if path == '/':
            st = dict(st_mode=S_IFDIR | 493, st_nlink=2)
        elif path == '/db':
            data = self.dump_db()
            size = len(data)
            st = dict(st_mode=S_IFREG | 292, st_size=size)
        else:
            raise FuseOSError(ENOENT)
        st['st_ctime'] = st['st_mtime'] = st['st_atime'] = time.time()
        return st

    def read(self, path, size, offset, fh):
        if path == '/db':
            data = self.dump_db()
            return data[offset:offset + size]
        raise RuntimeError('unexpected path: %r' % path)

    def readdir(self, path, fh):
        return [
         '.', '..', 'db']

    access = None
    flush = None
    getxattr = None
    listxattr = None
    open = None
    opendir = None
    release = None
    releasedir = None
    statfs = None


if __name__ == '__main__':
    pass