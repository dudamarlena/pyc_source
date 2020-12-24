# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/coils/foundation/alchemy/base.py
# Compiled at: 2012-10-12 07:02:39
import pprint
from sqlalchemy import *
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime, date
from pytz import timezone
Base = declarative_base()

class CoilsORMKVCException(Exception):
    pass


class KVC(object):

    def take_values(self, values, keymap):
        if values is None:
            raise 'Cannot take values from None'
        if not isinstance(values, dict):
            values = values.__dict__
        for key in values:
            (k, v) = self.translate_key(key, values[key], keymap)
            if k is not None:
                if hasattr(self, k):
                    try:
                        setattr(self, k, v)
                    except AttributeError, e:
                        raise CoilsORMKVCException(('Unable to set attribute "{0}" on entity {1}').format(k, self))

        return

    @staticmethod
    def translate_key(key, value, keymap):
        if keymap is None:
            return (key, value)
        else:
            key = key.lower()
            if key in keymap:
                x = keymap[key]
                if x is None:
                    return (None, None)
                key = x[0]
                if len(x) > 1:
                    t = x[1]
                    if t == 'int':
                        if value:
                            value = int(str(value))
                        else:
                            value = None
                    elif t == 'date':
                        if value is None:
                            value = None
                        elif isinstance(value, datetime):
                            value = value.replace(tzinfo=timezone('UTC'))
                        elif isinstance(value, date):
                            value = value
                        elif isinstance(value, basestring):
                            if len(value) == 0:
                                value = None
                            elif len(value) == 10:
                                value = datetime(int(value[0:4]), int(value[5:7]), int(value[8:10]), tzinfo=timezone('UTC'))
                            elif len(value) == 16 or len(value) == 19:
                                value = datetime(int(value[0:4]), int(value[5:7]), int(value[8:10]), int(value[11:13]), int(value[14:16]), tzinfo=timezone('UTC'))
                            else:
                                raise Exception('Invalid string format for datetime conversion')
                        elif isinstance(value, int):
                            value = datetime.utcfromtimestamp(value)
                        else:
                            raise Exception(('Unable to translate date/time value: {0}').format(value))
                    elif t == 'csv':
                        if isinstance(value, list):
                            pass
                        elif isinstance(value, basestring):
                            value = value.split(x[2])
                        else:
                            raise Exception('Cannot transform type to CSV value')
                        value = unicode(x[2]).join([ unicode(o.strip()) for o in value ])
                if value is None:
                    if len(x) == 3:
                        value = x[2]
            return (
             key, value)

    @staticmethod
    def translate_dict(values, keymap):
        result = {}
        for key in values:
            (k, v) = KVC.translate_key(key, values[key], keymap)
            if k is not None:
                result[k] = v

        return result

    @staticmethod
    def subvalues_for_key(values, keys, default=[]):
        for key in keys:
            if key in values:
                x = values[key]
                break
        else:
            x = default

        return x

    @staticmethod
    def keyed_values(values_list, key_value):
        if not isinstance(values_list, list):
            raise Exception('Provided values is not a list')
        else:
            if len(values_list) == 0:
                return {}
            else:
                first = values_list[0]
                if isinstance(key_value, list):
                    for candidate in key_value:
                        if candidate in first:
                            key_value = candidate
                            break
                    else:
                        key_value = None
                else:
                    if key_value not in first:
                        key_value = None
                    if key_value is None:
                        raise Exception('No specified key value present in values')
                    values = {}
                    for value in values_list:
                        if key_value in value:
                            values[value[key_value]] = value

                    return values
                return