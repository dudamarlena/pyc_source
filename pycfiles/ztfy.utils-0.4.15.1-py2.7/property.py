# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/ztfy/utils/property.py
# Compiled at: 2015-11-17 06:09:34
from ztfy.utils.request import queryRequest, getRequestData, setRequestData
from ztfy.utils.session import getSessionData, setSessionData

class cached(object):
    """Custom property decorator to define a property or function
    which is calculated only once
       
    When applied on a function, caching is based on input arguments
    """

    def __init__(self, function):
        self._function = function
        self._cache = {}

    def __call__(self, *args):
        try:
            return self._cache[args]
        except KeyError:
            self._cache[args] = self._function(*args)
            return self._cache[args]

    def expire(self, *args):
        del self._cache[args]


class cached_property(object):
    """A read-only @property decorator that is only evaluated once. The value is cached
    on the object itself rather than the function or class; this should prevent
    memory leakage.
    """

    def __init__(self, fget, doc=None):
        self.fget = fget
        self.__doc__ = doc or fget.__doc__
        self.__name__ = fget.__name__
        self.__module__ = fget.__module__

    def __get__(self, obj, cls):
        if obj is None:
            return self
        else:
            obj.__dict__[self.__name__] = result = self.fget(obj)
            return result


_marker = object()

def request_property(key):
    """Define a method decorator used to store result into request's annotations

    `key` is a required argument; if None, the key will be the method's object
    """

    def request_decorator(func):

        def wrapper(obj, key, *args, **kwargs):
            request = queryRequest()
            if callable(key):
                key = key(obj)
            if not key:
                key = ('{0!r}').format(obj)
            data = getRequestData(key, request, _marker)
            if data is _marker:
                data = func
                if callable(data):
                    data = data(obj, *args, **kwargs)
                setRequestData(key, data, request)
            return data

        return lambda x: wrapper(x, key=key)

    return request_decorator


class session_property(object):
    """Define a property for which computed value is stored into session"""

    def __init__(self, fget, app, key=None):
        self.fget = fget
        self.app = app
        if key is None:
            key = '%s.%s' % (fget.__module__, fget.__name__)
        self.key = key
        return

    def __get__(self, obj, cls):
        if obj is None:
            return self
        else:
            request = queryRequest()
            data = getSessionData(request, self.app, self.key, _marker)
            if data is _marker:
                data = self.fget(obj)
                setSessionData(request, self.app, self.key, data)
            return data