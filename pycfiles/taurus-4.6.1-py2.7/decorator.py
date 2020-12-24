# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/taurus/core/util/decorator/decorator.py
# Compiled at: 2019-08-19 15:09:29
"""
Provides a decorator to decorate decorators so that they can be used both
with and without args
"""
__all__ = [
 'decorator']
__docformat__ = 'restructuredtext'
import functools, inspect

def decorator(func):
    """
    Allow to use decorator either with arguments or not. Example::

        @decorator
        def apply(func, *args, **kw):
            return func(*args, **kw)

        @decorator
        class apply:
            def __init__(self, *args, **kw):
                self.args = args
                self.kw   = kw

            def __call__(self, func):
                return func(*self.args, **self.kw)

        #
        # Usage in both cases:
        #
        @apply
        def test():
            return 'test'

        assert test == 'test'

        @apply(2, 3)
        def test(a, b):
            return a + b

        assert test == 5

    """

    def isFuncArg(*args, **kw):
        return len(args) == 1 and len(kw) == 0 and (inspect.isfunction(args[0]) or isinstance(args[0], type))

    if isinstance(func, type):

        def class_wrapper(*args, **kw):
            if isFuncArg(*args, **kw):
                return func()(*args, **kw)
            return func(*args, **kw)

        class_wrapper.__name__ = func.__name__
        class_wrapper.__module__ = func.__module__
        return class_wrapper

    @functools.wraps(func)
    def func_wrapper(*args, **kw):
        if isFuncArg(*args, **kw):
            return func(*args, **kw)

        def functor(userFunc):
            return func(userFunc, *args, **kw)

        return functor

    return func_wrapper