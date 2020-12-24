# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: .\django\core\formatter\json.py
# Compiled at: 2018-02-12 22:15:17
# Size of source mod 2**32: 416 bytes
import json
from idh.django.formatter.base import Formatter

class JSONFormatter(Formatter):

    def content_type(self):
        return 'application/json'

    def content_data(self, data, **kwargs):
        if data is None:
            return ''
        result = super(JSONFormatter, self).fx_dumps(data, **kwargs)
        return json.dumps(result)