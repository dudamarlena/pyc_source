# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/credstuffer/db/connector.py
# Compiled at: 2020-04-05 08:14:43
# Size of source mod 2**32: 3944 bytes
import logging, sqlite3
from credstuffer.db.context import PostgresqlCursorContextManager, PostgresqlConnectionContextManager, SQLiteCursorContextManager, SQLiteConnectionContextManager
from credstuffer.exceptions import DBConnectorError
try:
    import psycopg2
    from psycopg2.pool import ThreadedConnectionPool
    from psycopg2 import Error
    is_psycopg2_importable = True
except ImportError as ex:
    is_psycopg2_importable = False
    print(ex)

class DBConnector:
    """DBConnector"""
    connection = None
    pool = None
    is_sqlite = False

    def __init__(self):
        self.logger = logging.getLogger('credstuffer')
        self.logger.info('create class DBConnector')

    @classmethod
    def connect_psycopg(cls, host, port, username, password, dbname, minConn=1, maxConn=10):
        """ connection to the ThreadedConnectionPool

        :param host: hostname of database
        :param port: port of database
        :param username: username for connection
        :param password: password for connection
        :param dbname: database name for connection
        :param minConn: minimum connections
        :param maxConn: maximum connections
        """
        try:
            if is_psycopg2_importable:
                cls.pool = ThreadedConnectionPool(minconn=minConn, maxconn=maxConn, user=username, password=password,
                  host=host,
                  port=port,
                  database=dbname)
                logging.getLogger('credstuffer').info('Connect to {} as user {} to database {}'.format(host, username, dbname))
                return True
            else:
                print('psycogp2 is not imported')
                return False
        except psycopg2.DatabaseError as e:
            logging.getLogger('credstuffer').error('Could not connect to ThreadedConnectionPool: {}'.format(e))
            return False

    @classmethod
    def connect_sqlite(cls, path):
        """ connection to the sqlite database

        :param path: path to database file
        """
        try:
            cls.connection = sqlite3.connect(path, isolation_level=None, check_same_thread=False)
            cls.is_sqlite = True
            return True
        except sqlite3.DatabaseError as ex:
            logging.getLogger('credstuffer').error('Could not connect to sqlite Database: {}'.format(ex))
            return False

    @classmethod
    def close(cls):
        """ closes all pool connections

        """
        cls.pool.closeall()

    def get_cursor(self, autocommit=False):
        """ get a cursor object from ConnectionPool

        :param autocommit: bool to enable autocommit
        :return: cursor object
        """
        if self.pool is not None:
            return PostgresqlCursorContextManager((self.pool), autocommit=autocommit)
        if self.connection is not None:
            return SQLiteCursorContextManager(self.connection)
        raise DBConnectorError('Database connection is not defined')

    def get_conn(self, autocommit=False):
        """ get a connection object from ConnectionPool

        :param autocommit: bool to enable autocommit
        :return: connection object
        """
        if self.pool is not None:
            return PostgresqlConnectionContextManager((self.pool), autocommit=autocommit)
        if self.connection is not None:
            return SQLiteConnectionContextManager(self.connection)
        raise DBConnectorError('Database connection is not defined')

    def commit(self):
        """ commits a sql statement

        """
        with self.get_conn() as (conn):
            conn.commit()