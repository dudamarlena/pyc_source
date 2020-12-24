# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python3.6/dist-packages/mvc/models/properties/cast_property.py
# Compiled at: 2020-03-07 03:51:49
# Size of source mod 2**32: 2221 bytes
from .labeled_property import LabeledProperty

class CastProperty(LabeledProperty):
    __doc__ = '\n     A descriptor that can cast the values to a given type and clamp values to a\n     minimum and maximum. \n     Expects its label to be set or passed to __init__.\n    '

    def __init__(self, minimum=None, maximum=None, cast_to=None, *args, **kwargs):
        (super(CastProperty, self).__init__)(*args, **kwargs)
        self.minimum = minimum
        self.maximum = maximum
        self.cast_to = cast_to

    def __cast_and_clamp__(self, instance, value):
        if self.minimum is not None:
            value = max(value, self.minimum)
        else:
            if self.maximum is not None:
                value = min(value, self.maximum)
            if self.cast_to is not None:
                if value is not None:
                    value = self.cast_to(value)
        return value

    def __set__(self, instance, value):
        value = self.__cast_and_clamp__(instance, value)
        if getattr(instance, self.label) != value:
            super(CastProperty, self).__set__(instance, value)