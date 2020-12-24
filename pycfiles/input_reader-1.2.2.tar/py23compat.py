# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/Seth/Programming/input_reader/input_reader/py23compat.py
# Compiled at: 2014-03-01 14:21:20
from __future__ import unicode_literals
import functools, sys
py23_str = str if sys.version[0] == b'3' else unicode
py23_range = range if sys.version[0] == b'3' else xrange
py23_basestring = str if sys.version[0] == b'3' else basestring
py23_input = input if sys.version[0] == b'3' else raw_input
if sys.version[0] == b'3':
    py23_zip = zip
else:
    import itertools
    py23_zip = itertools.izip
if sys.version[0] == b'3':
    py23_items = lambda x: getattr(x, b'items')
else:
    py23_items = lambda x: getattr(x, b'iteritems')
if sys.version[0] == b'3':
    py23_values = lambda x: getattr(x, b'values')
else:
    py23_values = lambda x: getattr(x, b'itervalues')

def _modify_str_or_docstring(str_change_func):

    @functools.wraps(str_change_func)
    def wrapper(func_or_str):
        if isinstance(func_or_str, py23_basestring):
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


if sys.version[0] == b'3':

    @_modify_str_or_docstring
    def u_format(s):
        """"{u}'abc'" --> "'abc'" (Python 3)
        
        Accepts a string or a function, so it can be used as a decorator."""
        return s.format(u=b'')


else:

    @_modify_str_or_docstring
    def u_format(s):
        """"{u}'abc'" --> "u'abc'" (Python 2)
        
        Accepts a string or a function, so it can be used as a decorator."""
        return s.format(u=b'u')