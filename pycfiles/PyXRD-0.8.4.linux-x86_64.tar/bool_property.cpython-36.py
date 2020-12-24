# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python3.6/dist-packages/mvc/models/properties/bool_property.py
# Compiled at: 2020-03-07 03:51:49
# Size of source mod 2**32: 1525 bytes
from .cast_property import CastProperty

class BoolProperty(CastProperty):
    __doc__ = '\n     A descriptor that will cast values to booleans.\n     Expects its label to be set or passed to __init__.\n    '
    data_type = bool
    widget_type = 'toggle'

    def __init__(self, *args, **kwargs):
        (super(BoolProperty, self).__init__)(args, cast_to=bool, **kwargs)