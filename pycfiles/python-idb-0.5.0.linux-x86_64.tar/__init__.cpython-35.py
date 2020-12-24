# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/user/env/lib/python3.5/site-packages/idb/__init__.py
# Compiled at: 2017-07-12 12:52:31
# Size of source mod 2**32: 775 bytes
import contextlib, six
from idb.idapython import IDAPython
if six.PY2:

    def memview(buf):
        return buf


else:

    def memview(buf):
        return memoryview(buf)


@contextlib.contextmanager
def from_file(path):
    import idb.fileformat
    with open(path, 'rb') as (f):
        buf = memview(f.read())
        db = idb.fileformat.IDB(buf)
        db.vsParse(buf)
        yield db


def from_buffer(buf):
    import idb.fileformat
    buf = memview(buf)
    db = idb.fileformat.IDB(buf)
    db.vsParse(buf)
    return db