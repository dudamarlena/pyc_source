# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/yugo/.virtualenvs/ssc/lib/python2.7/site-packages/spreadsheetconverter/loader/valueconverter/datetime.py
# Compiled at: 2015-09-14 12:51:54
from __future__ import absolute_import
from __future__ import unicode_literals
import os
from dateutil.parser import parse
import pytz
from .base import BaseValueConverter

class ValueConverter(BaseValueConverter):

    def __init__(self, settings, **kwargs):
        super(ValueConverter, self).__init__(settings, **kwargs)
        self._timezone = None
        _default_timezone = os.environ.get(b'SSC_TIMEZONE')
        if _default_timezone:
            self._timezone = pytz.timezone(_default_timezone)
        _settings_timezone = settings.get(b'timezone')
        if _settings_timezone:
            self._timezone = pytz.timezone(_default_timezone)
        return

    def _to_python(self, value):
        if not value:
            raise ValueError
        return self._localize(parse(value))

    def _localize(self, value):
        if self._timezone and not value.tzinfo:
            return self._timezone.localize(value)
        return value