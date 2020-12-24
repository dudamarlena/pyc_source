# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\b3\storage\postgresql.py
# Compiled at: 2016-03-08 18:42:10
import b3, re, sys
from b3.storage.cursor import Cursor as DBCursor
from b3.storage.common import DatabaseStorage
from time import time
from traceback import extract_tb

class PostgresqlStorage(DatabaseStorage):
    _reconnectDelay = 60
    _reInsert = re.compile('^INSERT', re.IGNORECASE)
    protocol = 'postgresql'

    def __new__(cls, *args, **kwargs):
        """
        Will make sure that the system has the necessary libraries.
        :raise ImportError: If the system misses the necessary libraries needed to setup the storage module.
        """
        try:
            import psycopg2
        except ImportError:
            psycopg2 = None
            raise ImportError("missing PostgreSQL connector driver. You need to install 'psycopg2': look for 'dependencies' in B3 documentation.")

        return super(PostgresqlStorage, cls).__new__(cls)

    def __init__(self, dsn, dsnDict, console):
        """
        Object constructor.
        :param dsn: The database connection string.
        :param dsnDict: The database connection string parsed into a dict.
        :param console: The console instance.
        """
        super(PostgresqlStorage, self).__init__(dsn, dsnDict, console)
        if not self.dsnDict['host']:
            raise AttributeError('invalid PostgreSQL host in %(protocol)s://%(user)s:******@%(host)s:%(port)s%(path)s' % self.dsnDict)
        if not self.dsnDict['path'] or not self.dsnDict['path'][1:]:
            raise AttributeError('missing PostgreSQL database name in %(protocol)s://%(user)s:******@%(host)s:%(port)s%(path)s' % self.dsnDict)
        patch_query_builder(self.console)

    def connect(self):
        """
        Establish and return a connection with the storage layer.
        Will store the connection object also in the 'db' attribute so in the future we can reuse it.
        :return The connection instance if established successfully, otherwise None.
        """
        if time() - self._lastConnectAttempt < self._reconnectDelay:
            self.db = None
            self.console.bot('New PostgreSQL database connection requested but last connection attempt failed less than %s seconds ago: exiting...' % self._reconnectDelay)
        else:
            self.shutdown()
            self.console.bot('Connecting to PostgreSQL database: %(protocol)s://%(user)s:******@%(host)s:%(port)s%(path)s...', self.dsnDict)
            try:
                import psycopg2
                self.db = psycopg2.connect(host=self.dsnDict['host'], port=self.dsnDict['port'], user=self.dsnDict['user'], password=self.dsnDict['password'], database=self.dsnDict['path'][1:])
                self.db.set_isolation_level(psycopg2.extensions.ISOLATION_LEVEL_AUTOCOMMIT)
                self.db.set_client_encoding('UTF8')
                self.console.bot('Successfully established a connection with PostgreSQL database')
                self._lastConnectAttempt = 0
                if self._consoleNotice:
                    self.console.screen.write('Connecting to DB : OK\n')
                    self._consoleNotice = False
                if not self.getTables():
                    try:
                        self.console.info('Missing PostgreSQL database tables: importing SQL file: %s...' % b3.getAbsolutePath('@b3/sql/postgresql/b3.sql'))
                        self.queryFromFile('@b3/sql/postgresql/b3.sql')
                    except Exception as e:
                        self.shutdown()
                        self.console.critical('Missing PostgreSQL database tables. You need to create the necessary tables for B3 to work. You can do so by importing the following SQL script into your database: %s. An attempt of creating tables automatically just failed: %s' % (
                         b3.getAbsolutePath('@b3/sql/postgresql/b3.sql'), e))

            except Exception as e:
                self.console.error('Database connection failed: working in remote mode: %s - %s', e, extract_tb(sys.exc_info()[2]))
                self.db = None
                self._lastConnectAttempt = time()
                if self._consoleNotice:
                    self.console.screen.write('Connecting to DB : FAILED!\n')
                    self._consoleNotice = False

        return self.db

    def getConnection(self):
        """
        Return the database connection. If the connection has not been established yet, will establish a new one.
        :return The connection instance, or None if no connection can be established.
        """
        if self.db and not self.db.closed:
            return self.db
        return self.connect()

    def shutdown(self):
        """
        Close the current active database connection.
        """
        if self.db and not self.db.closed:
            self.console.bot('Closing connection with PostgreSQL database...')
            self.db.close()
        self.db = None
        return

    def getTables(self):
        """
        List the tables of the current database.
        :return: List of strings.
        """
        tables = []
        cursor = self.query("SELECT table_name FROM information_schema.tables WHERE table_schema = 'public'")
        if cursor and not cursor.EOF:
            while not cursor.EOF:
                row = cursor.getRow()
                tables.append(row.values()[0])
                cursor.moveNext()

        cursor.close()
        return tables

    def truncateTable(self, table):
        """
        Empty a database table (or a collection of tables)
        :param table: The database table or a collection of tables
        :raise KeyError: If the table is not present in the database
        """
        current_tables = self.getTables()
        if isinstance(table, tuple) or isinstance(table, list):
            for v in table:
                if v not in current_tables:
                    raise KeyError("could not find table '%s' in the database" % v)

            self.query('TRUNCATE %s RESTART IDENTITY CASCADE;' % (', ').join(table))
        else:
            if table not in current_tables:
                raise KeyError("could not find table '%s' in the database" % table)
            self.query('TRUNCATE %s RESTART IDENTITY CASCADE;' % table)

    def _query(self, query, bindata=None):
        """
        Execute a query on the storage layer (internal method).
        :param query: The query to execute.
        :param bindata: Data to bind to the given query.
        :raise Exception: If the query cannot be evaluated.
        """
        self._lock.acquire()
        try:
            newquery = query.replace('`', '').strip()
            cursor = self.db.cursor()
            if bindata is None:
                cursor.execute(newquery)
            else:
                cursor.execute(newquery, bindata)
            dbcursor = DBCursor(cursor, self.db)
            if self._reInsert.match(newquery):
                try:
                    cursor = self.db.cursor()
                    cursor.execute('SELECT LASTVAL();')
                    dbcursor.lastrowid = cursor.fetchone()[0]
                    dbcursor._cursor.lastrowid = dbcursor.lastrowid
                    cursor.close()
                except Exception as e:
                    pass

        finally:
            self._lock.release()

        return dbcursor

    def status(self):
        """
        Check whether the connection with the storage layer is active or not.
        :return True if the connection is active, False otherwise.
        """
        if self.db and not self.db.closed:
            return True
        return False


from b3.querybuilder import QueryBuilder

def patch_query_builder(console):

    def new_escape(self, word):
        """
        Escape quotes from a given string.
        :param word: The string on which to perform the escape
        """
        if isinstance(word, int) or isinstance(word, long) or isinstance(word, complex) or isinstance(word, float):
            return str(word)
        else:
            if word is None:
                return "'None'"
            else:
                return "'%s'" % word.replace("'", "''")

            return

    console.bot('patching QueryBuilder.escape: %s -> %s' % (id(QueryBuilder.escape), id(new_escape)))
    QueryBuilder.escape = new_escape