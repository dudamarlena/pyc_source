# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/ComunioScore/db/sqlite.py
# Compiled at: 2020-04-13 07:58:16
# Size of source mod 2**32: 1836 bytes
import sqlite3, logging
from ComunioScore.db.context import SQLiteCursorContextManager, SQLiteConnectionContextManager
from ComunioScore.exceptions import DBConnectorError

class SQLite:
    """SQLite"""
    connection = None

    def __init__(self):
        self.logger = logging.getLogger('ComunioScore')
        self.logger.info('Create class SQLite')

    def __del__(self):
        """ destructor

        """
        SQLite.connection.close()

    @classmethod
    def connect(cls, path):
        """ connects to a local database file

        :param path: path to database file
        """
        try:
            cls.connection = sqlite3.connect(path, isolation_level=None)
        except sqlite3.DatabaseError as ex:
            logging.getLogger('ComunioScore').error('Could not connect to SQLite Database: {}'.format(ex))

    def get_cursor(self):
        """ get a cursor object

        :return: SQLiteCursorContextManager
        """
        if SQLite.connection is not None:
            return SQLiteCursorContextManager(conn=(SQLite.connection))
        raise DBConnectorError('SQLite.connection was not defined!')

    def get_conn(self):
        """ get a connection object

        :return: SQLiteConnectionContextManager
        """
        if SQLite.connection is not None:
            return SQLiteConnectionContextManager(conn=(SQLite.connection))
        raise DBConnectorError('SQLite.connection was not defined!')

    def commit(self):
        """ commits the current transaction

        """
        if SQLite.connection is not None:
            SQLite.connection.commit()
        else:
            raise DBConnectorError('SQLite.connection was not defined!')