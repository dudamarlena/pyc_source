# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/yugo/.virtualenvs/ssc/lib/python2.7/site-packages/spreadsheetconverter/loader/valueconverter/float.py
# Compiled at: 2015-09-14 12:51:54
from __future__ import absolute_import
from __future__ import unicode_literals
from .base import BaseValueConverter

class ValueConverter(BaseValueConverter):

    def _to_python(self, value):
        return float(value)