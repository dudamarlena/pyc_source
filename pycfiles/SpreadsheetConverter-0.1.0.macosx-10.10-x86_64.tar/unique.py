# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/yugo/.virtualenvs/ssc/lib/python2.7/site-packages/spreadsheetconverter/loader/validator/unique.py
# Compiled at: 2015-09-14 12:51:54
from __future__ import absolute_import
from __future__ import unicode_literals
from .base import BaseValidator

class Validator(BaseValidator):

    def __init__(self, settings):
        super(Validator, self).__init__(settings)
        self._data = set()

    def validate(self, value):
        if value in self._data:
            raise ValueError((b'Duplicate value {}: {}').format(self.fieldname, value))
        self._data.add(value)