# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/denny/project/picme/aiommy/build/lib/aiommy/json.py
# Compiled at: 2017-11-20 03:41:06
# Size of source mod 2**32: 540 bytes
import datetime, json
from aiommy import dateutils

def dumps(data, indent=None):

    def handler(entity):
        if isinstance(entity, datetime.datetime):
            return dateutils.to_iso(entity)
        if isinstance(entity, bytes):
            return entity.decode('utf-8')
        raise NotImplementedError('\n            You should implement method `dumps(self, data)`\n            in your view class\n            and override default json handler\n        ')

    return json.dumps(data, default=handler, indent=indent)