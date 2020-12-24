# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.8-intel/egg/marrow/util/events.py
# Compiled at: 2012-07-26 02:07:58
import os, select
from marrow.util.pipe import pipe
__all__ = [
 'WaitableEvent']

class WaitableEvent(object):
    """Provides an abstract object that can be used to resume select loops with
    indefinite waits from another thread or process. This mimics the standard
    threading.Event interface.
    
    Adapted from:
    http://code.activestate.com/recipes/498191-waitable-cross-process-threadingevent-class/
    """

    def __init__(self):
        self._read_fd, self._write_fd = pipe()

    def wait(self, timeout=None):
        rfds, wfds, efds = select.select([self._read_fd], [], [], timeout)
        return self._read_fd in rfds

    def isSet(self):
        return self.wait(0)

    def clear(self):
        if self.isSet():
            os.read(self._read_fd, 1)

    def set(self):
        if not self.isSet():
            os.write(self._write_fd, '1')

    def fileno(self):
        """Return the FD number of the read side of the pipe, allows this object to
        be used with select.select()."""
        return self._read_fd

    def close(self):
        os.close(self._read_fd)
        os.close(self._write_fd)