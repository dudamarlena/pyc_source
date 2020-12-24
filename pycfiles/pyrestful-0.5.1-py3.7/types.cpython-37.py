# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/pyrestful/types.py
# Compiled at: 2019-03-15 22:40:33
# Size of source mod 2**32: 1873 bytes
import sys
from datetime import date
boolean = str
if sys.version_info > (3, ):
    long = int
    unicode = str
    str = bytes

def convert_primitive(value):
    if isinstance(value, unicode):
        return value
    if isinstance(value, str):
        value = unicode(value, 'utf-8')
        if value.isdigit():
            return long(value)
        if value.isalnum():
            if value.upper() == 'TRUE':
                return True
            if value.upper() == 'FALSE':
                return False
            return value


def convert(value, data_type):
    """ Convert / Cast function """
    if issubclass(data_type, str):
        if value.upper() not in ('FALSE', 'TRUE'):
            return value.decode('utf-8')
    elif issubclass(data_type, unicode):
        return convert_primitive(value)
        if issubclass(data_type, int):
            return int(value)
        if issubclass(data_type, long):
            return long(value)
        if issubclass(data_type, float):
            return float(value)
        if issubclass(data_type, boolean) and value.upper() in ('FALSE', 'TRUE'):
            if str(value).upper() == 'TRUE':
                return True
            if str(value).upper() == 'FALSE':
                return False
    else:
        return value