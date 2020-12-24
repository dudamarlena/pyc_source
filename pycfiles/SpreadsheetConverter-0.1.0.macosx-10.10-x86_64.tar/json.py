# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/yugo/.virtualenvs/ssc/lib/python2.7/site-packages/spreadsheetconverter/handler/json.py
# Compiled at: 2015-09-14 12:51:54
from __future__ import absolute_import
from __future__ import unicode_literals
import datetime, json, os
from six import text_type
from .base import BaseHandler
from .valueformatter.base import BaseValueFormatter

class DatetimeValueFormatter(BaseValueFormatter):

    def format(self, value):
        if isinstance(value, datetime.datetime):
            return text_type(value)
        return value


class Handler(BaseHandler):

    def save(self, data):
        path = self.handler_config[b'path']
        base_path = os.environ.get(b'SSC_JSON_BASE_PATH')
        if base_path:
            path = os.path.join(base_path, path)
        _path, _filename = os.path.split(path)
        if not os.path.exists(_path):
            os.makedirs(_path)
        with open(path, b'w') as (f):
            indent = self.handler_config.get(b'indent')
            sort_keys = self.handler_config.get(b'sort_keys', False)
            f.write(json.dumps(data, indent=indent, sort_keys=sort_keys))

    def get_value_formatter(self, setting):
        if setting[b'type'] == b'datetime':
            return DatetimeValueFormatter(setting)
        return super(Handler, self).get_value_formatter(setting)