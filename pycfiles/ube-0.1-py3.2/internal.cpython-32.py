# uncompyle6 version 3.7.4
# Python bytecode 3.2 (3180)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/ube/concerns/internal.py
# Compiled at: 2013-08-25 16:11:22
"""
Created on Nov 6, 2012

@author: Nicklas Boerjesson
@note: This decorator raises an error if a certain method is decorated
"""
from decorator import decorator

def _not_implemented(func, *args, **kwargs):
    raise Exception('Internal error in "' + func.__name__ + '": Not implemented.')


def not_implemented(f):
    """Raises an "Internal error in func: Not implemented."""
    return decorator(_not_implemented, f)