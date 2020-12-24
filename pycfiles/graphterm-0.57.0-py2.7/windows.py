# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.5-x86_64/egg/graphterm/bin/tornado/platform/windows.py
# Compiled at: 2012-01-17 03:11:13
import ctypes, ctypes.wintypes, socket, errno
from tornado.platform import interface
from tornado.util import b
SetHandleInformation = ctypes.windll.kernel32.SetHandleInformation
SetHandleInformation.argtypes = (ctypes.wintypes.HANDLE, ctypes.wintypes.DWORD, ctypes.wintypes.DWORD)
SetHandleInformation.restype = ctypes.wintypes.BOOL
HANDLE_FLAG_INHERIT = 1

def set_close_exec(fd):
    success = SetHandleInformation(fd, HANDLE_FLAG_INHERIT, 0)
    if not success:
        raise ctypes.GetLastError()


class Waker(interface.Waker):
    """Create an OS independent asynchronous pipe"""

    def __init__(self):
        self.writer = socket.socket()
        self.writer.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
        count = 0
        while 1:
            count += 1
            a = socket.socket()
            a.bind(('127.0.0.1', 0))
            connect_address = a.getsockname()
            a.listen(1)
            try:
                self.writer.connect(connect_address)
                break
            except socket.error as detail:
                if detail[0] != errno.WSAEADDRINUSE:
                    raise
                if count >= 10:
                    a.close()
                    self.writer.close()
                    raise socket.error('Cannot bind trigger!')
                a.close()

        self.reader, addr = a.accept()
        self.reader.setblocking(0)
        self.writer.setblocking(0)
        a.close()
        self.reader_fd = self.reader.fileno()

    def fileno(self):
        return self.reader.fileno()

    def wake(self):
        try:
            self.writer.send(b('x'))
        except IOError:
            pass

    def consume(self):
        try:
            while True:
                result = self.reader.recv(1024)
                if not result:
                    break

        except IOError:
            pass

    def close(self):
        self.reader.close()
        self.writer.close()