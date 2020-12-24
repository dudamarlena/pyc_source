# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python2.7/dist-packages/inotify/__init__.py
# Compiled at: 2013-07-23 10:21:39
"""Low-level interface to the Linux inotify subsystem.

The inotify subsystem provides an efficient mechanism for file status
monitoring and change notification.

This package provides the low-level inotify system call interface and
associated constants and helper functions.

For a higher-level interface that remains highly efficient, use the
inotify.watcher package."""
__author__ = "Bryan O'Sullivan <bos@serpentine.com>"
from ._inotify import *
procfs_path = '/proc/sys/fs/inotify'

def _read_procfs_value(name):

    def read_value():
        try:
            return int(open(procfs_path + '/' + name).read())
        except OSError as err:
            return

        return

    read_value.__doc__ = 'Return the value of the %s setting from /proc.\n\n    If inotify is not enabled on this system, return None.' % name
    return read_value


max_queued_events = _read_procfs_value('max_queued_events')
max_user_instances = _read_procfs_value('max_user_instances')
max_user_watches = _read_procfs_value('max_user_watches')