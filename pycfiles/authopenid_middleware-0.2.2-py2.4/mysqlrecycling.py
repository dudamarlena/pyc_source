# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/authopenid_middleware/mysqlrecycling.py
# Compiled at: 2009-10-29 02:02:05
import MySQLdb, time

class MySQLRecyclingConnection:
    __module__ = __name__

    def __init__(self, **kwargs):
        self.connection = MySQLdb.connect(**kwargs)
        self.args = kwargs
        self.start_time = time.time()

    def _check_connection(self):
        if time.time() - self.start_time > 3600:
            self.connection.close()
            self.connection = MySQLdb.connect(**self.args)
            self.start_time = time.time()

    def cursor(self):
        self._check_connection()
        return self.connection.cursor()

    def dbapi():
        return MySQLdb

    def close():
        return self.connection.close()

    def commit(self):
        self._check_connection()
        self.connection.commit()

    def rollback(self):
        self._check_connection()
        self.connection.rollback()