# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.3-fat/egg/schevo/mt/plugin.py
# Compiled at: 2007-03-21 14:34:39
"""Multi-threading support for Schevo.

For copyright, license, and warranty, see bottom of file.
"""
from schevo.database import dummy_lock
from schevo.mt import mrow

def install(db):
    """Install a database locker in `db` if one does not yet exist."""
    if db.read_lock is dummy_lock:
        Plugin(db)


class Plugin(object):
    """A plugin giving a Schevo database a multiple-reader, one-writer
    locking mechanism.
    
    Usage::

      from schevo.database import open
      db = open(...)
      from schevomt import lockable
      lockable.install(db)
      lock = db.read_lock()         # Or .write_lock()
      try:
          # Do stuff here.
          pass
      finally:
          lock.release()
    """
    __module__ = __name__

    def __init__(self, db):
        self.db = db
        rwlock = mrow.RWLock()
        reader = rwlock.reader
        writer = rwlock.writer
        db.read_lock = reader
        db.write_lock = writer

        def db_reader(fn):

            def inner(*args, **kw):
                lock = reader()
                try:
                    return fn(*args, **kw)
                finally:
                    lock.release()

            inner.__name__ = fn.__name__
            inner.__doc__ = fn.__doc__
            inner.__dict__.update(fn.__dict__)
            return inner

        def db_writer(fn):

            def inner(*args, **kw):
                lock = reader()
                try:
                    return fn(*args, **kw)
                finally:
                    lock.release()

            inner.__name__ = fn.__name__
            inner.__doc__ = fn.__doc__
            inner.__dict__.update(fn.__dict__)
            return inner

        db.db_reader = db_reader
        db.db_writer = db_writer
        self._execute = db.execute

    def close(self):
        pass

    def execute(self, transaction):
        db = self.db
        lock = db.write_lock()
        try:
            return self._execute(transaction)
        finally:
            lock.release()