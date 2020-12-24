# uncompyle6 version 3.6.7
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/aiogcd/orm/properties/datetimevalue.py
# Compiled at: 2019-09-11 07:21:09
# Size of source mod 2**32: 958 bytes
from .value import Value
from connector.timestampvalue import TimestampValue
import re
RFC3339_RE = re.compile('^\\d{4}-\\d{2}-\\d{2}T\\d{2}:\\d{2}:\\d{2}(?:\\.\\d{1,9})?(?:(?:[\\+\\-]\\d{2}:\\d{2})|Z)$')

class DatetimeValue(Value):

    def check_value(self, value):
        if not isinstance(value, TimestampValue):
            raise TypeError("Expecting an value of type 'TimestampValue' for property {!r} but received type {!r}.".format(self.name, value.__class__.__name__))
        if not RFC3339_RE.search(str(value)):
            raise TypeError("Expecting a value of type 'str' in RFC3339 datetime format for property {!r}.".format(self.name))

    def set_value(self, model, value):
        if isinstance(value, str):
            value = TimestampValue(value)
        self.check_value(value)
        super().set_value(model, value)