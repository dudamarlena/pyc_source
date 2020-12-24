# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python3.6/dist-packages/mvc/support/observables/value_wrapper.py
# Compiled at: 2020-03-07 03:51:49
# Size of source mod 2**32: 2695 bytes
from mvc.support.utils import not_none

class ValueWrapper(object):
    wrappers = []

    @staticmethod
    def register_wrapper(cls=None, position=None):
        """
            Decorator that can be applied to wrapper classes (need to 
            define a wrap_value(label, value, model=None) method).
            Can also be called with a position keyword argument to
            force that wrapper to be at a certain position in the list of
            wrappers.
            Otherwise appends the wrapper to the end of wrapper list.
        """

        def inner(cls, position=None):
            position = not_none(position, len(ValueWrapper.wrappers))
            ValueWrapper.wrappers.insert(position, cls.wrap_value)

        if cls == None:
            return inner
        else:
            return inner(cls, position=position)

    @staticmethod
    def wrap_value(label, val, model=None, verbose=False):
        """This is used to wrap a value to be assigned to a
        property. Depending on the type of the value, different values
        are created and returned. For example, for a list, a
        ListWrapper is created to wrap it, and returned for the
        assignment. model is different from None when the value is
        changed (a model exists). Otherwise, during property creation
        model is None"""
        for wrapper in ValueWrapper.wrappers:
            wrapped = wrapper(label, val, model)
            if wrapped is None:
                continue
            else:
                return wrapped

        return val