# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/fede/newhome/projects/bottle-cork/tests/cork/base_backend.py
# Compiled at: 2015-04-12 07:32:09
"""
.. module:: backend.py
   :synopsis: Base Backend.
"""

class BackendIOException(Exception):
    """Generic Backend I/O Exception"""
    pass


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