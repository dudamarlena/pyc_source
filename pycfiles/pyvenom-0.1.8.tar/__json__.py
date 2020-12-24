# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/Larco/Documents/Github/pyvenom/framework/venom/monkeypatches/__json__.py
# Compiled at: 2016-04-26 14:29:46
from json import JSONEncoder
import datetime, time

def _default(self, obj):
    if isinstance(obj, datetime.datetime):
        timestamp = time.mktime(obj.timetuple())
        return timestamp
    if hasattr(obj, '__json__'):
        return getattr(obj, '__json__')()
    return obj


_default.default = JSONEncoder().default
JSONEncoder.default = _default