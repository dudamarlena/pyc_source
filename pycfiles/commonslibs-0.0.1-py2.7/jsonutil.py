# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/commonslib/jsonutil.py
# Compiled at: 2015-04-04 05:19:06
import json, datetime
from tornado.escape import to_basestring
__author__ = 'freeway'

class JSONExtensionEncoder(json.JSONEncoder):

    def default(self, obj):
        try:
            if isinstance(obj, datetime.date):
                encoded_object = obj.strftime('%Y-%m-%d')
            else:
                encoded_object = json.JSONEncoder.default(self, obj)
        except ValueError:
            encoded_object = '1900-01-01'

        return encoded_object


def json_encode(value):
    return json.dumps(value, cls=JSONExtensionEncoder).replace('</', '<\\/')


def json_decode(value):
    """Returns Python objects for the given JSON string."""
    return json.loads(to_basestring(value))