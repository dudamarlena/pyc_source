# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-intel/egg/tailow/fields/datetime.py
# Compiled at: 2018-06-14 12:05:35
# Size of source mod 2**32: 587 bytes
from datetime import datetime
from tailow.fields.base import BaseField
DEFAULT_FORMAT = '%Y-%m-%d-%H-%M-%S'

class DateTimeField(BaseField):
    FORMAT = DEFAULT_FORMAT

    def __init__(self, date_format=None, **kwargs):
        (super(DateTimeField, self).__init__)(**kwargs)
        self.FORMAT = date_format or self.__class__.FORMAT

    def to_son(self, value):
        return value.strftime(self.FORMAT)

    def from_son(self, value):
        return datetime.strptime(value, self.FORMAT)

    def validate(self, value):
        return isinstance(value, datetime)