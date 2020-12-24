# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /home/travis/build/quantmind/pulsar-odm/odm/dialects/postgresql/pool.py
# Compiled at: 2017-11-24 06:00:10
# Size of source mod 2**32: 2260 bytes
from sqlalchemy import pool
from pulsar.apps.greenio import GreenLock

class GreenletPool(pool.Pool):
    """GreenletPool"""

    def __init__(self, creator, pool_size=10, timeout=30, **kw):
        (super().__init__)(creator, **kw)
        self._lock = GreenLock()
        self._max_size = pool_size
        self._timeout = timeout
        self._connections = set()
        self._available_connections = set()

    def dispose(self):
        for conn in self._connections:
            try:
                conn.close()
            except Exception:
                pass

        self.logger.info('Pool disposed. %s', self.status())

    def status(self):
        return 'size: %d, available: %d' % (self.size(),
         len(self._available_connections))

    def size(self):
        return len(self._connections)

    def max_size(self):
        return self._max_size

    def timeout(self):
        return self._timeout

    def recreate(self):
        self.logger.info('Pool recreating')
        return self.__class__((self._creator), pool_size=(self.max_size),
          recycle=(self._recycle),
          echo=(self.echo),
          logging_name=(self._orig_logging_name),
          use_threadlocal=(self._use_threadlocal),
          reset_on_return=(self._reset_on_return),
          _dispatch=(self.dispatch),
          dialect=(self._dialect))

    def _do_return_conn(self, conn):
        self._available_connections.add(conn)

    def _do_get(self):
        try:
            return self._available_connections.pop()
        except KeyError:
            pass

        with self._lock:
            conn = self._create_connection()
            self._connections.add(conn)
            return conn