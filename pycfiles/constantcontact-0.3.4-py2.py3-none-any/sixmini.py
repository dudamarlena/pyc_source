# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /Users/sanhehu/Documents/GitHub/constant2-project/constant2/pkg/sixmini.py
# Compiled at: 2018-12-19 11:16:54
__doc__ = '\nThis is a minimized six model.\n'
import sys, types
PY2 = sys.version_info[0] == 2
PY3 = sys.version_info[0] == 3
if PY3:
    string_types = (
     str,)
    integer_types = (int,)
    class_types = (type,)
    text_type = str
    binary_type = bytes
    MAXSIZE = sys.maxsize
else:
    string_types = (
     basestring,)
    integer_types = (int, long)
    class_types = (type, types.ClassType)
    text_type = unicode
    binary_type = str
    if sys.platform.startswith('java'):
        MAXSIZE = int(2147483647)
    else:

        class X(object):

            def __len__(self):
                return 2147483648


        try:
            len(X())
        except OverflowError:
            MAXSIZE = int(2147483647)
        else:
            MAXSIZE = int(9223372036854775807)

        del X

def add_metaclass(metaclass):
    """Class decorator for creating a class with a metaclass."""

    def wrapper(cls):
        orig_vars = cls.__dict__.copy()
        slots = orig_vars.get('__slots__')
        if slots is not None:
            if isinstance(slots, str):
                slots = [
                 slots]
            for slots_var in slots:
                orig_vars.pop(slots_var)

        orig_vars.pop('__dict__', None)
        orig_vars.pop('__weakref__', None)
        return metaclass(cls.__name__, cls.__bases__, orig_vars)

    return wrapper