# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/synapseclient/core/models/custom_json.py
# Compiled at: 2020-03-23 17:17:03
# Size of source mod 2**32: 777 bytes
"""
When imported, monkey-patches the 'json' module's encoder with a custom json encoding function.
"""
import json, datetime
from synapseclient.core.utils import datetime_to_iso

def _json_encoder(self, obj):
    if isinstance(obj, datetime.datetime):
        return datetime_to_iso(obj, sep=' ').replace('Z', '')
    else:
        return getattr(obj.__class__, 'to_json', _json_encoder.default)(obj)


_json_encoder.default = json.JSONEncoder().default
json.JSONEncoder.default = _json_encoder