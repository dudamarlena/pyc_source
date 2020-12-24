# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.5-x86_64/egg/graphterm/bin/tornado/platform/posix.py
# Compiled at: 2012-01-17 03:11:13
"""Posix implementations of platform-specific functionality."""
import fcntl, os
from tornado.platform import interface
from tornado.util import b

def set_close_exec(fd):
    flags = fcntl.fcntl(fd, fcntl.F_GETFD)
    fcntl.fcntl(fd, fcntl.F_SETFD, flags | fcntl.FD_CLOEXEC)


def _set_nonblocking(fd):
    flags = fcntl.fcntl(fd, fcntl.F_GETFL)
    fcntl.fcntl(fd, fcntl.F_SETFL, flags | os.O_NONBLOCK)


class Waker(interface.Waker):

    def __init__(self):
        r, w = os.pipe()
        _set_nonblocking(r)
        _set_nonblocking(w)
        set_close_exec(r)
        set_close_exec(w)
        self.reader = os.fdopen(r, 'rb', 0)
        self.writer = os.fdopen(w, 'wb', 0)

    def fileno(self):
        return self.reader.fileno()

    def wake(self):
        try:
            self.writer.write(b('x'))
        except IOError:
            pass

    def consume(self):
        try:
            while True:
                result = self.reader.read()
                if not result:
                    break

        except IOError:
            pass

    def close(self):
        self.reader.close()
        self.writer.close()