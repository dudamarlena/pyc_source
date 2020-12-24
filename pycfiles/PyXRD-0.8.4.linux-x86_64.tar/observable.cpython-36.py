# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python3.6/dist-packages/mvc/support/observables/observable.py
# Compiled at: 2020-03-07 03:51:49
# Size of source mod 2**32: 1986 bytes
from ..decorators import good_classmethod_decorator
from .base import ObsWrapperBase

class Observable(ObsWrapperBase):

    @classmethod
    @good_classmethod_decorator
    def observed(cls, _func):
        """
        Decorate methods to be observable. If they are called on an instance
        stored in a property, the model will emit before and after
        notifications.
        """

        def wrapper(*args, **kwargs):
            self = args[0]
            assert isinstance(self, Observable)
            self._notify_method_before(self, _func.__name__, args, kwargs)
            res = _func(*args, **kwargs)
            self._notify_method_after(self, _func.__name__, res, args, kwargs)
            return res

        return wrapper