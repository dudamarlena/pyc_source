# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\Crypto\Util\py21compat.py
# Compiled at: 2013-03-13 13:15:35
"""Compatibility code for Python 2.1

Currently, this just defines:
    - True and False
    - object
    - isinstance
"""
__revision__ = '$Id$'
__all__ = []
import sys, __builtin__
try:
    (
     True, False)
except NameError:
    True, False = (1, 0)
    __all__ += ['True', 'False']

try:
    object
except NameError:

    class object:
        pass


    __all__ += ['object']

try:
    isinstance(5, (int, long))
except TypeError:
    __all__ += ['isinstance']
    _builtin_type_map = {tuple: type(()), 
       list: type([]), 
       str: type(''), 
       unicode: type(''), 
       int: type(0), 
       long: type(0)}

    def isinstance(obj, t):
        if not __builtin__.isinstance(t, type(())):
            return __builtin__.isinstance(obj, _builtin_type_map.get(t, t))
        else:
            for typ in t:
                if __builtin__.isinstance(obj, _builtin_type_map.get(typ, typ)):
                    return True

            return False