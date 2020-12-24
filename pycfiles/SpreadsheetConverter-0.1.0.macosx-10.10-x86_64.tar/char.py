# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/yugo/.virtualenvs/ssc/lib/python2.7/site-packages/spreadsheetconverter/loader/valueconverter/char.py
# Compiled at: 2015-09-14 12:51:54
from __future__ import absolute_import
from __future__ import unicode_literals
from .base import BaseValueConverter
import six

class ValueConverter(BaseValueConverter):

    def to_python(self, value):
        if isinstance(value, six.string_types) and self._has_default and not value:
            return self.get_default()
        return six.text_type(value)