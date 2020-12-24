# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/formskit/converters.py
# Compiled at: 2016-04-05 11:05:23
# Size of source mod 2**32: 2136 bytes
from datetime import datetime

class FakeConvert(object):
    __doc__ = 'Default convertor which does nothing.'

    def _set_field(self, field):
        self.field = field

    def __call__(self, value):
        return self.convert(value)

    def convert(self, value):
        return value

    def convert_back(self, value):
        return value

    def back(self, value):
        return self.convert_back(value)

    def make_field(self):
        pass


class ToInt(FakeConvert):
    __doc__ = 'Converts to int.'

    def convert(self, value):
        try:
            return int(value)
        except (ValueError, TypeError):
            return

    def convert_back(self, value):
        if value is None:
            return
        else:
            return str(value)


class ToDate(FakeConvert):
    __doc__ = 'Converts to datetime.'
    format = '%Y-%m-%d'

    def convert(self, value):
        try:
            return datetime.strptime(value, self.format)
        except (ValueError, TypeError):
            return

    def convert_back(self, value):
        if value:
            return value.strftime(self.format)
        else:
            return


class ToDatetime(FakeConvert):
    __doc__ = 'Converts to datetime.'
    format = '%Y-%m-%d %H:%M'

    def convert(self, value):
        try:
            return datetime.strptime(value, self.format)
        except (ValueError, TypeError):
            return

    def convert_back(self, value):
        if value:
            return value.strftime(self.format)
        else:
            return

    def make_field(self):
        fvalue = self.field.values.pop(1)
        self.field.values[0].value += ' ' + fvalue.value


class ToBool(FakeConvert):

    def convert(self, value):
        if value in ('1', '2'):
            return True
        else:
            return False

    def convert_back(self, value):
        if value:
            return '1'
        else:
            return ''

    def make_field(self):
        value = self.field.form and self.field.name in self.field.form.raw_data
        self.field.set_value(value)