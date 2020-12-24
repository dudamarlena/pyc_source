# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/mdipierro/make_web2py/web2py/gluon/contrib/pg8000/interface.py
# Compiled at: 2013-10-14 11:16:24
__author__ = 'Mathieu Fenniak'
import socket, protocol, threading
from errors import *

def conninfo_parse(conninfo):
    """Conninfo parser routine based on libpq conninfo_parse"""
    options = {}
    buf = conninfo + ' '
    tmp = pname = ''
    quoted_string = False
    cp = 0
    while cp < len(buf):
        c = buf[cp]
        if c.isspace() and tmp and not quoted_string and pname:
            options[pname] = tmp
            tmp = pname = ''
        elif c == "'":
            quoted_string = not quoted_string
        elif c == '\\':
            cp += 1
            tmp += buf[cp]
        elif c == '=':
            if not tmp:
                raise RuntimeError('missing parameter name (conninfo:%s)' % cp)
            pname = tmp
            tmp = ''
        elif not c.isspace() or quoted_string:
            tmp += c
        cp += 1

    if quoted_string:
        raise RuntimeError('unterminated quoted string (conninfo:%s)' % cp)
    return options


class DataIterator(object):

    def __init__(self, obj, func):
        self.obj = obj
        self.func = func

    def __iter__(self):
        return self

    def next(self):
        retval = self.func(self.obj)
        if retval == None:
            raise StopIteration()
        return retval


statement_number_lock = threading.Lock()
statement_number = 0

class PreparedStatement(object):
    row_cache_size = 100

    def __init__(self, connection, statement, *types, **kwargs):
        global statement_number
        if connection == None or connection.c == None:
            raise InterfaceError('connection not provided')
        try:
            statement_number_lock.acquire()
            self._statement_number = statement_number
            statement_number += 1
        finally:
            statement_number_lock.release()

        self.c = connection.c
        self._portal_name = None
        self._statement_name = kwargs.get('statement_name', 'pg8000_statement_%s' % self._statement_number)
        self._row_desc = None
        self._cached_rows = []
        self._ongoing_row_count = 0
        self._command_complete = True
        self._parse_row_desc = self.c.parse(self._statement_name, statement, types)
        self._lock = threading.RLock()
        return

    def close(self):
        if self._statement_name != '':
            self.c.close_statement(self._statement_name)
        if self._portal_name != None:
            self.c.close_portal(self._portal_name)
            self._portal_name = None
        return

    row_description = property(lambda self: self._getRowDescription())

    def _getRowDescription(self):
        if self._row_desc == None:
            return
        else:
            return self._row_desc.fields

    def execute(self, *args, **kwargs):
        self._lock.acquire()
        try:
            if not self._command_complete:
                self._cached_rows = []
                self._ongoing_row_count = 0
            if self._portal_name != None:
                self.c.close_portal(self._portal_name)
            self._command_complete = False
            self._portal_name = 'pg8000_portal_%s' % self._statement_number
            self._row_desc, cmd = self.c.bind(self._portal_name, self._statement_name, args, self._parse_row_desc, kwargs.get('stream'))
            if self._row_desc:
                self._fill_cache()
            else:
                self._command_complete = True
                self._ongoing_row_count = -1
                if cmd != None and cmd.rows != None:
                    self._ongoing_row_count = cmd.rows
        finally:
            self._lock.release()

        return

    def _fill_cache(self):
        self._lock.acquire()
        try:
            if self._cached_rows:
                raise InternalError("attempt to fill cache that isn't empty")
            end_of_data, rows = self.c.fetch_rows(self._portal_name, self.row_cache_size, self._row_desc)
            self._cached_rows = rows
            if end_of_data:
                self._command_complete = True
        finally:
            self._lock.release()

    def _fetch(self):
        if not self._row_desc:
            raise ProgrammingError('no result set')
        self._lock.acquire()
        try:
            if not self._cached_rows:
                if self._command_complete:
                    return
                self._fill_cache()
                if self._command_complete and not self._cached_rows:
                    return
            row = self._cached_rows.pop(0)
            self._ongoing_row_count += 1
            return tuple(row)
        finally:
            self._lock.release()

        return

    row_count = property(lambda self: self._get_row_count())

    def _get_row_count(self):
        self._lock.acquire()
        try:
            if not self._command_complete:
                end_of_data, rows = self.c.fetch_rows(self._portal_name, 0, self._row_desc)
                self._cached_rows += rows
                if end_of_data:
                    self._command_complete = True
                else:
                    raise InternalError('fetch_rows(0) did not hit end of data')
            return self._ongoing_row_count + len(self._cached_rows)
        finally:
            self._lock.release()

    def read_dict(self):
        row = self._fetch()
        if row == None:
            return row
        else:
            retval = {}
            for i in range(len(self._row_desc.fields)):
                col_name = self._row_desc.fields[i]['name']
                if retval.has_key(col_name):
                    raise InterfaceError('cannot return dict of row when two columns have the same name (%r)' % (col_name,))
                retval[col_name] = row[i]

            return retval

    def read_tuple(self):
        return self._fetch()

    def iterate_tuple(self):
        return DataIterator(self, PreparedStatement.read_tuple)

    def iterate_dict(self):
        return DataIterator(self, PreparedStatement.read_dict)


class SimpleStatement(PreparedStatement):
    """Internal wrapper to Simple Query protocol emulating a PreparedStatement"""
    row_cache_size = None

    def __init__(self, connection, statement):
        if connection == None or connection.c == None:
            raise InterfaceError('connection not provided')
        self.c = connection.c
        self._row_desc = None
        self._cached_rows = []
        self._ongoing_row_count = -1
        self._command_complete = True
        self.statement = statement
        self._lock = threading.RLock()
        return

    def close(self):
        pass

    def execute(self, *args, **kwargs):
        """Run the SQL simple query stataments"""
        self._lock.acquire()
        try:
            self._row_desc, cmd_complete, self._cached_rows = self.c.send_simple_query(self.statement, kwargs.get('stream'))
            self._command_complete = True
            self._ongoing_row_count = -1
            if cmd_complete is not None and cmd_complete.rows is not None:
                self._ongoing_row_count = cmd_complete.rows
        finally:
            self._lock.release()

        return

    def _fill_cache(self):
        pass

    def _fetch(self):
        if not self._row_desc:
            raise ProgrammingError('no result set')
        self._lock.acquire()
        try:
            if not self._cached_rows:
                return
            else:
                row = self._cached_rows.pop(0)
                return tuple(row)

        finally:
            self._lock.release()

        return

    def _get_row_count(self):
        return self._ongoing_row_count


class Cursor(object):

    def __init__(self, connection):
        self.connection = connection
        self._stmt = None
        return

    def require_stmt(func):

        def retval(self, *args, **kwargs):
            if self._stmt == None:
                raise ProgrammingError('attempting to use unexecuted cursor')
            return func(self, *args, **kwargs)

        return retval

    row_description = property(lambda self: self._getRowDescription())

    def _getRowDescription(self):
        if self._stmt == None:
            return
        else:
            return self._stmt.row_description

    def execute(self, query, *args, **kwargs):
        if self.connection.is_closed:
            raise ConnectionClosedError()
        self.connection._unnamed_prepared_statement_lock.acquire()
        try:
            if kwargs.get('simple_query'):
                self._stmt = SimpleStatement(self.connection, query)
            else:
                self._stmt = PreparedStatement(self.connection, query, statement_name='', *[ {'type': type(x), 'value': x} for x in args ])
            self._stmt.execute(*args, **kwargs)
        finally:
            self.connection._unnamed_prepared_statement_lock.release()

    row_count = property(lambda self: self._get_row_count())

    @require_stmt
    def _get_row_count(self):
        return self._stmt.row_count

    @require_stmt
    def read_dict(self):
        return self._stmt.read_dict()

    @require_stmt
    def read_tuple(self):
        return self._stmt.read_tuple()

    @require_stmt
    def iterate_tuple(self):
        return self._stmt.iterate_tuple()

    @require_stmt
    def iterate_dict(self):
        return self._stmt.iterate_dict()

    def close(self):
        if self._stmt != None:
            self._stmt.close()
            self._stmt = None
        return

    def fileno(self):
        return self.connection.fileno()

    def isready(self):
        return self.connection.isready()


class Connection(Cursor):

    def __init__(self, dsn='', user=None, host=None, unix_sock=None, port=5432, database=None, password=None, socket_timeout=60, ssl=False):
        self._row_desc = None
        if dsn:
            opts = conninfo_parse(dsn)
            database = opts.get('dbname', database)
            user = opts.get('user', user)
            password = opts.get('password', user)
            host = opts.get('host', host)
            port = int(opts.get('port', port))
            ssl = opts.get('sslmode', 'disable') != 'disable'
        try:
            self.c = protocol.Connection(unix_sock=unix_sock, host=host, port=port, socket_timeout=socket_timeout, ssl=ssl)
            self.c.authenticate(user, password=password, database=database)
        except socket.error as e:
            raise InterfaceError('communication error', e)

        Cursor.__init__(self, self)
        self._begin = PreparedStatement(self, 'BEGIN TRANSACTION')
        self._commit = PreparedStatement(self, 'COMMIT TRANSACTION')
        self._rollback = PreparedStatement(self, 'ROLLBACK TRANSACTION')
        self._unnamed_prepared_statement_lock = threading.RLock()
        self.in_transaction = False
        self.autocommit = False
        return

    NotificationReceived = property(lambda self: getattr(self.c, 'NotificationReceived'), lambda self, value: setattr(self.c, 'NotificationReceived', value))
    NoticeReceived = property(lambda self: getattr(self.c, 'NoticeReceived'), lambda self, value: setattr(self.c, 'NoticeReceived', value))
    ParameterStatusReceived = property(lambda self: getattr(self.c, 'ParameterStatusReceived'), lambda self, value: setattr(self.c, 'ParameterStatusReceived', value))

    def begin(self):
        if self.is_closed:
            raise ConnectionClosedError()
        if self.autocommit:
            return
        self._begin.execute()
        self.in_transaction = True

    def commit(self):
        if self.is_closed:
            raise ConnectionClosedError()
        self._commit.execute()
        self.in_transaction = False

    def rollback(self):
        if self.is_closed:
            raise ConnectionClosedError()
        self._rollback.execute()
        self.in_transaction = False

    def close(self):
        if self.is_closed:
            raise ConnectionClosedError()
        self.c.close()
        self.c = None
        return

    is_closed = property(lambda self: self.c == None)

    def fileno(self):
        return self.c.fileno()

    def isready(self):
        return self.c.isready()

    def server_version(self):
        return self.c.server_version()

    def encoding(self, encoding=None):
        """Returns the client_encoding as reported from the connected server"""
        return self.c.encoding()