# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/paste/webkit/FakeWebware/MiscUtils/DBPool.py
# Compiled at: 2006-10-22 17:01:01
"""
DBPool.py

Implements a pool of cached connections to a database. This should result in
a speedup for persistent apps. The pool of connections is threadsafe
regardless of whether the DB API module question in general has a
threadsafety of 1 or 2.

For more information on the DB API, see:
        http://www.python.org/topics/database/DatabaseAPI-2.0.html

The idea behind DBPool is that it's completely seamless, so once you have
established your connection, use it just as you would any other DB-API
compliant module. For example:

        dbPool = DBPool(MySQLdb, 5, host=xxx, user=xxx, ...)
        db = dbPool.getConnection()

Now use "db" exactly as if it were a MySQLdb connection. It's really
just a proxy class.

db.close() will return the connection to the pool, not actually
close it. This is so your existing code works nicely.

FUTURE

* If in the presence of WebKit, register ourselves as a Can.

CREDIT

* Contributed by Dan Green
* thread safety bug found by Tom Schwaller
* Fixes by Geoff Talvola (thread safety in _threadsafe_getConnection()).
* Clean up by Chuck Esterbrook.
* Fix unthreadsafe functions which were leaking, Jay Love
* Eli Green's webware-discuss comments were lifted for additional docs.
"""
import threading

class DBPoolError(Exception):
    __module__ = __name__


class UnsupportedError(DBPoolError):
    __module__ = __name__


class PooledConnection:
    """ A wrapper for database connections to help with DBPool. You don't normally deal with this class directly, but use DBPool to get new connections. """
    __module__ = __name__

    def __init__(self, pool, con):
        self._con = con
        self._pool = pool

    def close(self):
        if self._con is not None:
            self._pool.returnConnection(self)
            self._con = None
        return

    def __getattr__(self, name):
        return getattr(self._con, name)

    def __del__(self):
        self.close()


class DBPool:
    __module__ = __name__

    def __init__(self, dbModule, maxConnections, *args, **kwargs):
        if dbModule.threadsafety == 0:
            raise UnsupportedError, 'Database module does not support any level of threading.'
        elif dbModule.threadsafety == 1:
            from Queue import Queue
            self._queue = Queue(maxConnections)
            self.addConnection = self._unthreadsafe_addConnection
            self.getConnection = self._unthreadsafe_getConnection
            self.returnConnection = self._unthreadsafe_returnConnection
        elif dbModule.threadsafety >= 2:
            self._lock = threading.Lock()
            self._nextCon = 0
            self._connections = []
            self.addConnection = self._threadsafe_addConnection
            self.getConnection = self._threadsafe_getConnection
            self.returnConnection = self._threadsafe_returnConnection
        for i in range(maxConnections):
            con = apply(dbModule.connect, args, kwargs)
            self.addConnection(con)

    def _threadsafe_addConnection(self, con):
        self._connections.append(con)

    def _threadsafe_getConnection(self):
        self._lock.acquire()
        try:
            con = PooledConnection(self, self._connections[self._nextCon])
            self._nextCon = self._nextCon + 1
            if self._nextCon >= len(self._connections):
                self._nextCon = 0
            return con
        finally:
            self._lock.release()

    def _threadsafe_returnConnection(self, con):
        pass

    def _unthreadsafe_addConnection(self, con):
        self._queue.put(con)

    def _unthreadsafe_getConnection(self):
        return PooledConnection(self, self._queue.get())

    def _unthreadsafe_returnConnection(self, conpool):
        """
                This should never be called explicitly outside of this module.
                """
        self.addConnection(conpool._con)