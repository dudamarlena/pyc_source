# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/yugo/.virtualenvs/ssc/lib/python2.7/site-packages/spreadsheetconverter/handler/inspector/number_gte.py
# Compiled at: 2016-03-17 09:43:59
from __future__ import absolute_import
from __future__ import unicode_literals
from .base import BaseCompareNumberInspector

class Inspector(BaseCompareNumberInspector):

    def inspect(self, data):
        """
        :param data: row data
        """
        if data[self.target_fieldname] >= self.get_compare_value(data):
            return
        raise Exception(b'%s %s', self.target_fieldname, data)