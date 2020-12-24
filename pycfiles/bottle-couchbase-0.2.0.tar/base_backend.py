# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /home/fede/newhome/projects/bottle-cork/tests/cork/base_backend.py
# Compiled at: 2015-04-12 07:32:09
__doc__ = '\n.. module:: backend.py\n   :synopsis: Base Backend.\n'

class BackendIOException(Exception):
    """Generic Backend I/O Exception"""


def ni(*args, **kwargs):
    raise NotImplementedError


class Backend(object):
    """Base Backend class - to be subclassed by real backends."""
    save_users = ni
    save_roles = ni
    save_pending_registrations = ni


class Table(object):
    """Base Table class - to be subclassed by real backends."""
    __len__ = ni
    __contains__ = ni
    __setitem__ = ni
    __getitem__ = ni
    __iter__ = ni
    iteritems = ni