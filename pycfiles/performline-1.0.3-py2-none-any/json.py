# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/ghetzel/src/github.com/PerformLine/python-performline-client/build/lib.linux-x86_64-2.7/performline/embedded/stdlib/utils/json.py
# Compiled at: 2018-05-17 16:01:23
from __future__ import absolute_import
from datetime import datetime
import json

def json_serializer(obj):
    """JSON serializer for objects not serializable by default json code"""
    if isinstance(obj, datetime):
        serial = obj.isoformat()
        return serial
    raise TypeError('Type not serializable')


def jsonify(input, **kwargs):
    kwargs.update({'default': json_serializer})
    return json.dumps(input, **kwargs)