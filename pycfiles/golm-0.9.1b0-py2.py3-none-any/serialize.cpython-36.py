# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/prihodad/Documents/projects/visitor/golm/golm/core/serialize.py
# Compiled at: 2018-04-15 14:00:29
# Size of source mod 2**32: 455 bytes
import dateutil.parser

def json_deserialize(obj):
    if obj.get('__type__') == 'datetime':
        return dateutil.parser.parse(obj.get('value'))
    else:
        return obj


def json_serialize(obj):
    from datetime import datetime
    if isinstance(obj, datetime):
        return {'__type__':'datetime', 
         'value':obj.isoformat()}
    raise TypeError('Error saving entity value. Type %s not serializable: %s' % (type(obj), obj))