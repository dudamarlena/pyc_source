# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/pg_python2/pg_dates.py
# Compiled at: 2018-11-30 06:03:49
# Size of source mod 2**32: 1914 bytes
import calendar
from umalqurra.hijri_date import HijriDate
import jdatetime
from datetime import datetime
import re

def split_non_alpha(string_to_split):
    ret_val = []
    arr_spl = re.split('[^a-zA-Z0-9 ]', string_to_split)
    for s in arr_spl:
        ret_val.append(s.strip())

    return ret_val


def middle_east_parsed_date(text_date, kwargs):
    """
    :param text_date:
    :param kwargs: format : %d-%m-%Y for 12-7-1397.
    :return:
    """
    dict_month_numeric = dict((v, k) for k, v in enumerate(calendar.month_name))
    dict_month_abbr_numeric = dict((v, k) for k, v in enumerate(calendar.month_abbr))
    day = -1
    month = -1
    year = -1
    default_format = ['%d', '%m', '%Y']
    tsplit = split_non_alpha(text_date)
    if 'format' in kwargs:
        format = kwargs['format']
    else:
        format = default_format
    if len(tsplit) != len(default_format):
        return
    for idx in range(0, len(tsplit)):
        item = tsplit[idx]
        if not isinstance(item, int):
            if not isinstance(item, float):
                item = item.capitalize().strip()
                if item in dict_month_numeric:
                    item = dict_month_numeric[item]
                elif item in dict_month_abbr_numeric:
                    item = dict_month_abbr_numeric[item]
        f_value = format[idx]
        if f_value == '%d':
            day = int(item)
        else:
            if f_value == '%m':
                month = int(item)
            else:
                if f_value == '%Y':
                    year = int(item)

    if month > 0:
        if day > 0:
            if year > 0:
                if year < 1410:
                    jd = jdatetime.datetime(year, month, day)
                    return jd.togregorian()
                if year < 1500:
                    um = HijriDate(year, month, day)
                    return datetime(um.year_gr, um.month_gr, um.day_gr)


def gregorian_parsed_date(text_date):
    pass