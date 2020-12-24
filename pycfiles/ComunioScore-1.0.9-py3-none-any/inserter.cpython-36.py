# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/ComunioScore/db/inserter.py
# Compiled at: 2020-04-13 07:58:16
# Size of source mod 2**32: 2613 bytes
import logging
from ComunioScore.db import DBConnector, Error
from ComunioScore.exceptions import DBInserterError, DBIntegrityError

class DBInserter(DBConnector):
    """DBInserter"""

    def __init__(self):
        self.logger = logging.getLogger('ComunioScore')
        self.logger.info('Create class DBInserter')
        super().__init__()

    def sql(self, sql, autocommit=False):
        """ executes a sql statement

        :param sql: sql statement
        :param autocommit: bool to enable autocommit
        """
        with self.get_cursor(autocommit=autocommit) as (cursor):
            cursor.execute(sql)

    def one(self):
        """ insert one entry in a row

        """
        pass

    def row(self, sql, data, autocommit=False):
        """ insert one row into database table

                sql= INSERT INTO comunio (id, username, wealth) VALUES (%s, %s, %s)
                data = (13, "test", 353.24)

                row(sql=sql, data=data)

        :param sql: sql statement
        :param data: data as a set
        :param autocommit: bool to enable autocommit
        """
        with self.get_cursor(autocommit=autocommit) as (cursor):
            if self.is_sqlite:
                sql = sql.replace('%s', '?')
            try:
                cursor.execute(sql, data)
            except Error as e:
                if e.pgcode == '23505':
                    raise DBIntegrityError(e)

    def many_rows(self, sql, datas, autocommit=False):
        """ insert many rows into database table

                sql= INSERT INTO comunio (id, username, wealth) VALUES (%s, %s, %s)
                datas = [(13, "test", 353.24), (14, "test2", 400.02)]

                many_rows(sql=sql, datas=datas)

        :param sql: sql statement
        :param datas: data as a list
        :param autocommit: bool to enable autocomm
        """
        if isinstance(datas, list):
            with self.get_cursor(autocommit=autocommit) as (cursor):
                if self.is_sqlite:
                    sql = sql.replace('%s', '?')
                try:
                    cursor.executemany(sql, datas)
                except Error as e:
                    if e.pgcode == '23505':
                        raise DBIntegrityError(e)

        else:
            raise DBInserterError("'datas' must be type of list")