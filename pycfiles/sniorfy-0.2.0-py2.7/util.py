# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.4-x86_64/egg/sniorfy/util.py
# Compiled at: 2012-04-26 20:48:40
"""Miscellaneous utility functions."""
from __future__ import absolute_import, division, with_statement

class ObjectDict(dict):
    """Makes a dictionary behave like an object."""

    def __getattr__(self, name):
        try:
            return self[name]
        except KeyError:
            raise AttributeError(name)

    def __setattr__(self, name, value):
        self[name] = value


def import_object(name):
    """Imports an object by name.

    import_object('x.y.z') is equivalent to 'from x.y import z'.

    >>> import tornado.escape
    >>> import_object('tornado.escape') is tornado.escape
    True
    >>> import_object('tornado.escape.utf8') is tornado.escape.utf8
    True
    """
    parts = name.split('.')
    obj = __import__(('.').join(parts[:-1]), None, None, [parts[(-1)]], 0)
    return getattr(obj, parts[(-1)])


if str is unicode:

    def b(s):
        return s.encode('latin1')


    bytes_type = bytes
else:

    def b(s):
        return s


    bytes_type = str

def doctests():
    import doctest
    return doctest.DocTestSuite()