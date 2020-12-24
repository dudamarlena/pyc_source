# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/travis/build/quantmind/pulsar-odm/odm/dialects/postgresql/green.py
# Compiled at: 2017-11-24 06:00:10
# Size of source mod 2**32: 2558 bytes
from asyncio import Future
from greenlet import getcurrent
import psycopg2
from psycopg2 import *
from psycopg2 import extensions, OperationalError
__version__ = psycopg2.__version__

def psycopg2_wait_callback(conn):
    """A wait callback to allow greenlet to work with Psycopg.
    The caller must be from a greenlet other than the main one.

    :param conn: psycopg2 connection or file number

    This function must be invoked from a coroutine with parent, therefore
    invoking it from the main greenlet will raise an exception.
    """
    while True:
        state = conn.poll()
        if state == extensions.POLL_OK:
            break
        else:
            if state == extensions.POLL_READ:
                _wait_fd(conn)
            else:
                if state == extensions.POLL_WRITE:
                    _wait_fd(conn, read=False)
                else:
                    raise OperationalError('Bad result from poll: %r' % state)


def _wait_fd(conn, read=True):
    """Wait for an event on file descriptor ``fd``.

    :param conn: file descriptor
    :param read: wait for a read event if ``True``, otherwise a wait
        for write event.

    This function must be invoked from a coroutine with parent, therefore
    invoking it from the main greenlet will raise an exception.
    """
    current = getcurrent()
    parent = current.parent
    if not parent:
        raise AssertionError('"_wait_fd" must be called by greenlet with a parent')
    else:
        try:
            fileno = conn.fileno()
        except AttributeError:
            fileno = conn

        future = Future()
        if read:
            future._loop.add_reader(fileno, _done_wait_fd, fileno, future, read)
        else:
            future._loop.add_writer(fileno, _done_wait_fd, fileno, future, read)
    parent.switch(future)
    future.result()


def _done_wait_fd(fd, future, read):
    try:
        if read:
            future._loop.remove_reader(fd)
        else:
            future._loop.remove_writer(fd)
    except Exception as exc:
        future.set_exception(exc)
    else:
        future.set_result(None)


try:
    extensions.POLL_OK
except AttributeError:
    from pulsar import ImproperlyConfigured
    raise ImproperlyConfigured('Psycopg2 does not have support for asynchronous connections. You need at least version 2.2.0 of Psycopg2.')

extensions.set_wait_callback(psycopg2_wait_callback)