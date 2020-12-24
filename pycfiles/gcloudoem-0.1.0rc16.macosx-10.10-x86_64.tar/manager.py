# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/rstuart/.pyenv/versions/gcloudoem/lib/python2.7/site-packages/gcloudoem/queryset/manager.py
# Compiled at: 2015-04-20 22:18:08
from __future__ import absolute_import, division, print_function, unicode_literals
from functools import partial
from . import QuerySet

class QuerySetManager(object):
    """
    The default QuerySet Manager.

    Custom QuerySet Manager functions can extend this class and users can add extra queryset functionality.  Any custom
    manager methods must accept a :class:`~gcloudoem.entity.Entity` class as its first argument, and a
    :class:`~gcloudoem.queryset.QuerySet` as its second argument.

    The queryset_func function should return a :class:`~gcloudoem.queryset.QuerySet`, probably the same one that was
    passed in, but modified in some way.
    """
    get_queryset = None
    default = QuerySet

    def __init__(self, queryset_func=None):
        if queryset_func:
            self.get_queryset = queryset_func

    def __get__(self, instance, owner):
        """Descriptor for instantiating a new QuerySet object when Entity.objects is accessed."""
        if instance is not None:
            return self
        else:
            queryset_class = owner._meta.queryset_class or self.default
            queryset = queryset_class(owner)
            if self.get_queryset:
                arg_count = self.get_queryset.func_code.co_argcount
                if arg_count == 1:
                    queryset = self.get_queryset(queryset)
                elif arg_count == 2:
                    queryset = self.get_queryset(owner, queryset)
                else:
                    queryset = partial(self.get_queryset, owner, queryset)
            return queryset


def queryset_manager(func):
    """
    Decorator that allows you to define custom QuerySet managers on :class:`~gcloudoem.entity.Entity` classes. The
    manager must be a function that accepts a :class:`~gcloudoem.entity.Entity` class as its first argument, and a
    :class:`~gcloudoem.queryset.QuerySet` as its second argument. The method function should return a
    :class:`~gcloudoem.queryset.QuerySet`, probably the same one that was passed in, but modified in some way.
    """
    return QuerySetManager(func)