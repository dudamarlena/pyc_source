# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/wgzhao/Codes/easybase/py3/lib/python3.7/site-packages/easybase/pool.py
# Compiled at: 2019-09-10 23:04:16
# Size of source mod 2**32: 5436 bytes
"""
EasyBase connection pool module.
"""
import contextlib, logging
from six.moves import queue, range, xrange
import socket, threading
from thriftpy2.thrift import TException
from .connection import Connection
logger = logging.getLogger(__name__)

class NoConnectionsAvailable(RuntimeError):
    __doc__ = '\n    Exception raised when no connections are available.\n\n    This happens if a timeout was specified when obtaining a connection,\n    and no connection became available within the specified timeout.\n\n    .. versionadded:: 0.5\n    '


class ConnectionPool(object):
    __doc__ = '\n    Thread-safe connection pool.\n\n    .. versionadded:: 0.5\n\n    The `size` argument specifies how many connections this pool\n    manages. Additional keyword arguments are passed unmodified to the\n    :py:class:`easybase.Connection` constructor, with the exception of\n    the `autoconnect` argument, since maintaining connections is the\n    task of the pool.\n\n    :param int size: the maximum number of concurrently open connections\n    :param kwargs: keyword arguments passed to\n                   :py:class:`easybase.Connection`\n    '

    def __init__(self, size, **kwargs):
        if not isinstance(size, int):
            raise TypeError("Pool 'size' arg must be an integer")
        if not size > 0:
            raise ValueError("Pool 'size' arg must be greater than zero")
        logger.debug('Initializing connection pool with %d connections', size)
        self._lock = threading.Lock()
        self._queue = queue.LifoQueue(maxsize=size)
        self._thread_connections = threading.local()
        connection_kwargs = kwargs
        connection_kwargs['autoconnect'] = False
        for i in xrange(size):
            connection = Connection(**connection_kwargs)
            self._queue.put(connection)

        with self.connection():
            pass

    def _acquire_connection(self, timeout=None):
        """Acquire a connection from the pool."""
        try:
            return self._queue.get(True, timeout)
        except queue.Empty:
            raise NoConnectionsAvailable('No connection available from pool within specified timeout')

    def _return_connection(self, connection):
        """Return a connection to the pool."""
        self._queue.put(connection)

    @contextlib.contextmanager
    def connection(self, timeout=None):
        """
        Obtain a connection from the pool.

        This method *must* be used as a context manager, i.e. with
        Python's ``with`` block. Example::

            with pool.connection() as connection:
                pass  # do something with the connection

        If `timeout` is specified, this is the number of seconds to wait
        for a connection to become available before
        :py:exc:`NoConnectionsAvailable` is raised. If omitted, this
        method waits forever for a connection to become available.

        :param int timeout: number of seconds to wait (optional)
        :return: active connection from the pool
        :rtype: :py:class:`easybase.Connection`
        """
        connection = getattr(self._thread_connections, 'current', None)
        return_after_use = False
        if connection is None:
            return_after_use = True
            connection = self._acquire_connection(timeout)
            with self._lock:
                self._thread_connections.current = connection
        try:
            try:
                connection.open()
                yield connection
            except (TException, socket.error):
                logger.info('Replacing tainted pool connection')
                connection._refresh_thrift_client()
                connection.open()
                raise

        finally:
            if return_after_use:
                del self._thread_connections.current
                self._return_connection(connection)