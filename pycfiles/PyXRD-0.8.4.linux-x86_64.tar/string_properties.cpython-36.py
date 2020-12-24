# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python3.6/dist-packages/mvc/models/properties/string_properties.py
# Compiled at: 2020-03-07 03:51:49
# Size of source mod 2**32: 2678 bytes
from .cast_property import CastProperty
from .cast_choice_property import CastChoiceProperty

class StringProperty(CastProperty):
    __doc__ = '\n     A descriptor that will cast values to strings and can optionally clamp\n     values to a minimum and maximum.\n     Expects its label to be set or passed to __init__.\n    '
    data_type = str
    widget_type = 'entry'

    def __init__(self, *args, **kwargs):
        (super(StringProperty, self).__init__)(args, cast_to=str, **kwargs)


class ColorProperty(StringProperty):
    __doc__ = '\n     A descriptor that will cast values to strings and can optionally clamp\n     values to a minimum and maximum. Has a color widget as the default widget.\n     Expects its label to be set or passed to __init__.\n    '
    widget_type = 'color'


class StringChoiceProperty(CastChoiceProperty):
    __doc__ = '\n     A descriptor that will cast values to strings and can optionally clamp\n     values to a minimum and maximum.\n     It also expects the (cast and clamped) value to be in a set of choices or\n     it will raise a ValueError.\n     Expects its label to be set or passed to __init__.\n    '
    data_type = str
    widget_type = 'option_list'

    def __init__(self, choices=[], *args, **kwargs):
        (super(StringChoiceProperty, self).__init__)(args, cast_to=str, choices=choices, **kwargs)