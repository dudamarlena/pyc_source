# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/nbollweg/Documents/projects/widget-dateslider/dateslider/traits.py
# Compiled at: 2016-05-07 11:25:10
# Size of source mod 2**32: 432 bytes
from datetime import datetime
import six
from dateutil import parser
from traitlets import TraitType

class Date(TraitType):
    __doc__ = 'A trait for dates.'
    default_value = None
    info_text = 'a datetime'

    def validate(self, obj, value):
        if isinstance(value, datetime):
            return value
        if isinstance(value, six.text_type):
            return parser.parse(value)
        self.error(obj, value)