# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/pocoo/utils/debug.py
# Compiled at: 2006-12-26 17:18:07
"""
    pocoo.utils.debug
    ~~~~~~~~~~~~~~~~~

    Implements a simple debugging toolkit.

    Usage example::

        from pocoo.utils.debug import use_dtk, dtk

        use_dtk()
        dtk.log('source', 'important message')

    :copyright: 2006 by Georg Brandl.
    :license: GNU GPL, see LICENSE for more details.
"""
import sys, time
from pocoo.utils.logging import Logger

class DtkBase(object):
    __module__ = __name__

    def __init__(self):
        self._logger = Logger(stream=sys.stderr)

    def set_output(self, ctx):
        self._logger = Logger(ctx=ctx)


class FakeDtk(DtkBase):
    __module__ = __name__

    def log(self, component, msg, *args):
        pass

    def trace(self, func):
        return func

    def trace_time(self, func):
        return func

    def trace_if_return(self, condition):
        return lambda func: func

    def trace_if_exc(self, func):
        return func


class RealDtk(DtkBase):
    __module__ = __name__

    def log(self, component, msg, *args):
        self._logger._log(0, component, msg % args)

    def trace(self, func):
        """ Decorator.
        If debugging is enabled, wrap function to print arguments
        and return value.
        """
        name = func.func_name
        parent = sys._getframe(1).f_code.co_name

        def wrapper(*args, **kwargs):
            self.log(parent, '%s() called with %r, %r' % (name, args, kwargs))
            ret = func(*args, **kwargs)
            if ret is not None:
                self.log(parent, '  ... returned %r' % ret)
            return ret

        wrapper.func_name = name
        wrapper.__doc__ = func.__doc__
        return wrapper

    def trace_time(self, func):
        """ Decorator.
        Print how long the function took to run.
        """
        name = func.func_name
        parent = sys._getframe(1).f_code.co_name

        def wrapper(*args, **kwargs):
            self.log(parent, '%s() called with %r, %r' % (name, args, kwargs))
            t1 = time.time()
            ret = func(*args, **kwargs)
            t2 = time.time()
            self.log(parent, '  ... took %.4f' % (t2 - t1))
            return ret

        wrapper.func_name = name
        wrapper.__doc__ = func.__doc__
        return wrapper

    def trace_if_return(self, condition):
        """ Decorator.
        Print trace information of decorated function only if the
        condition is true.
        """

        def decorator(func):
            name = func.func_name
            parent = sys._getframe(1).f_code.co_name

            def wrapper(*args, **kwargs):
                ret = func(*args, **kwargs)
                if eval('ret ' + condition):
                    self.log(parent, '%s() called with %r, %r' % (name, args, kwargs))
                    self.log(parent, '  ... returned %r' % ret)
                return ret

            wrapper.func_name = name
            wrapper.__doc__ = func.__doc__
            return wrapper

        return decorator

    def trace_if_exc(self, func):
        """ Decorator.
        Print trace information of function if it raises an exception.
        """
        name = func.func_name
        parent = sys._getframe(1).f_code.co_name

        def wrapper(*args, **kwargs):
            try:
                ret = func(*args, **kwargs)
            except Exception, exc:
                self.log(parent, '%s() called with %r, %r' % (name, args, kwargs))
                self.log(parent, '  ... raised %r' % exc)
                raise
            else:
                return ret

        wrapper.func_name = name
        wrapper.__doc__ = func.__doc__
        return wrapper


dtk = FakeDtk()

def use_dtk(enable=True):
    if enable:
        dtk.__class__ = RealDtk
    else:
        dtk.__class__ = FakeDtk