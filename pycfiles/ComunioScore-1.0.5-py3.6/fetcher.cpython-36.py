# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/ComunioScore/db/fetcher.py
# Compiled at: 2020-04-13 07:58:16
# Size of source mod 2**32: 2315 bytes
import logging
from ComunioScore.db import DBConnector

class DBFetcher(DBConnector):
    __doc__ = ' class DBFetcher to fetch data from database tables\n\n    USAGE:\n            fetcher = DBFetcher()\n            fetcher.connect(host, port, username, password, dbname, minConn=1, maxConn=10)\n            fetcher.many(sql=sql, size=20)\n\n    '

    def __init__(self):
        self.logger = logging.getLogger('ComunioScore')
        self.logger.info('Create class DBFetcher')
        super().__init__()

    def one(self, sql, data=None, autocommit=False):
        """ fetches one row from sql statement

        :param sql: sql statement
        :param data: data for sql statement
        :param autocommit: True or False

        :return: one row from table
        """
        with self.get_cursor(autocommit=autocommit) as (cursor):
            if self.is_sqlite:
                sql = sql.replace('%s', '?')
            else:
                if data is None:
                    cursor.execute(sql)
                else:
                    cursor.execute(sql, data)
            return cursor.fetchone()

    def many(self, sql, data=None, size=None, autocommit=False):
        """ fetches many rows (size) from sql statement

        :param sql: sql statement
        :param data: data for sql statement
        :param size: size of rows
        :param autocommit: True or False

        :return: many rows from table
        """
        with self.get_cursor(autocommit=autocommit) as (cursor):
            if self.is_sqlite:
                sql = sql.replace('%s', '?')
            else:
                if data is None:
                    cursor.execute(sql)
                else:
                    cursor.execute(sql, data)
            return cursor.fetchmany(size=size)

    def all(self, sql, data=None, autocommit=False):
        """ fetches all rows from sql statement

        :param sql: sql statement
        :param data: data for sql statement
        :param autocommit: True or False

        :return: all rows from table
        """
        with self.get_cursor(autocommit=autocommit) as (cursor):
            if self.is_sqlite:
                sql = sql.replace('%s', '?')
            else:
                if data is None:
                    cursor.execute(sql)
                else:
                    cursor.execute(sql, data)
            return cursor.fetchall()