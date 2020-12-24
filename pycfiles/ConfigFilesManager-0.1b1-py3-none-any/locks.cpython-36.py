# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /usr/local/lib/python3.6/dist-packages/configfiles/repo/locks.py
# Compiled at: 2018-11-05 09:00:56
# Size of source mod 2**32: 2381 bytes
__doc__ = '\nImplements the locking functionality of repositories\n'
from paramiko.transport import Transport
from ..auth import authenticate_transport, interpret_urlish
from socket import socket

class RepoReadLock:

    def __init__(self, url):
        self.url = url
        self.transport = None
        self.client = None
        self.socket = None
        self.i = 0

    def __enter__(self):
        self.socket = socket()
        self.socket.connect((interpret_urlish(self.url)[1], 22))
        self.transport = Transport(self.socket)
        self.transport.start_client()
        authenticate_transport(self.transport)
        self.client = self.transport.open_sftp_client()
        self.client.chdir(interpret_urlish(self.url)[2])
        self._lock()

    def _lock(self):
        target_locks = self.client.listdir('locks')
        target_locks.sort()
        if 'write_lock' in target_locks:
            raise RuntimeError('repo is write locked; try again later')
        else:
            self.i = 0
            while 'read_lock_' + str(self.i) in target_locks:
                self.i += 1

            self.client.mkdir('locks/read_lock_' + str(self.i))

    def _unlock(self):
        self.client.rmdir('locks/read_lock_' + str(self.i))

    def __exit__(self, *args):
        self._unlock()
        self.client.close()
        self.transport.close()
        self.socket.close()


class RepoWriteLock:

    def __init__(self, url):
        self.url = url
        self.transport = None
        self.client = None
        self.socket = socket()

    def __enter__(self):
        self.socket.connect((interpret_urlish(self.url)[1], 22))
        self.transport = Transport(self.socket)
        self.transport.start_client()
        authenticate_transport(self.transport)
        self.client = self.transport.open_sftp_client()
        self.client.chdir(interpret_urlish(self.url)[2])
        self._lock()

    def _lock(self):
        target_locks = self.client.listdir('locks')
        target_locks.sort()
        if target_locks:
            raise RuntimeError('repo is locked; try again later')
        else:
            self.client.mkdir('locks/write_lock')

    def _unlock(self):
        self.client.rmdir('locks/write_lock')

    def __exit__(self, *args):
        self._unlock()
        self.client.close()
        self.transport.close()
        self.socket.close()