# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python2.7/dist-packages/panipuri/backends/SQLiteCache.py
# Compiled at: 2014-04-27 07:42:33
from CacheBackend import CacheBackend
import sqlite3, pickle

class SQLiteCache(CacheBackend):

    def __init__(self, filename, tablename):
        self._db = sqlite3.connect(filename)
        self._tablename = tablename
        self._create_table()

    def _create_table(self):
        try:
            c = self._db.cursor()
            c.execute('CREATE TABLE ' + self._tablename + ' (\n            key TEXT PRIMARY KEY,\n            value TEXT\n            );\n            ')
            self._db.commit()
            c.close()
        except sqlite3.OperationalError as e:
            pass

    def put(self, key, val):
        pickled_val = pickle.dumps(val)
        c = self._db.cursor()
        c.execute('INSERT INTO ' + self._tablename + ' (key, value) VALUES (?,?);', (key, pickled_val))
        self._db.commit()

    def get(self, key):
        c = self._db.cursor()
        c.execute('SELECT value FROM ' + self._tablename + ' WHERE key=?;', (key,))
        pickled_value = c.fetchone()
        if pickled_value is None:
            raise KeyError('key ' + key + ' not found')
        c.close()
        return pickle.loads(pickled_value[0])