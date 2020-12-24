# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /private/var/folders/70/_7dmwj6x12q099dhb0z0p7p80000gn/T/pycharm-packaging/djangorestframework/rest_framework/utils/humanize_datetime.py
# Compiled at: 2018-05-14 04:48:23
# Size of source mod 2**32: 1285 bytes
"""
Helper functions that convert strftime formats into more readable representations.
"""
from rest_framework import ISO_8601

def datetime_formats(formats):
    format = ', '.join(formats).replace(ISO_8601, 'YYYY-MM-DDThh:mm[:ss[.uuuuuu]][+HH:MM|-HH:MM|Z]')
    return humanize_strptime(format)


def date_formats(formats):
    format = ', '.join(formats).replace(ISO_8601, 'YYYY[-MM[-DD]]')
    return humanize_strptime(format)


def time_formats(formats):
    format = ', '.join(formats).replace(ISO_8601, 'hh:mm[:ss[.uuuuuu]]')
    return humanize_strptime(format)


def humanize_strptime(format_string):
    mapping = {'%Y':'YYYY', 
     '%y':'YY', 
     '%m':'MM', 
     '%b':'[Jan-Dec]', 
     '%B':'[January-December]', 
     '%d':'DD', 
     '%H':'hh', 
     '%I':'hh', 
     '%M':'mm', 
     '%S':'ss', 
     '%f':'uuuuuu', 
     '%a':'[Mon-Sun]', 
     '%A':'[Monday-Sunday]', 
     '%p':'[AM|PM]', 
     '%z':'[+HHMM|-HHMM]'}
    for key, val in mapping.items():
        format_string = format_string.replace(key, val)

    return format_string