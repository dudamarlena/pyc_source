# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/yugo/.virtualenvs/ssc/lib/python2.7/site-packages/spreadsheetconverter/handler/inspector/number_range.py
# Compiled at: 2016-03-17 09:43:59
from __future__ import absolute_import
from __future__ import unicode_literals
from .base import BaseCompareNumberInspector

class Inspector(BaseCompareNumberInspector):

    def inspect(self, data):
        """
        :param data: row data
        """
        max_value = self._get_formula_result(self.setting[b'max'], data)
        min_value = self._get_formula_result(self.setting[b'min'], data)
        if min_value <= data[self.target_fieldname] <= max_value:
            return
        raise Exception(b'%s %s', self.target_fieldname, data)