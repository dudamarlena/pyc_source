# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/mortar/convertors.py
# Compiled at: 2008-12-19 12:41:15
from datetime import date, datetime
from dateutil.parser import parse
from interfaces import IFieldType, empty
from time import strptime
from types import date as date_type
from types import datetime as datetime_type
from types import not_sequence
from types import number as number_type
from types import reference
from types import text as text_type
from types import texts
from types import type as type_of
from zope.component import provideAdapter
from zope.interface import classImplements
classImplements(unicode, text_type)
classImplements(int, number_type)
classImplements(float, number_type)
classImplements(date, date_type)
classImplements(datetime, datetime_type)

def to_text(str):
    return unicode(str)


def str_to_datetime(str):
    try:
        return parse(str, dayfirst=True)
    except ValueError:
        return

    return


def str_to_date(str):
    dt = str_to_datetime(str)
    return dt and dt.date()


def str_to_time(str):
    dt = str_to_datetime(str)
    return dt and dt.time()


def date_to_text(date):
    return unicode(date.strftime('%Y/%m/%d'))


def datetime_to_text(date):
    return unicode(date.strftime('%Y/%m/%d %H:%M:%S'))


def reference_to_text(ref):
    return 'Reference to ' + unicode(ref.id)


def obj_to_texts(obj):
    if text_type.providedBy(obj):
        value = obj
    else:
        value = text_type(obj)
    return (
     value,)


def sequence_to_texts(s):
    r = []
    for obj in s:
        if text_type.providedBy(obj):
            value = obj
        else:
            value = text_type(obj)
        r.append(value)

    return r


def sequence_to_sequence(s):
    if not s:
        return empty
    type = type_of(IFieldType(s[0]))
    try:
        for i in s:
            type(i)

    except TypeError:
        raise TypeError('Sequences must be of one type, could not convert %r to %r' % (
         i,
         type))

    return s


def none_to_text(v):
    return ''


def none_to_sequence(v):
    return []


provideAdapter(str_to_date, (str,), date_type)
provideAdapter(str_to_datetime, (str,), datetime_type)
provideAdapter(date_to_text, (date,), text_type)
provideAdapter(datetime_to_text, (datetime,), text_type)
provideAdapter(obj_to_texts, (IFieldType,), texts)
provideAdapter(sequence_to_texts, (tuple,), texts)
provideAdapter(sequence_to_texts, (list,), texts)
provideAdapter(sequence_to_sequence, (tuple,), IFieldType)
provideAdapter(sequence_to_sequence, (list,), IFieldType)
provideAdapter(to_text, (str,), text_type)
provideAdapter(to_text, (int,), text_type)
provideAdapter(to_text, (float,), text_type)
provideAdapter(reference_to_text, (reference,), text_type)
provideAdapter(none_to_text, (type(None),), text_type)
provideAdapter(none_to_sequence, (type(None),), texts)