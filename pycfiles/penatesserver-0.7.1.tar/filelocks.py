# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/mgallet/Github/Penates-Server/penatesserver/filelocks.py
# Compiled at: 2015-12-29 03:07:09
from __future__ import unicode_literals
import os, time, errno
__author__ = b'mgallet'

class Lock(object):
    """Lock interprocess basé sur des fichiers

    :param filename: name of the lock file
    """

    def __init__(self, filename):
        self.filename = filename
        self.acquired = False

    def acquire(self, blocking=True, timeout=-1):
        """Acquire a lock, blocking or non-blocking.
        When invoked with the blocking argument set to True (the default), block until the lock is unlocked,
            then set it to locked and return True.

        When invoked with the blocking argument set to False, do not block. If a call with blocking set to True would
            block, return False immediately; otherwise, set the lock to locked and return True.

        When invoked with the floating-point timeout argument set to a positive value, block for at most the number of
            seconds specified by timeout and as long as the lock cannot be acquired. A timeout argument of -1 specifies
             an unbounded wait. It is forbidden to specify a timeout when blocking is false.

        The return value is True if the lock is acquired successfully, False if not (for example if the timeout
            expired).

        :param blocking:
        :param timeout:
        :return: :raise:
        """
        start = time.time()
        if self.acquired:
            return True
        while True:
            try:
                os.open(self.filename, os.O_CREAT | os.O_EXCL | os.O_WRONLY)
                self.acquired = True
                return True
            except OSError as e:
                if e.errno == errno.EEXIST:
                    if not blocking:
                        return False
                    if -1 < timeout < time.time() - start:
                        return False
                    time.sleep(0.2)
                else:
                    raise

    def __enter__(self):
        self.acquire()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.release()

    def release(self):
        """Release a lock. This can be called from any thread, not only the thread which has acquired the lock.

        When the lock is locked, reset it to unlocked, and return. If any other threads are blocked waiting for the
        lock to become unlocked, allow exactly one of them to proceed.
        When invoked on an unlocked lock, a RuntimeError is raised.
        There is no return value.

        :raise RuntimeError:
        """
        if not self.acquired:
            raise RuntimeError
        os.remove(self.filename)
        self.acquired = False