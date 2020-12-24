# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python3.6/dist-packages/mvc/models/properties/cast_choice_property.py
# Compiled at: 2020-03-07 03:51:49
# Size of source mod 2**32: 2041 bytes
from .cast_property import CastProperty

class CastChoiceProperty(CastProperty):
    __doc__ = '\n     A descriptor that can cast the values to a given type, clamp values to a\n     minimum and maximum.\n     It also expects the (cast and clamped) value to be in a list or dict of\n     choices or it will raise a ValueError.\n     Expects its label to be set or passed to __init__.\n    '
    choices = None
    widget_type = 'option_list'

    def __init__(self, choices=[], *args, **kwargs):
        (super(CastChoiceProperty, self).__init__)(*args, **kwargs)
        self.choices = choices

    def __set__(self, instance, value):
        value = self.__cast_and_clamp__(instance, value)
        if value in self.choices:
            super(CastProperty, self).__set__(instance, value)
        else:
            raise ValueError("'%s' is not a valid value for %s!" % (value, self.label))