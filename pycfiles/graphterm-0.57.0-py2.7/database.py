# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.5-x86_64/egg/graphterm/bin/tornado/database.py
# Compiled at: 2012-01-23 23:44:33
"""A lightweight wrapper around MySQLdb."""
import copy, MySQLdb.constants, MySQLdb.converters, MySQLdb.cursors, itertools, logging, time

class Connection(object):
    """A lightweight wrapper around MySQLdb DB-API connections.

    The main value we provide is wrapping rows in a dict/object so that
    columns can be accessed by name. Typical usage::

        db = database.Connection("localhost", "mydatabase")
        for article in db.query("SELECT * FROM articles"):
            print article.title

    Cursors are hidden by the implementation, but other than that, the methods
    are very similar to the DB-API.

    We explicitly set the timezone to UTC and the character encoding to
    UTF-8 on all connections to avoid time zone and encoding errors.
    """

    def __init__(self, host, database, user=None, password=None, max_idle_time=25200):
        self.host = host
        self.database = database
        self.max_idle_time = max_idle_time
        args = dict(conv=CONVERSIONS, use_unicode=True, charset='utf8', db=database, init_command='SET time_zone = "+0:00"', sql_mode='TRADITIONAL')
        if user is not None:
            args['user'] = user
        if password is not None:
            args['passwd'] = password
        if '/' in host:
            args['unix_socket'] = host
        else:
            self.socket = None
            pair = host.split(':')
            if len(pair) == 2:
                args['host'] = pair[0]
                args['port'] = int(pair[1])
            else:
                args['host'] = host
                args['port'] = 3306
            self._db = None
            self._db_args = args
            self._last_use_time = time.time()
            try:
                self.reconnect()
            except Exception:
                logging.error('Cannot connect to MySQL on %s', self.host, exc_info=True)

        return

    def __del__(self):
        self.close()

    def close(self):
        """Closes this database connection."""
        if getattr(self, '_db', None) is not None:
            self._db.close()
            self._db = None
        return

    def reconnect(self):
        """Closes the existing database connection and re-opens it."""
        self.close()
        self._db = MySQLdb.connect(**self._db_args)
        self._db.autocommit(True)

    def iter(self, query, *parameters):
        """Returns an iterator for the given query and parameters."""
        self._ensure_connected()
        cursor = MySQLdb.cursors.SSCursor(self._db)
        try:
            self._execute(cursor, query, parameters)
            column_names = [ d[0] for d in cursor.description ]
            for row in cursor:
                yield Row(zip(column_names, row))

        finally:
            cursor.close()

    def query(self, query, *parameters):
        """Returns a row list for the given query and parameters."""
        cursor = self._cursor()
        try:
            self._execute(cursor, query, parameters)
            column_names = [ d[0] for d in cursor.description ]
            return [ Row(itertools.izip(column_names, row)) for row in cursor ]
        finally:
            cursor.close()

    def get(self, query, *parameters):
        """Returns the first row returned for the given query."""
        rows = self.query(query, *parameters)
        if not rows:
            return
        else:
            if len(rows) > 1:
                raise Exception('Multiple rows returned for Database.get() query')
            else:
                return rows[0]
            return

    def execute(self, query, *parameters):
        """Executes the given query, returning the lastrowid from the query."""
        return self.execute_lastrowid(query, *parameters)

    def execute_lastrowid(self, query, *parameters):
        """Executes the given query, returning the lastrowid from the query."""
        cursor = self._cursor()
        try:
            self._execute(cursor, query, parameters)
            return cursor.lastrowid
        finally:
            cursor.close()

    def execute_rowcount(self, query, *parameters):
        """Executes the given query, returning the rowcount from the query."""
        cursor = self._cursor()
        try:
            self._execute(cursor, query, parameters)
            return cursor.rowcount
        finally:
            cursor.close()

    def executemany(self, query, parameters):
        """Executes the given query against all the given param sequences.

        We return the lastrowid from the query.
        """
        return self.executemany_lastrowid(query, parameters)

    def executemany_lastrowid(self, query, parameters):
        """Executes the given query against all the given param sequences.

        We return the lastrowid from the query.
        """
        cursor = self._cursor()
        try:
            cursor.executemany(query, parameters)
            return cursor.lastrowid
        finally:
            cursor.close()

    def executemany_rowcount(self, query, parameters):
        """Executes the given query against all the given param sequences.

        We return the rowcount from the query.
        """
        cursor = self._cursor()
        try:
            cursor.executemany(query, parameters)
            return cursor.rowcount
        finally:
            cursor.close()

    def _ensure_connected(self):
        if self._db is None or time.time() - self._last_use_time > self.max_idle_time:
            self.reconnect()
        self._last_use_time = time.time()
        return

    def _cursor(self):
        self._ensure_connected()
        return self._db.cursor()

    def _execute(self, cursor, query, parameters):
        try:
            return cursor.execute(query, parameters)
        except OperationalError:
            logging.error('Error connecting to MySQL on %s', self.host)
            self.close()
            raise


class Row(dict):
    """A dict that allows for object-like property access syntax."""

    def __getattr__(self, name):
        try:
            return self[name]
        except KeyError:
            raise AttributeError(name)


FIELD_TYPE = MySQLdb.constants.FIELD_TYPE
FLAG = MySQLdb.constants.FLAG
CONVERSIONS = copy.copy(MySQLdb.converters.conversions)
field_types = [
 FIELD_TYPE.BLOB, FIELD_TYPE.STRING, FIELD_TYPE.VAR_STRING]
if 'VARCHAR' in vars(FIELD_TYPE):
    field_types.append(FIELD_TYPE.VARCHAR)
for field_type in field_types:
    CONVERSIONS[field_type] = [
     (
      FLAG.BINARY, str)] + CONVERSIONS[field_type]

IntegrityError = MySQLdb.IntegrityError
OperationalError = MySQLdb.OperationalError