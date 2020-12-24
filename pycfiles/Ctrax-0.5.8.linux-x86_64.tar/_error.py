# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python2.7/dist-packages/psutil/_error.py
# Compiled at: 2013-09-24 00:55:57
"""psutil exception classes.
Not supposed to be used / imported directly.
Instead use psutil.NoSuchProcess, etc.
"""

class Error(Exception):
    """Base exception class. All other psutil exceptions inherit
    from this one.
    """
    pass


class NoSuchProcess(Error):
    """Exception raised when a process with a certain PID doesn't
    or no longer exists (zombie).
    """

    def __init__(self, pid, name=None, msg=None):
        self.pid = pid
        self.name = name
        self.msg = msg
        if msg is None:
            if name:
                details = '(pid=%s, name=%s)' % (self.pid, repr(self.name))
            else:
                details = '(pid=%s)' % self.pid
            self.msg = 'process no longer exists ' + details
        return

    def __str__(self):
        return self.msg


class AccessDenied(Error):
    """Exception raised when permission to perform an action is denied."""

    def __init__(self, pid=None, name=None, msg=None):
        self.pid = pid
        self.name = name
        self.msg = msg
        if msg is None:
            if pid is not None and name is not None:
                self.msg = '(pid=%s, name=%s)' % (pid, repr(name))
            elif pid is not None:
                self.msg = '(pid=%s)' % self.pid
            else:
                self.msg = ''
        return

    def __str__(self):
        return self.msg


class TimeoutExpired(Error):
    """Raised on Process.wait(timeout) if timeout expires and process
    is still alive.
    """

    def __init__(self, pid=None, name=None):
        self.pid = pid
        self.name = name
        if pid is not None and name is not None:
            self.msg = '(pid=%s, name=%s)' % (pid, repr(name))
        elif pid is not None:
            self.msg = '(pid=%s)' % self.pid
        else:
            self.msg = ''
        return

    def __str__(self):
        return self.msg