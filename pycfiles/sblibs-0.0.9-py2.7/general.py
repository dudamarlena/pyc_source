# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.12-intel/egg/sblibs/display/general.py
# Compiled at: 2017-09-18 18:37:05
"""
    An collection of usefull decorators for debug
    and time evaluation of functions flow
"""
from functools import wraps
import sys
PY2 = sys.version_info[0] == 2
PY3 = sys.version_info[0] == 3
if PY2:
    from itertools import izip
    zip = izip
else:
    zip = zip

def with_metaclass(meta, *bases):
    """Create a base class with a metaclass."""

    class metaclass(meta):
        """Dummy metaclass"""

        def __new__(cls, name, this_bases, d):
            return meta(name, bases, d)

    return type.__new__(metaclass, 'temporary_class', (), {})


def cache(function):
    """
    Function: cache
    Summary: Decorator used to cache the input->output
    Examples: An fib memoized executes at O(1) time
              instead O(e^n)
    Attributes:
        @param (function): function
    Returns: wrapped function

    TODO: Give support to functions with kwargs
    """
    memory = {}
    miss = object()

    @wraps(function)
    def _wrapper(*args):
        result = memory.get(args, miss)
        if result is miss:
            _wrapper.call += 1
            result = function(*args)
            memory[args] = result
        return result

    _wrapper.call = 0
    return _wrapper