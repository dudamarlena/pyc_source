# uncompyle6 version 3.6.7
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-i686/egg/boduch/type/util.py
# Compiled at: 2009-08-14 17:29:30
__doc__ = 'This module defines some simple utility type functionality.'
import types
from boduch.constant import *

def is_type(obj, t):
    """Return true if the specified obj is the specified type."""
    candidates = []
    if hasattr(obj, '__name__'):
        candidates.append(obj.__name__)
    elif hasattr(obj, '__class__'):
        class_obj = obj.__class__
        candidates.append(class_obj.__name__)
        for base in class_obj.__bases__:
            candidates.append(base.__name__)

    if hasattr(obj, '__bases__'):
        for base in obj.__bases__:
            candidates.append(base.__name__)

    if t in candidates:
        return True
    else:
        t = t.upper()
        if t == TYPE_BOOL or t == TYPE_BOOLEAN:
            return type(obj) is types.BooleanType
        elif t == TYPE_INT or t == TYPE_INTEGER:
            return type(obj) is types.IntType
        elif t == TYPE_LONG:
            return type(obj) is types.LongType
        elif t == TYPE_FLOAT:
            return type(obj) is types.FloatType
        elif t == TYPE_STR or t == TYPE_STRING:
            return type(obj) is types.StringType
        elif t == TYPE_UNICODE:
            return type(obj) is types.UnicodeType
        elif t == TYPE_TUPLE:
            return type(obj) is types.TupleType
        elif t == TYPE_LIST:
            return type(obj) is types.ListType
        elif t == TYPE_DICT or t == TYPE_DICTIONARY:
            return type(obj) is types.DictionaryType


__all__ = [
 'is_type']