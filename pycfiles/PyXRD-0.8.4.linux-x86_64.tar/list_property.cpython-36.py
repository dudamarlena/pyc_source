# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python3.6/dist-packages/mvc/models/properties/list_property.py
# Compiled at: 2020-03-07 03:51:49
# Size of source mod 2**32: 1803 bytes
from .cast_property import CastProperty

class ListProperty(CastProperty):
    __doc__ = '\n     A descriptor that will cast values to lists.\n     Expects its label to be set or passed to __init__.\n    '
    widget_type = 'object_list_view'

    def __cast_and_clamp__(self, instance, value):
        if self.cast_to is not None:
            if value is not None:
                if not isinstance(value, self.cast_to):
                    value = self.cast_to(value)
        return value

    def __init__(self, *args, **kwargs):
        if 'cast_to' not in kwargs:
            kwargs['cast_to'] = list
        (super(ListProperty, self).__init__)(*args, **kwargs)