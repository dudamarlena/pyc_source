# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/riopg/connection.py
# Compiled at: 2018-09-23 13:57:48
# Size of source mod 2**32: 4368 bytes
"""
.. currentmodule:: riopg.connection
"""
import socket, inspect, multio
from psycopg2 import OperationalError, connect
from psycopg2._psycopg import connection
from psycopg2.extensions import POLL_ERROR, POLL_OK, POLL_READ, POLL_WRITE
from riopg import cursor as md_cursor

class Connection(object):
    __doc__ = '\n    Wraps a :class:`psycopg2.Connection` object, making it work with an async library.\n\n    Do not construct this object manually; use :meth:`.Connection.open` or :meth:`.Pool.acquire`.\n    '

    def __init__(self):
        self._connection = None
        self._sock = None
        self._lock = multio.Lock()

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.close()
        return False

    def __getattr__(self, item):
        original = getattr(self._connection, item)
        if not callable(original):
            return original
        else:

            def wrapper(s, fn):

                def wrapped(*args, **kwargs):
                    return (s._do_async)(fn, *args, **kwargs)

                return wrapped

            return wrapper(self, original)

    @classmethod
    async def open(cls, *args, **kwargs) -> 'Connection':
        """
        Opens a new connection.
        """
        conn = cls()
        await (conn._connect)(*args, **kwargs)
        return conn

    async def _wait_callback(self):
        """
        The wait callback. This callback is used for polling the psycopg2 sockets, waiting until
        they are ready.
        """
        while 1:
            state = self._connection.poll()
            if state == POLL_OK:
                return
            if state == POLL_READ:
                await multio.asynclib.wait_read(self._sock)
            else:
                if state == POLL_WRITE:
                    await multio.asynclib.wait_write(self._sock)
                else:
                    if state == POLL_ERROR:
                        raise OperationalError('Polling socket returned error')

    async def _do_async(self, fn, *args):
        """
        Performs a psycopg2 action asynchronously, using the wait callback.
        """
        async with self._lock:
            res = fn(*args)
            if inspect.isawaitable(res):
                res = await res
            await self._wait_callback()
        return res

    async def _connect(self, dsn: str):
        """
        Connects the psycopg2 connection.

        :param dsn: The DSN to connect with.
        """
        self._connection = connect(dsn, async_=True)
        self._sock = socket.fromfd(self._connection.fileno(), socket.AF_INET, socket.SOCK_STREAM)
        await self._wait_callback()

    def _cursor(self, **kwargs):
        """
        Internal implementation of acquiring a cursor.
        """
        return (self._connection.cursor)(**kwargs)

    async def cursor(self, **kwargs) -> 'md_cursor.Cursor':
        """
        Gets a new cursor object.

        :return: A :class:`.cursor.Cursor` object attached to this connection.
        """
        cur = md_cursor.Cursor(self, kwargs)
        await cur.open()
        return cur

    async def close(self):
        """
        Closes this connection.
        """
        self._connection.close()