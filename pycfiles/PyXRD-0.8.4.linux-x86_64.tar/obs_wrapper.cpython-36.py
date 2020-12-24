# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python3.6/dist-packages/mvc/support/observables/obs_wrapper.py
# Compiled at: 2020-03-07 03:51:49
# Size of source mod 2**32: 2544 bytes
from .base import ObsWrapperBase

class ObsWrapper(ObsWrapperBase):
    __doc__ = '\n    Base class for wrappers, like user-classes and sequences.\n    Use sub-classes!\n    '

    def __init__(self, obj, method_names):
        ObsWrapperBase.__init__(self)
        self._obj = obj
        self.__doc__ = obj.__doc__
        d = dict((name, self._ObsWrapper__get_wrapper(name)) for name in method_names)
        self.__class__ = type(self.__class__.__name__, (self.__class__,), d)

    def __get_wrapper(self, name):

        def _wrapper_fun(self, *args, **kwargs):
            self._notify_method_before(self._obj, name, args, kwargs)
            res = (getattr(self._obj, name))(*args, **kwargs)
            self._notify_method_after(self._obj, name, res, args, kwargs)
            return res

        return _wrapper_fun

    def __getattr__(self, name):
        return getattr(self._obj, name)

    def __repr__(self):
        return self._obj.__repr__()

    def __str__(self):
        return self._obj.__str__()