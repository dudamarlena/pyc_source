# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/boduch/type/util.py
# Compiled at: 2009-08-14 17:29:30
"""This module defines some simple utility type functionality."""
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