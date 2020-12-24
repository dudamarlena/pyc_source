# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\strategycontainer\utils\compat.py
# Compiled at: 2018-01-15 22:54:12
# Size of source mod 2**32: 2257 bytes
from six import PY2
import functools, sys
if PY2:
    from ctypes import py_object, pythonapi
    mappingproxy = pythonapi.PyDictProxy_New
    mappingproxy.argtypes = [py_object]
    mappingproxy.restype = py_object

    def exc_clear():
        sys.exc_clear()


    def update_wrapper(wrapper, wrapped, assigned=functools.WRAPPER_ASSIGNMENTS, updated=functools.WRAPPER_UPDATES):
        """Backport of Python 3's functools.update_wrapper for __wrapped__.
        """
        for attr in assigned:
            try:
                value = getattr(wrapped, attr)
            except AttributeError:
                pass
            else:
                setattr(wrapper, attr, value)

        for attr in updated:
            getattr(wrapper, attr).update(getattr(wrapped, attr, {}))

        wrapper.__wrapped__ = wrapped
        return wrapper


    def wraps(wrapped, assigned=functools.WRAPPER_ASSIGNMENTS, updated=functools.WRAPPER_UPDATES):
        """Decorator factory to apply update_wrapper() to a wrapper function

           Returns a decorator that invokes update_wrapper() with the decorated
           function as the wrapper argument and the arguments to wraps() as the
           remaining arguments. Default arguments are as for update_wrapper().
           This is a convenience function to simplify applying partial() to
           update_wrapper().
        """
        return functools.partial(update_wrapper, wrapped=wrapped, assigned=assigned,
          updated=updated)


else:
    from types import MappingProxyType as mappingproxy

    def exc_clear():
        pass


    update_wrapper = functools.update_wrapper
    wraps = functools.wraps
unicode = type('')
__all__ = [
 'mappingproxy',
 'unicode']