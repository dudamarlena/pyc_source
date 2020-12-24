# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/credstuffer/db/fetcher.py
# Compiled at: 2019-12-19 13:25:41
# Size of source mod 2**32: 2323 bytes
import logging
from credstuffer.db.connector import DBConnector

class DBFetcher(DBConnector):
    """DBFetcher"""

    def __init__(self):
        self.logger = logging.getLogger('credstuffer')
        self.logger.info('create class DBFetcher')
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