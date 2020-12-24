# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\henrio\windows.py
# Compiled at: 2017-12-18 18:35:18
# Size of source mod 2**32: 4846 bytes
import _overlapped
from _winapi import NULL, INFINITE, CloseHandle
from collections import deque
from . import BaseLoop, Future, BaseFile, BaseSocket
__all__ = [
 'IOCPLoop', 'IOCPSocket', 'IOCPInstance', 'IOCPFile']
ERROR_CONNECTION_REFUSED = 1225
ERROR_CONNECTION_ABORTED = 1236

class IOCPLoop(BaseLoop):

    def __init__(self, concurrency=INFINITE):
        super().__init__()
        self._port = _overlapped.CreateIoCompletionPort(_overlapped.INVALID_HANDLE_VALUE, NULL, 0, concurrency)
        self._current_iocp = dict()
        self._open_ports = list()

    def _poll(self):
        if self._current_iocp:
            if not self._tasks or self._queue:
                if self._timers:
                    ms = max(100, (self._timers[0][0] - self.time()) * 1000)
                else:
                    ms = 100
            else:
                ms = 100
            while True:
                status = _overlapped.GetQueuedCompletionStatus(self._port, ms)
                if status is None:
                    break
                ms = 0
                err, transferred, key, address = status
                try:
                    future = self._current_iocp.pop(address)
                    if isinstance(future, IOCPInstance):
                        future._io_ready(address, transferred)
                    else:
                        if isinstance(future, Future):
                            future.set_result(transferred)
                except KeyError:
                    if key not in (0, _overlapped.INVALID_HANDLE_VALUE):
                        CloseHandle(key)
                    continue

        elif self._timers:
            self.sleep(max(0, self._timers[0][0] - self.time()))

    def wrap_channel(self, wrapper, channel):
        wrapped = wrapper(channel, self)
        self._open_ports.append(channel.fileno())
        _overlapped.CreateIoCompletionPort(channel.fileno(), self._port, 0, 0)
        return wrapped

    def wrap_file(self, file) -> 'IOCPFile':
        """Wrap a file in an async file API."""
        return self.wrap_channel(IOCPFile, file)

    def wrap_socket(self, socket) -> 'IOCPSocket':
        """Wrap a file in an async socket API."""
        return self.wrap_channel(IOCPSocket, socket)

    def unwrap_file(self, file):
        if file.fileno not in (0, _overlapped.INVALID_HANDLE_VALUE):
            CloseHandle(file.fileno())
        del self._current_iocp[file._overlap.overlap.address]


class IOCPInstance:

    def __init__(self, file, loop):
        self.file = file
        self._readqueue = deque()
        self._writequeue = deque()
        self._loop = loop
        self._queue = dict()

    def _io_ready(self, key, data):
        _type, fut, _data = self._queue.pop(key)
        fut.set_result(data)

    def close(self):
        try:
            if self.file.fileno not in (0, _overlapped.INVALID_HANDLE_VALUE):
                CloseHandle(self.file.fileno())
        finally:
            self.file.close()

    @property
    def fileno(self):
        return self.file.fileno()


class IOCPFile(BaseFile, IOCPInstance):

    def write(self, data):
        ov = _overlapped.Overlapped(NULL)
        ov.WriteFile(self.file.fileno(), data)
        fut = Future()
        self._queue[ov.address] = (0, fut, data)
        self._loop._current_iocp[ov.address] = self
        return fut

    async def read(self, nbytes):
        ov = _overlapped.Overlapped(NULL)
        ov.ReadFile(self.file.fileno(), nbytes)
        fut = Future()
        self._queue[ov.address] = (0, fut, nbytes)
        self._loop._current_iocp[ov.address] = self
        await fut
        return self.file.read(nbytes)


class IOCPSocket(BaseSocket, IOCPInstance):

    def send(self, data, flags=0):
        ov = _overlapped.Overlapped(NULL)
        ov.WSASend(self.file.fileno(), data, flags)
        fut = Future()
        self._queue[ov.address] = (0, fut, data)
        self._loop._current_iocp[ov.address] = self
        return fut

    async def recv(self, nbytes, flags=0):
        ov = _overlapped.Overlapped(NULL)
        ov.WSARecv(self.file.fileno(), nbytes, flags)
        fut = Future()
        self._queue[ov.address] = (1, fut, nbytes)
        self._loop._current_iocp[ov.address] = self
        await fut
        return self.file.recv(nbytes)