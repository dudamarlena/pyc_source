# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/jsonish/pythonjson.py
# Compiled at: 2009-07-28 07:04:28
import datetime
from jsonish.json import JSON
from decimal import Decimal

def date_to_dict(obj):
    return {'year': obj.year, 'month': obj.month, 'day': obj.day}


def date_from_dict(obj):
    return datetime.date(obj['year'], obj['month'], obj['day'])


def time_to_dict(obj):
    return {'hour': obj.hour, 'minute': obj.minute, 'second': obj.second, 'microsecond': obj.microsecond}


def time_from_dict(obj):
    return datetime.time(obj['hour'], obj['minute'], obj['second'], obj['microsecond'])


def datetime_to_dict(obj):
    return {'year': obj.year, 'month': obj.month, 'day': obj.day, 'hour': obj.hour, 'minute': obj.minute, 'second': obj.second, 'microsecond': obj.microsecond}


def datetime_from_dict(obj):
    return datetime.datetime(obj['year'], obj['month'], obj['day'], obj['hour'], obj['minute'], obj['second'], obj['microsecond'])


def decimal_from_dict(obj):
    return Decimal(obj['value'])


def decimal_to_dict(obj):
    return {'value': str(obj)}


json = JSON()
json.register_type(datetime.date, date_to_dict, date_from_dict, 'date')
json.register_type(datetime.time, time_to_dict, time_from_dict, 'time')
json.register_type(datetime.datetime, datetime_to_dict, datetime_from_dict, 'datetime')
json.register_type(Decimal, decimal_to_dict, decimal_from_dict, 'decimal')
dumps = json.dumps
loads = json.loads
decode_mapping = {'datetime': datetime_from_dict, 
   'date': date_from_dict, 
   'time': time_from_dict, 
   'decimal': decimal_from_dict}
encode_mapping = {datetime.datetime: (
                     'datetime', datetime_to_dict), 
   datetime.date: (
                 'date', date_to_dict), 
   datetime.time: (
                 'time', time_to_dict), 
   Decimal: (
           'decimal', decimal_to_dict)}

def encode_obj_to_dict(obj, mapping=encode_mapping):
    encode = mapping.get(type(obj))
    if encode is None:
        return obj
    else:
        d = encode[1](obj)
        d['__type__'] = encode[0]
        return d


def decode_obj_from_dict(d, mapping=decode_mapping):
    if not isinstance(d, dict):
        return d
    else:
        name = d.get('__type__')
        decode = mapping.get(name, None)
        if decode is None:
            return d
        return decode(d)


def encode_to_dict(obj, mapping=encode_mapping):
    if isinstance(obj, dict):
        return dict([ (k, encode_to_dict(v, mapping)) for (k, v) in obj.items() ])
    else:
        if isinstance(obj, list):
            return [ encode_to_dict(v, mapping) for v in obj ]
        if isinstance(obj, tuple):
            return [ encode_to_dict(v, mapping) for v in obj ]
        return encode_obj_to_dict(obj, mapping)


def decode_from_dict(d, mapping=decode_mapping):
    if isinstance(d, dict) and '__type__' not in d:
        return dict([ (k, decode_from_dict(v, mapping)) for (k, v) in d.items() ])
    else:
        if isinstance(d, list):
            return [ decode_from_dict(v, mapping) for v in d ]
        return decode_obj_from_dict(d, mapping)