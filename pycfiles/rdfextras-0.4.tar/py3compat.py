# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/grimnes/projects/rdflib/rdfextras/rdfextras/py3compat.py
# Compiled at: 2012-02-24 05:27:21
"""
Utility functions and objects to ease Python 3 compatibility.
"""
import sys
try:
    from functools import wraps
except ImportError:

    def wraps(f):

        def dec(newf):
            return newf

        return dec


def cast_bytes(s, enc='utf-8'):
    if isinstance(s, unicode):
        return s.encode(enc)
    return s


PY3 = sys.version_info[0] >= 3

def _modify_str_or_docstring(str_change_func):

    @wraps(str_change_func)
    def wrapper(func_or_str):
        if isinstance(func_or_str, str):
            func = None
            doc = func_or_str
        else:
            func = func_or_str
            doc = func.__doc__
        doc = str_change_func(doc)
        if func:
            func.__doc__ = doc
            return func
        else:
            return doc

    return wrapper


if PY3:

    def b(s):
        return s.encode('ascii')


    bytestype = bytes

    @_modify_str_or_docstring
    def format_doctest_out(s):
        """Python 2 version
        "%(u)s'abc'" --> "'abc'"
        "%(b)s'abc'" --> "b'abc'"
        "55%(L)s"    --> "55"
        
        Accepts a string or a function, so it can be used as a decorator."""
        return s % {'u': '', 'b': 'b', 'L': ''}


    def type_cmp(a, b):
        """Python 2 style comparison based on type"""
        ta, tb = type(a).__name__, type(b).__name__
        if ta == 'str':
            ta = 'unicode'
        if tb == 'str':
            tb = 'unicode'
        if ta > tb:
            return 1
        else:
            if ta < tb:
                return -1
            return 0


else:

    def b(s):
        return s


    bytestype = str

    @_modify_str_or_docstring
    def format_doctest_out(s):
        """Python 2 version
        "%(u)s'abc'" --> "u'abc'"
        "%(b)s'abc'" --> "'abc'"
        "55%(L)s"    --> "55L"
        
        Accepts a string or a function, so it can be used as a decorator."""
        return s % {'u': 'u', 'b': '', 'L': 'L'}


    def type_cmp(a, b):
        if a > b:
            return 1
        else:
            if a < b:
                return -1
            return 0