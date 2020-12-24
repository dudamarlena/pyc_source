# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/dispatk.py
# Compiled at: 2015-10-07 18:24:04
"""
This function is inspired by singledispatch of Python 3.4+ (PEP 443),
but the dispatch happens on the key extracted fro the arguments values.

from dispatk import dispatk

@dispatk(lambda n: int(n))
def fib(n):
    return fib(n-1) + fib(n-2)

@fib.register(0)
def _(n):
    return 0

@fib.register(1, 2)
def _(n):
    return 1

@fib.register(41)
def _(n):
    return 165580141

*register* accepts one or more keys.

@fib.register(1, 2)
def _(n):
    return 1

is equivalent to

@fib.register(1)
@fib.register(2)
def _(n):
    return 1

"""
from functools import wraps
__all__ = ('dispatk', )

def dispatk(keyer):
    """This is the decorator for the generic function and it accepts
    only one argument *keyer*, it'll be called with the same arguments
    of the function call and it must return an hashable object
    (int, tuple, etc.).

    Rhe generic function has a *register* method used to decorate the
    function for some specific keys.
    *register* accepts one or more keys and returns the decorated
    function.
    """
    calls = {}

    def _dispatk(main):

        def register(*keys):

            def _register(spec):
                for key in keys:
                    if key in calls:
                        raise ValueError('function already registered for %r' % (
                         main.__name__, key))
                    calls[key] = spec

                return spec

            return _register

        @wraps(main)
        def run(*args, **kwargs):
            return calls.get(keyer(*args, **kwargs), main)(*args, **kwargs)

        run.register = register
        return run

    return _dispatk