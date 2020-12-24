# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/lib/python3.5/site-packages/future/backports/total_ordering.py
# Compiled at: 2016-10-27 16:05:38
# Size of source mod 2**32: 1929 bytes
"""
For Python < 2.7.2. total_ordering in versions prior to 2.7.2 is buggy.
See http://bugs.python.org/issue10042 for details. For these versions use
code borrowed from Python 2.7.3.

From django.utils.
"""
import sys
if sys.version_info >= (2, 7, 2):
    from functools import total_ordering
else:

    def total_ordering(cls):
        """Class decorator that fills in missing ordering methods"""
        convert = {'__lt__': [('__gt__', lambda self, other: not (self < other or self == other)),
                    (
                     '__le__', lambda self, other: self < other or self == other),
                    (
                     '__ge__', lambda self, other: not self < other)], 
         
         '__le__': [('__ge__', lambda self, other: not self <= other or self == other),
                    (
                     '__lt__', lambda self, other: self <= other and not self == other),
                    (
                     '__gt__', lambda self, other: not self <= other)], 
         
         '__gt__': [('__lt__', lambda self, other: not (self > other or self == other)),
                    (
                     '__ge__', lambda self, other: self > other or self == other),
                    (
                     '__le__', lambda self, other: not self > other)], 
         
         '__ge__': [('__le__', lambda self, other: not self >= other or self == other),
                    (
                     '__gt__', lambda self, other: self >= other and not self == other),
                    (
                     '__lt__', lambda self, other: not self >= other)]}
        roots = set(dir(cls)) & set(convert)
        if not roots:
            raise ValueError('must define at least one ordering operation: < > <= >=')
        root = max(roots)
        for opname, opfunc in convert[root]:
            if opname not in roots:
                opfunc.__name__ = opname
                opfunc.__doc__ = getattr(int, opname).__doc__
                setattr(cls, opname, opfunc)

        return cls