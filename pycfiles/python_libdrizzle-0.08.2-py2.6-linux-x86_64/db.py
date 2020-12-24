# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/drizzle/db.py
# Compiled at: 2010-03-22 02:56:07
from itertools import izip, islice
from drizzle import libdrizzle as _libdrizzle
from drizzle.errors import *
from drizzle.column_types import *
libdrizzle = _libdrizzle.Drizzle()
apilevel = '2.0'

def connect(*args, **kwargs):
    """Connect to a database, returning a new Connection object."""
    connection = Connection(*args, **kwargs)
    connection._connect()
    return connection


def _columns_description(columns):
    """Given a list of libdrizzle Column objects, generate a list of 
    tuples suitable for the Python DB-API Cursor.descriptions field.
    
    """
    description = list()
    for column in columns:
        name = column.name()
        column_type = column.column_type()
        display_size = column.max_size()
        internal_size = column.size()
        precision = None
        scale = None
        null_ok = column.flags() & _libdrizzle.DRIZZLE_COLUMN_FLAGS_NOT_NULL == 0
        description.append((name, column_type, display_size, internal_size,
         precision, scale, null_ok))

    return description


class Connection(object):

    def __init__(self, host=None, username=None, password=None, database=None, port=None):
        self.host = host
        self.port = port
        self.username = username
        self.password = password
        self.database = database
        self._drizzle_connection = None
        return

    def _connect(self):
        self._drizzle_connection = libdrizzle.create_connection()
        self._drizzle_connection.set_tcp(self.host, self.port)
        self._drizzle_connection.set_db(self.database)
        self._drizzle_connection.connect()
        self.autocommit = False

    def _check_connected(self):
        """Raise a InterfaceError if the Connection has been closed."""
        if self.is_closed:
            raise InterfaceError('Connection closed')

    def close(self):
        self._check_connected()
        self._drizzle_connection.close()
        self._drizzle_connection = None
        return

    def commit(self):
        self._check_connected()
        self._drizzle_connection.query('COMMIT')

    def rollback(self):
        self._check_connected()
        self._drizzle_connection.query('ROLLBACK')

    @property
    def is_closed(self):
        """Return true if the Connection is not open."""
        return self._drizzle_connection is None

    def cursor(self, convert=True):
        """Return a new Cursor object using the connection."""
        return Cursor(self, convert)

    @property
    def autocommit(self):
        return self._drizzle_connection.status() & _libdrizzle.DRIZZLE_CON_STATUS_AUTOCOMMIT != 0

    @autocommit.setter
    def autocommit(self, status):
        self._check_connected()
        sql = ('SET autocommit={0}').format('ON' if status else 'OFF')
        self._drizzle_connection.query(sql)

    @property
    def is_transactional(self):
        return self._drizzle_connection.capabilities() & _libdrizzle.DRIZZLE_CAPABILITIES_TRANSACTIONS != 0

    @property
    def server_version(self):
        """Return the server version string."""
        self._check_connected()
        return self._drizzle_connection.server_version()

    @property
    def protocol_version(self):
        """Return the protocol version number in use."""
        self._check_connected()
        return self._drizzle_connection.protocol_version()


Connection.Warning = Warning
Connection.Error = Error
Connection.InterfaceError = InterfaceError
Connection.DatabaseError = DatabaseError
Connection.OperationalError = OperationalError
Connection.IntegrityError = IntegrityError
Connection.InternalError = InternalError
Connection.ProgrammingError = ProgrammingError
Connection.NotSupportedError = NotSupportedError

class Cursor(object):

    def __init__(self, connection, convert=True):
        self._connection = connection
        self.arraysize = 1
        self._convert_rows = convert
        self._last_result = None
        self._has_rows_left = False
        self._reset()
        return

    def _reset(self):
        if self._has_rows_left:
            for row in self:
                pass

        self._last_result = None
        self._has_rows_left = False
        self._columns = None
        self._description = None
        return

    def close(self):
        self._connection = None
        return

    @property
    def is_closed(self):
        """Return true if the Cursor is not open."""
        return self.connection is None

    @property
    def connection(self):
        """The Connection object on which this cursor was created."""
        return self._connection

    @property
    def _drizzle_connection(self):
        return self.connection._drizzle_connection

    def __iter__(self):
        """Iterate over query result rows one-by-one."""
        return iter(self.fetchone, None)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        if exc_type:
            self.connection.rollback()
        else:
            self.connection.commit()
        self.close()

    def _check_open(self):
        """Raise a InterfaceError if the Cursor has been closed."""
        if not self.connection:
            raise InterfaceError('Cursor closed')

    def _check_has_data(self):
        if self._last_result is None or self.description is None:
            raise InterfaceError('No data to fetch')
        return

    def _convert_row(self, row):
        return tuple(from_db.convert(field, valuetype=descr[1]) for (descr, field) in izip(self.description, row))

    def _update_description(self):
        self._description = _columns_description(self._columns)

    def execute(self, sql):
        """Execute a database operation, making the results accessible
        using this cursor.
        
        """
        self._check_open()
        self.connection._check_connected()
        self._reset()
        self._last_result = self._drizzle_connection.query(sql)
        if self._last_result.column_count() != 0:
            self._last_result.buffer_column()
            self._columns = [ column for column in iter(self._last_result.next_column, None)
                            ]
            self._has_rows_left = True
            self._update_description()
        return

    def fetchone(self):
        """Fetch the next row of a query result set, returning a single
        sequence, or None when no more data is available.
        
        """
        self._check_open()
        self.connection._check_connected()
        self._check_has_data()
        if self._has_rows_left:
            row = self._last_result.buffer_row()
            if row is not None:
                if self._convert_rows:
                    return self._convert_row(row)
                return row
            self._has_rows_left = False
            self._update_description()
        return

    def fetchmany(self, size=None):
        """Fetch the next set of rows of a query result, returning a
        sequence of sequences (e.g. a list of tuples). An empty sequence
        is returned when no more rows are available.
            
        The number of rows to fetch per call is specified by the
        parameter.  If it is not given, the cursor's arraysize
        determines the number of rows to be fetched.
        
        """
        self._check_open()
        self.connection._check_connected()
        self._check_has_data()
        if size is None:
            size = self.arraysize
        if self._has_rows_left:
            rows = self._last_result.buffer_multiple_rows(size)
            if len(rows) < size:
                self._has_rows_left = False
                self._update_description()
            if self._convert_rows:
                return [ self._convert_row(row) for row in rows ]
            return rows
        else:
            return []
        return

    def fetchall(self):
        """Fetch all (remaining) rows of a query result, returning them
        as a sequence of sequences (e.g. a list of tuples).
        
        """
        self._check_open()
        self.connection._check_connected()
        self._check_has_data()
        if self._has_rows_left:
            if self.rownumber == 0:
                self._last_result.buffer_result()
                self._has_rows_left = False
                rows = list(iter(self._last_result.next_row, None))
            else:
                rows = list(iter(self))
            self._update_description()
            if self._convert_rows:
                return [ self._convert_row(row) for row in rows ]
            return rows
        else:
            return []
        return

    def setinputsizes(self, sizes):
        """Included for DB-API interface compatibility. No effect."""
        pass

    def setoutputsize(self, size, column=None):
        """Included for DB-API interface compatibility. No effect."""
        pass

    @property
    def rowcount(self):
        """The number of rows that the last .execute*() produced.
        
        The attribute is -1 in case no .execute*() has been performed on
        the cursor or the rowcount of the last operation is cannot be
        determined.
        
        Note: for Drizzle, the row count of a query cannot be determined
        until all rows have been fetched.
        
        """
        if self._last_result is None or self._has_rows_left:
            return -1
        else:
            if self.description is None:
                return self._last_result.affected_rows()
            else:
                return self._last_result.row_count()
            return

    @property
    def rownumber(self):
        """The current 0-based index of the cursor in the result set or
        None if the index cannot be determined.
        
        """
        return self._last_result.row_current()

    @property
    def lastrowid(self):
        """The rowid of the last modified row."""
        return self._last_result.insert_id()

    @property
    def description(self):
        """A list of tuples describing the columns in the current result
        set:
        
        Tuples returned are of the form:
        (name, type, display_size, internal_size, precision, scale, null_ok)
        
        """
        return self._description