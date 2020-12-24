# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/socketio/defaultjson.py
# Compiled at: 2014-02-03 00:13:04
try:
    import simplejson as json
    json_decimal_args = {'use_decimal': True}
except ImportError:
    import json, decimal

    class DecimalEncoder(json.JSONEncoder):

        def default(self, o):
            if isinstance(o, decimal.Decimal):
                return float(o)
            return super(DecimalEncoder, self).default(o)


    json_decimal_args = {'cls': DecimalEncoder}

def default_json_dumps(data):
    return json.dumps(data, separators=(',', ':'), **json_decimal_args)


def default_json_loads(data):
    return json.loads(data)