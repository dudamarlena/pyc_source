# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.4-x86_64/egg/sniorfy/interface.py
# Compiled at: 2012-04-26 20:48:40
"""Interfaces for platform-specific functionality.

This module exists primarily for documentation purposes and as base classes
for other tornado.platform modules.  Most code should import the appropriate
implementation from `tornado.platform.auto`.
"""
from __future__ import absolute_import, division, with_statement

def set_close_exec(fd):
    """Sets the close-on-exec bit (``FD_CLOEXEC``)for a file descriptor."""
    raise NotImplementedError()


class Waker(object):
    """A socket-like object that can wake another thread from ``select()``.

    The `~tornado.ioloop.IOLoop` will add the Waker's `fileno()` to
    its ``select`` (or ``epoll`` or ``kqueue``) calls.  When another
    thread wants to wake up the loop, it calls `wake`.  Once it has woken
    up, it will call `consume` to do any necessary per-wake cleanup.  When
    the ``IOLoop`` is closed, it closes its waker too.
    """

    def fileno(self):
        """Returns a file descriptor for this waker.

        Must be suitable for use with ``select()`` or equivalent on the
        local platform.
        """
        raise NotImplementedError()

    def wake(self):
        """Triggers activity on the waker's file descriptor."""
        raise NotImplementedError()

    def consume(self):
        """Called after the listen has woken up to do any necessary cleanup."""
        raise NotImplementedError()

    def close(self):
        """Closes the waker's file descriptor(s)."""
        raise NotImplementedError()