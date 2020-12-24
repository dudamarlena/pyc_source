# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/credstuffer/db/sqlite.py
# Compiled at: 2019-12-19 13:25:41
# Size of source mod 2**32: 1832 bytes
import sqlite3, logging
from credstuffer.db.context import SQLiteCursorContextManager, SQLiteConnectionContextManager
from credstuffer.exceptions import DBConnectorError

class SQLite:
    __doc__ = ' class SQLite for connection to sqlite database\n\n    USAGE:\n            SQLite.connect(path="database.db")\n\n    '
    connection = None

    def __init__(self):
        self.logger = logging.getLogger('credstuffer')
        self.logger.info('create class SQLite')

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
            logging.getLogger('credstuffer').error('Could not connect to SQLite Database: {}'.format(ex))

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