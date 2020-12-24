# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/kvndb/dbmdb.py
# Compiled at: 2016-11-17 12:05:55
"""anydbm database interface."""
import anydbm

class DbmDatabase(object):
    """A anydbm database"""

    def __init__(self, args):
        self.args = args
        if len(self.args) != 1:
            raise ValueError, 'Expected exactly one argument for the DB.'
        self.path = args[0]
        self.db = anydbm.open(self.path, 'c')

    def get(self, key):
        """returns the value for key."""
        if key in self.db:
            return self.db[key]
        raise KeyError(key)

    def set(self, key, value):
        """sets key to value"""
        self.db[key] = value

    def delete(self, key):
        """deletes the key/value pair for key."""
        try:
            del self.db[key]
        except KeyError:
            pass

    def getkeys(self):
        """returns a list of keys."""
        return self.db.keys()

    def reset(self):
        """resets the database."""
        self.db.close()
        self.db = anydbm.open(self.path, 'n')

    def close(self):
        """this should close the database."""
        self.db.close()