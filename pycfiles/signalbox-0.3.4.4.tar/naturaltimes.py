# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/ben/dev/signalbox/signalbox/models/naturaltimes.py
# Compiled at: 2014-08-27 19:26:12
from signalbox.utilities.delta_time import NTime

def parse_natural_date(date_str):
    """Date/time as a str -> (datetime or None, error string or None)"""
    ntime = NTime().parser
    try:
        return (
         ntime.parseString(date_str).datetime, None)
    except Exception as e:
        return (
         None, date_str + ': ' + unicode(e))

    return