# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/yugo/.virtualenvs/ssc/lib/python2.7/site-packages/spreadsheetconverter/loader/valueconverter/base.py
# Compiled at: 2015-09-14 12:51:54
from __future__ import absolute_import
from __future__ import unicode_literals

class BaseValueConverter(object):

    def __init__(self, settings, config=None):
        """
        :type settings: dict
        :type config: Config
        """
        self.settings = settings
        self._config = config
        self._has_default = b'default' in settings
        self._default = settings.get(b'default')

    def to_python(self, value):
        try:
            return self._to_python(value)
        except ValueError:
            if not value:
                return self.get_default()
            raise

    def _to_python(self, value):
        return value

    def get_default(self):
        if self._has_default:
            return self._default
        raise ValueError((b'nothing default {}').format(self.fieldname))

    @property
    def fieldname(self):
        return self.settings[b'column']