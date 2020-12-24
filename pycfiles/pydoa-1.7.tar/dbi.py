# uncompyle6 version 3.6.7
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-i686/egg/pydo/dbi.py
# Compiled at: 2007-02-15 13:23:36
from itertools import izip
from threading import Lock, local
from collections import deque
import time
from pydo.log import *
from pydo.operators import BindingConverter
from pydo.exceptions import PyDOError
from pydo.utils import _strip_tablename, _import_a_class
exception_names = ('DataError', 'DatabaseError', 'Error', 'IntegrityError', 'InterfaceError',
                   'InternalError', 'NotSupportedError', 'OperationalError', 'ProgrammingError')

class DBIBase(object):
    """base class for db connection wrappers.
    """
    __module__ = __name__
    paramstyle = 'format'
    auto_increment = False
    has_sane_rowcount = True

    def __init__(self, connectArgs, connectFunc, dbapiModule, pool=None, verbose=False, initFunc=None):
        """
        constructor.
        * connectArgs are arguments passed directly to the underlying
          DBAPI driver.
        * connectFunc is the connect function from the DBAPI module.
        * pool is a connection pool instance.
        * verbose is whether or not to log the sql being executed.
        """
        self.connectArgs = connectArgs
        self.connectFunc = connectFunc
        self.pool = pool
        self.verbose = verbose
        self.initFunc = initFunc
        self._local = local()
        self.dbapiModule = dbapiModule
        self._initExceptions()

    def _initExceptions(self):
        self.exceptions = dict(((e, getattr(self.dbapiModule, e)) for e in exception_names))

    def conn():

        def fget(self):
            try:
                return self._local.connection
            except AttributeError:
                c = self._connect()
                self._local.connection = c
                return c

        def fset(self, c):
            self._local.connection = c

        def fdel(self):
            c = self._local.connection
            del self._local.connection
            c.close()

        return (
         fget, fset, fdel, 'the underlying db connection')

    conn = property(*conn())

    def swapConnection(self, connection):
        """switch the connection in use for the current thread with another one."""
        c = self._local.__dict__.get('connection')
        self._local.connection = connection
        return c

    def endConnection(self):
        """ disassociate from the current connection, which may be
        deleted or returned to a pool."""
        del self.conn

    def commit(self):
        """commits a transaction"""
        self.conn.commit()
        if self.pool:
            del self.conn

    def rollback(self):
        """rolls back a transaction"""
        self.conn.rollback()
        if self.pool:
            del self.conn

    def cursor(self):
        """returns a database cursor for direct access to the db connection"""
        return self.conn.cursor()

    def _connect(self):
        if self.pool:
            return self.pool.connect(self.connectFunc, self.connectArgs, self.initFunc)
        else:
            return _real_connect(self.connectFunc, self.connectArgs, self.initFunc)

    def getConverter(self):
        """returns a converter instance."""
        return BindingConverter(self.paramstyle)

    def execute(self, sql, values=(), qualified=False):
        """Executes the statement with the values and does conversion
        of the return result as necessary.
        result is list of dictionaries, or number of rows affected"""
        if self.verbose:
            debug('SQL: %s', sql)
            debug('bind variables: %s', values)
        c = self.conn.cursor()
        if values:
            c.execute(sql, values)
        else:
            c.execute(sql)
        resultset = c.fetchall()
        if not resultset:
            return c.rowcount
        res = self._convertResultSet(c.description, resultset, qualified)
        c.close()
        return res

    @staticmethod
    def _convertResultSet(description, resultset, qualified=False):
        """internal function that turns a result set into a list of dictionaries."""
        if qualified:
            fldnames = [ x[0] for x in description ]
        else:
            fldnames = [ _strip_tablename(x[0]) for x in description ]
        return [ dict(izip(fldnames, row)) for row in resultset ]

    @staticmethod
    def orderByString(order, limit, offset):

        def do_order(o):
            if isinstance(o, basestring):
                return o
            return (' ').join(o)

        if not order:
            order = ''
        elif not isinstance(order, basestring):
            order = (', ').join(map(do_order, order))
        if order:
            order = 'ORDER BY %s' % order
        if limit not in ('', None):
            limit = 'LIMIT %s' % limit
        else:
            limit = ''
        if offset not in ('', None):
            offset = 'OFFSET %s' % offset
        else:
            offset = ''
        return (' ').join(filter(None, (order, limit, offset)))

    def getSequence(self, name, field, table):
        """If db has sequences, this should return
        the next value of the sequence named 'name'"""
        pass

    def getAutoIncrement(self, name):
        """If db uses auto increment, should obtain
        the value of the auto-incremented field named 'name'"""
        pass

    def listTables(self, schema=None):
        """list the tables in the database schema"""
        raise NotImplementedError

    def describeTable(self, table, schema=None):
        """for the given table, returns a 2-tuple: a dict of Field objects
        keyed by name, and list of multi-column unique constraints (sets of Fields)).
        The Field instances should contain information about whether they are unique
        or sequenced.
        """
        raise NotImplementedError


_driverConfig = {'mysql': 'pydo.drivers.mysqlconn.MysqlDBI', 'psycopg': 'pydo.drivers.psycopgconn.PsycopgDBI', 'sqlite': 'pydo.drivers.sqliteconn.SqliteDBI', 'mssql': 'pydo.drivers.mssqlconn.MssqlDBI', 'oracle': 'pydo.drivers.oracleconn.OracleDBI'}
_loadedDrivers = {}
_aliases = {}
_connlock = Lock()

def _real_connect(connfunc, connargs, initFunc=None):
    if isinstance(connargs, dict):
        conn = connfunc(**connargs)
    elif isinstance(connargs, tuple):
        conn = connfunc(*connargs)
    else:
        conn = connfunc(connargs)
    if initFunc:
        initFunc(conn)
    return conn


def _connect(driver, connectArgs, pool=None, verbose=False, initFunc=None):
    if isinstance(driver, basestring):
        driver = _get_driver_class(driver)
    return driver(connectArgs, pool, verbose, initFunc)


def _get_driver_class(name):
    if not _loadedDrivers.has_key(name):
        fqcn = _driverConfig[name]
        cls = _import_a_class(fqcn)
        _loadedDrivers[name] = cls
        return cls
    return _loadedDrivers[name]


def initAlias(alias, driver, connectArgs, pool=None, verbose=False, init=None):
    """initializes a connection alias with the stated connection arguments.
    
    It can cause confusion to let this be called repeatedly; you might
    think you are initializing it one way and not realize it is being
    initialized elsewhere differently.  Therefore, this raises a
    ValueError if the alias is already initialized with different
    data.  Multiple initializations with the same data (such as
    happens when a module calling initAlias is reloaded) are permitted.

    If you need to change the connect values at runtime, call delAlias
    before initAlias.
    
    """
    if isinstance(init, basestring):
        sql = init

        def init(conn):
            c = conn.cursor()
            c.execute(sql)
            c.close()

    elif isinstance(init, (list, tuple)):
        for s in init:
            if not isinstance(s, basestring):
                raise ValueError, 'expected string, got %s' % s

        sql = init

        def init(conn):
            c = conn.cursor()
            for s in sql:
                c.execute(s)

            c.close()

    elif init and not callable(init):
        raise ValueError, 'init must be either None, a string, or callable, got %s' % type(init)
    data = dict(driver=driver, connectArgs=connectArgs, pool=pool, verbose=verbose, initFunc=init)
    _connlock.acquire()
    try:
        old = _aliases.get(alias)
        if old:
            old = old.copy()
            old.pop('connection', None)
            if data != old:
                raise ValueError, 'already initialized: %s' % alias
        else:
            _aliases[alias] = data
    finally:
        _connlock.release()
    return


def delAlias(alias):
    """delete a connection alias if it has already been initialized;
    does nothing otherwise"""
    _connlock.acquire()
    try:
        if _aliases.has_key(alias):
            del _aliases[alias]
    finally:
        _connlock.release()


def getConnection(alias, create=True):
    """get a connection given a connection alias"""
    _connlock.acquire()
    try:
        try:
            conndata = _aliases[alias]
        except KeyError:
            raise ValueError, 'alias %s not recognized' % alias

        if not conndata.has_key('connection'):
            if not create:
                return
            res = _connect(**conndata)
            conndata['connection'] = res
            return res
        return conndata['connection']
    finally:
        _connlock.release()
    return


class ConnectionWrapper(object):
    """a connection object returned from a connection pool which wraps
    a real db connection.  It delegates to the real connection, but
    overrides close(), which instead of closing the connection,
    returns the it to the pool.  """
    __module__ = __name__
    __slots__ = ('_conn', '_pool', '_closed')

    def __init__(self, conn, pool):
        self._conn = conn
        self._pool = pool
        self._closed = 0

    def __getattr__(self, attr):
        return getattr(self._conn, attr)

    def __setattr__(self, attr, val):
        if attr in self.__slots__:
            super(ConnectionWrapper, self).__setattr__(attr, val)
        else:
            setattr(self._conn, attr, val)

    def close(self):
        self._pool.release(self._conn)
        self._closed = 1

    def __del__(self):
        if not self._closed:
            self.close()


class ConnectionPool(object):
    """ a connection pool for a single connection alias."""
    __module__ = __name__

    def __init__(self, max_poolsize=0, keep_poolsize=1, delay=0.2, retries=10):
        self._free = deque()
        self._busy = []
        self._max_poolsize = max_poolsize
        self._keep_poolsize = keep_poolsize
        self._delay = delay
        self._retries = retries
        self._lock = Lock()

    def connect(self, connectFunc, connectArgs, initFunc=None):
        return self._connect(connectFunc, connectArgs, initFunc, self._retries)

    def _connect(self, connectFunc, connectArgs, initFunc, retries):
        """internal method; don't call it"""
        max_poolsize = self._max_poolsize
        self._lock.acquire()
        try:
            free = self._free
            busy = self._busy
            if free:
                c = free.popleft()
                busy.append(c)
            else:
                lenbusy = len(busy)
                if max_poolsize > 0:
                    assert lenbusy <= max_poolsize
                    if lenbusy == max_poolsize:
                        if not retries:
                            raise PyDOError, 'all connections in use, attempted retries: %d' % self._retries
                        else:
                            c = None
                    else:
                        c = _real_connect(connectFunc, connectArgs, initFunc)
                        busy.append(c)
                else:
                    c = _real_connect(connectFunc, connectArgs, initFunc)
                    busy.append(c)
        finally:
            self._lock.release()
        if c:
            if self.onHandOut(c):
                return ConnectionWrapper(c, self)
            else:
                busy.remove(c)
                del c
        time.sleep(self._delay)
        return self._connect(connectFunc, connectArgs, initFunc, retries - 1)

    def release(self, conn):
        keep_poolsize = self._keep_poolsize
        self._lock.acquire()
        try:
            free = self._free
            busy = self._busy
            numconns = len(free) + len(busy)
            keep = keep_poolsize >= numconns
            busy.remove(conn)
            if keep:
                free.append(conn)
            self.onRelease(conn)
        finally:
            self._lock.release()

    def onRelease(self, realConn):
        """anything you want to do to a connection when it is returned
        (default: rollback)"""
        try:
            realConn.rollback()
        except:
            pass

    def onHandOut(self, realConn):
        """any test you want to perform on a cached (i.e., not newly
        connected) connection before giving it out.  If the connection
        isn't good, return False"""
        if hasattr(realConn, 'closed'):
            return not realConn.closed
        if hasattr(realConn, 'open'):
            return realConn.open
        return 1


__all__ = [
 'initAlias', 'delAlias', 'getConnection', 'ConnectionPool']