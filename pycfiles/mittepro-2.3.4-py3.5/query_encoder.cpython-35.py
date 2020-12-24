# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/mittepro/apysignature/query_encoder.py
# Compiled at: 2019-11-05 14:08:37
# Size of source mod 2**32: 989 bytes
import six, json, urllib

class QueryEncoder(object):

    @staticmethod
    def encode_param(key, value):
        if isinstance(value, list):
            return '&'.join([QueryEncoder.escape(key) + '[]=' + QueryEncoder.escape(item) for item in value])
        else:
            return QueryEncoder.escape(key) + '=' + QueryEncoder.escape(value)

    @staticmethod
    def encode_param_without_escaping(key, value):
        if isinstance(value, list):
            return str('&'.join([key + '[]=' + item for item in value]))
        if isinstance(value, dict):
            value = json.dumps(value)
        elif six.PY2 and isinstance(value, unicode):
            value = str(value.encode('utf-8'))
        return '{key}={value}'.format(key=key, value=value)

    @staticmethod
    def escape(s):
        if six.PY2:
            return urllib.quote(s, '')
        else:
            return urllib.parse.quote(s, '')