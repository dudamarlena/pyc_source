# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\b3\storage\sqlite.py
# Compiled at: 2016-03-08 18:42:10
import b3, os
from b3.storage.common import DatabaseStorage

class SqliteStorage(DatabaseStorage):
    protocol = 'sqlite'

    def __init__(self, dsn, dsnDict, console):
        """
        Object constructor.
        :param dsn: The database connection string.
        :param dsnDict: The database connection string parsed into a dict.
        :param console: The console instance.
        """
        super(SqliteStorage, self).__init__(dsn, dsnDict, console)

    def connect(self):
        """
        Establish and return a connection with the storage layer.
        Will store the connection object also in the 'db' attribute so in the future we can reuse it.
        :return The connection instance if established successfully, otherwise None.
        """
        try:
            try:
                import sqlite3
                path = b3.getWritableFilePath(self.dsn[9:])
                self.console.bot('Using database file: %s' % path)
                is_new_database = not os.path.isfile(path)
                self.db = sqlite3.connect(path, check_same_thread=False)
                self.db.isolation_level = None
            except Exception as e:
                self.db = None
                self.console.error('Database connection failed: %s', e)
                if self._consoleNotice:
                    self.console.screen.write('Connecting to DB : FAILED\n')
                    self._consoleNotice = False

            if path == ':memory:' or is_new_database:
                self.console.info('Importing SQL file: %s...' % b3.getAbsolutePath('@b3/sql/sqlite/b3.sql'))
                self.queryFromFile('@b3/sql/sqlite/b3.sql')
            if self._consoleNotice:
                self.console.screen.write('Connecting to DB : OK\n')
                self._consoleNotice = False
        finally:
            return self.db

    def getConnection(self):
        """
        Return the database connection. If the connection has not been established yet, will establish a new one.
        :return The connection instance, or None if no connection can be established.
        """
        if self.db:
            return self.db
        return self.connect()

    def shutdown(self):
        """
        Close the current active database connection.
        """
        if self.db:
            self.console.bot('Closing connection with SQLite database...')
            self.db.close()
        self.db = None
        return

    def getTables(self):
        """
        List the tables of the current database.
        :return: List of strings.
        """
        tables = []
        cursor = self.query("SELECT * FROM sqlite_master WHERE type='table'")
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
                self.query('DELETE FROM %s;' % v)
                self.query("DELETE FROM sqlite_sequence WHERE name='%s';" % v)

        else:
            if table not in current_tables:
                raise KeyError("could not find table '%s' in the database" % table)
            self.query('DELETE FROM %s;' % table)
            self.query("DELETE FROM sqlite_sequence WHERE name='%s';" % table)

    def status(self):
        """
        Check whether the connection with the storage layer is active or not.
        :return True if the connection is active, False otherwise.
        """
        return self.db is None