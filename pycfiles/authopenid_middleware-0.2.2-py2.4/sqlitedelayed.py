# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/authopenid_middleware/sqlitedelayed.py
# Compiled at: 2009-10-29 02:02:05
from pysqlite2 import dbapi2 as sqlite
import threading

class SQLiteDelayed(sqlite.Connection):
    """ This class makes separate SQLite connection
    for each thread because SQLite requires that. """
    __module__ = __name__

    def __init__(self, db, **kwargs):
        self.db = db
        self.args = kwargs
        self.connections = {}
        self.available = threading.Condition(threading.RLock())

    def _get_connection(self):
        self.available.acquire()
        try:
            tid = threading._get_ident()
            if tid in self.connections:
                return self.connections[tid]
            else:
                connection = sqlite.connect(self.db, **self.args)
                self.connections[tid] = connection
                return connection
        finally:
            self.available.release()

    def cursor(self):
        connection = self._get_connection()
        return connection.cursor()

    def dbapi():
        return sqlite

    def close():
        self.available.acquire()
        try:
            for connection in self.connections:
                connection.close()

        finally:
            self.available.release()

    def commit(self):
        connection = self._get_connection()
        return connection.commit()

    def rollback(self):
        connection = self._get_connection()
        return connection.rollback()