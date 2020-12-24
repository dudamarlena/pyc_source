# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/christian/workspace_py/jankflix-python/jankflixmodules/utils/decorators.py
# Compiled at: 2013-01-14 13:15:18
import functools, collections

class unicodeToAscii(object):
    """Decorator. Encodes the result of the function call as ascii, 
    ignoring unicode characters.
    """

    def __init__(self, func):
        self.func = func

    def __call__(self, *args):
        result = self.func(*args)
        if isinstance(result, unicode):
            return result.encode('ascii', 'ignore')
        else:
            if isinstance(result, list):
                return [ element.encode('ascii', 'ignore') for element in result ]
            else:
                if isinstance(result, dict):
                    assert isinstance(result, dict)
                    for key in result.iterkeys():
                        result[key] = result[key].encode('ascii', 'ignore')

                    return result
                if result == None:
                    return
                return result.encode('ascii', 'ignore')

            return

    def __repr__(self):
        """Return the function's docstring."""
        return self.func.__doc__

    def __get__(self, obj, objtype):
        """Support instance methods."""
        return functools.partial(self.__call__, obj)


class memoized(object):
    """Decorator. Caches a function's return value each time it is called.
    If called later with the same arguments, the cached value is returned
    (not reevaluated).
    """

    def __init__(self, func):
        self.func = func
        self.cache = {}

    def __call__(self, *args):
        if not isinstance(args, collections.Hashable):
            return self.func(*args)
        else:
            if args in self.cache:
                return self.cache[args]
            value = self.func(*args)
            self.cache[args] = value
            return value

    def __repr__(self):
        """Return the function's docstring."""
        return self.func.__doc__

    def __get__(self, obj, objtype):
        """Support instance methods."""
        return functools.partial(self.__call__, obj)