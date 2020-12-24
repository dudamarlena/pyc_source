# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\henrio\bases.py
# Compiled at: 2017-10-24 23:20:15
# Size of source mod 2**32: 1732 bytes
__all__ = [
 'AbstractLoop', 'AbstractProtocol', 'IOBase', 'BaseSocket', 'BaseFile']

class AbstractLoop:

    def time(self):
        raise NotImplementedError

    def sleep(self, time):
        raise NotImplementedError

    def run_forever(self):
        raise NotImplementedError

    def run_until_complete(self, coro):
        raise NotImplementedError

    def close(self):
        raise NotImplementedError

    def create_task(self, coro):
        raise NotImplementedError

    def register_reader(self, file, callback, *args):
        raise NotImplementedError

    def register_writer(self, file, callback, *args):
        raise NotImplementedError

    def unregister_reader(self, fileobj):
        raise NotImplementedError

    def unregister_writer(self, fileobj):
        raise NotImplementedError

    def wrap_file(self, file):
        raise NotImplementedError

    def wrap_socket(self, socket):
        raise NotImplementedError

    def _poll(self):
        raise NotImplementedError


class IOBase:
    file = None

    def fileno(self):
        raise NotImplementedError

    def close(self):
        raise NotImplementedError


class BaseFile(IOBase):

    async def read(self, nbytes):
        raise NotImplementedError

    async def write(self, nbytes):
        raise NotImplementedError


class BaseSocket(IOBase):

    async def recv(self, nbytes):
        raise NotImplementedError

    async def send(self, data):
        raise NotImplementedError


class AbstractProtocol:

    async def data_received(self, data):
        raise NotImplementedError

    async def connection_lost(self, exc):
        raise NotImplementedError