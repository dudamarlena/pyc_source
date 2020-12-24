# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/mortar/types.py
# Compiled at: 2008-12-19 12:41:15
import datetime as python_datetime
from interfaces import IFieldType, empty

class sequence(IFieldType):
    pass


class not_sequence(IFieldType):
    pass


class datetime(not_sequence):
    pass


class datetimes(sequence):
    pass


class date(not_sequence):
    pass


class dates(sequence):
    pass


class time:
    pass


class times(sequence):
    pass


class number(not_sequence):
    pass


class numbers(sequence):
    pass


class text(not_sequence):
    pass


class texts(sequence):
    pass


class reference(not_sequence):
    pass


class references(sequence):
    pass


class binary:
    pass


class binaries:
    pass


class_to_type_singular = {type(None): None, 
   python_datetime.datetime: datetime, 
   python_datetime.date: date, 
   python_datetime.time: time, 
   int: number, 
   float: number, 
   unicode: text, 
   str: binary, 
   empty: None}
class_to_type_plural = {python_datetime.datetime: datetimes, 
   python_datetime.date: dates, 
   python_datetime.time: times, 
   int: numbers, 
   float: numbers, 
   unicode: texts, 
   str: binaries}

def type(value):
    if value is empty:
        return None
    else:
        if isinstance(value, (list, tuple)):
            value = value[0]
            mapping = class_to_type_plural
        else:
            mapping = class_to_type_singular
        return mapping[value.__class__]