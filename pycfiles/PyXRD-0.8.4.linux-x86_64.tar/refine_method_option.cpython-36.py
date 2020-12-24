# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python3.6/dist-packages/pyxrd/refinement/refine_method_option.py
# Compiled at: 2020-03-07 03:51:50
# Size of source mod 2**32: 1640 bytes


class RefineMethodOption(object):
    __doc__ = ' Descriptor for refinement methods '
    label = None

    def __init__(self, description, default=None, limits=[None, None], value_type=object, fget=None, fset=None, fdel=None, doc=None, label=None):
        self.description = description
        self.limits = limits
        self.value_type = value_type
        self.fget = fget
        self.fset = fset
        self.fdel = fdel
        if doc is None:
            if fget is not None:
                doc = fget.__doc__
        self.__doc__ = doc
        self.label = label
        self.default = default

    def __get__(self, instance, owner):
        if instance is None:
            return self
        else:
            if self.fget is None:
                return getattr(instance, '_%s' % self.label, self.default)
            return self.fget(instance)

    def __set__(self, instance, value):
        _min, _max = self.limits
        if self.value_type in (str, int, float):
            value = self.value_type(value)
        else:
            if _min is not None:
                value = max(value, _min)
            if _max is not None:
                value = min(value, _max)
            if self.fset is None:
                setattr(instance, '_%s' % self.label, value)
            else:
                return self.fset(instance, value)

    def __delete__(self, instance):
        if self.fdel is None:
            raise AttributeError("can't delete attribute")
        self.fdel(instance)