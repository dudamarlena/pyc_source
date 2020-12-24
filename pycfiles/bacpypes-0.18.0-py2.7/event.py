# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/bacpypes/event.py
# Compiled at: 2016-10-06 14:34:19
"""
Event
"""
import asyncore, os, select
from .debugging import Logging, bacpypes_debugging, ModuleLogger
_debug = 0
_log = ModuleLogger(globals())

@bacpypes_debugging
class WaitableEvent(asyncore.file_dispatcher, Logging):

    def __init__(self):
        if _debug:
            WaitableEvent._debug('__init__')
        self._read_fd, self._write_fd = os.pipe()
        asyncore.file_dispatcher.__init__(self, self._read_fd)

    def __del__(self):
        if _debug:
            WaitableEvent._debug('__del__')
        os.close(self._read_fd)
        os.close(self._write_fd)

    def readable(self):
        return True

    def writable(self):
        return False

    def handle_read(self):
        if _debug:
            WaitableEvent._debug('handle_read')

    def handle_write(self):
        if _debug:
            WaitableEvent._debug('handle_write')

    def handle_close(self):
        if _debug:
            WaitableEvent._debug('handle_close')
        self.close()

    def wait(self, timeout=None):
        rfds, wfds, efds = select.select([self._read_fd], [], [], timeout)
        return self._read_fd in rfds

    def isSet(self):
        return self.wait(0)

    def set(self):
        if _debug:
            WaitableEvent._debug('set')
        if not self.isSet():
            os.write(self._write_fd, '1')

    def clear(self):
        if _debug:
            WaitableEvent._debug('clear')
        if self.isSet():
            os.read(self._read_fd, 1)