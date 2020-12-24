# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/yugo/.virtualenvs/ssc/lib/python2.7/site-packages/spreadsheetconverter/loader/valueconverter/foreignkey.py
# Compiled at: 2015-09-14 12:51:54
from __future__ import absolute_import
from __future__ import unicode_literals
from ...exceptions import ForeignkeyTargetDataDoesNotExistError
from .base import BaseValueConverter

class ValueConverter(BaseValueConverter):

    def __init__(self, settings, **kwargs):
        super(ValueConverter, self).__init__(settings, **kwargs)
        self._relation_data = {}
        self._converter = None
        self._value_converter = None
        return

    def _to_python(self, value):
        converted = self.value_converter.to_python(value)
        if converted not in self.relation:
            raise ForeignkeyTargetDataDoesNotExistError((b'{}[{}:"{}"] does not exist in "{}"').format(self._config.name, self.settings[b'name'], value, self.settings[b'relation'][b'from'].name))
        return self.relation[converted]

    @property
    def value_converter(self):
        if self._value_converter:
            return self._value_converter
        self._value_converter = self.converter.config.get_converter_by_column(self.relation_field_from)
        return self._value_converter

    @property
    def converter(self):
        if self._converter:
            return self._converter
        from spreadsheetconverter import Converter
        self._converter = Converter(self.settings[b'relation'][b'from'], indent=2)
        return self._converter

    @property
    def relation(self):
        u"""
        変換表データ
        :rtype: dict
        """
        if self._relation_data:
            return self._relation_data
        for entity in self.converter.convert():
            from_value = entity[self.relation_field_from]
            to_value = entity[self.relation_field_to]
            self._relation_data[from_value] = to_value

        return self._relation_data

    @property
    def relation_field_to(self):
        return self.settings[b'relation'][b'column']

    @property
    def relation_field_from(self):
        return self.settings[b'relation'][b'key']