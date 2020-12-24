# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/ydbf/lib.py
# Compiled at: 2009-07-13 07:52:25
"""
Common lib for both reader and writer
"""
import datetime
ENCODINGS = {0: ('ascii', 'ASCII'), 1: ('cp437', 'DOS USA'), 2: ('cp850', 'DOS Multilingual'), 3: ('cp1252', 'Windows ANSI'), 4: ('mac_roman', 'Standard Macintosh'), 100: ('cp852', 'EE MS-DOS'), 101: ('cp866', 'Russian MS-DOS'), 102: ('cp865', 'Nordic MS-DOS'), 103: ('cp861', 'Icelandic MS-DOS'), 106: ('cp737', 'Greek MS-DOS (437G)'), 107: ('cp857', 'Turkish MS-DOS'), 150: ('mac_cyrillic', 'Russian Macintosh'), 151: ('mac_latin2', 'Eastern Europe Macintosh'), 152: ('mac_greek', 'Greek Macinstosh'), 200: ('cp1250', 'Windows EE'), 201: ('cp1251', 'Russian Windows'), 202: ('cp1254', 'Turkish Windows'), 203: ('cp1253', 'Greek Windows')}
REVERSE_ENCODINGS = dict([ (value[0], (code, value[1])) for (code, value) in ENCODINGS.items() ])
SIGNATURES = {2: 'FoxBase', 3: 'dBASE III', 4: 'dBASE IV', 5: 'dBASE V', 48: 'Visual FoxPro', 49: 'Visual FoxPro with AutoIncrement field', 67: 'dBASE IV with SQL table and memo file', 123: 'dBASE IV with memo file', 131: 'dBASE III with memo file', 139: 'dBASE IV with memo file', 142: 'dBASE IV with SQL table', 179: '.dbv and .dbt memo (Flagship)', 203: 'dBASE IV with SQL table and memo file', 229: 'Clipper SIX driver with SMT memo field', 245: 'FoxPro with memo field', 251: 'FoxPro'}
SUPPORTED_SIGNATURES = (
 3, 4, 5)
HEADER_FORMAT = '<B3BLHH17xB2x'
FIELD_DESCRIPTION_FORMAT = '<11sc4xBB14x'

def dbf2date(dbf_str):
    """
    Converts date from dbf-date to datetime.date
    
    Args:
        `dbf_str`:
            string in format YYYYMMDD
    """
    if dbf_str is None or not dbf_str.isdigit() or len(dbf_str) != 8:
        result = None
    else:
        result = datetime.date(int(dbf_str[:4]), int(dbf_str[4:6]), int(dbf_str[6:8]))
    return result


def date2dbf(dt):
    """
    Converts date from datetime.date to dbf-date (string in format YYYYMMDD)
    
    Args:
        `dt`:
            datetime.date instance
    """
    if not isinstance(dt, datetime.date):
        raise TypeError('Espects datetime.date instead of %s' % type(dt))
    return '%04d%02d%02d' % (dt.year, dt.month, dt.day)


def dbf2str(dbf_str):
    """
    Converts date from dbf-date to string (DD.MM.YYYY)
    
    Args:
        `dbf_str`:
            dbf-date (string in format YYYYMMDD)
    """
    if dbf_str is None or not dbf_str.isdigit() or len(dbf_str) != 8:
        result = None
    else:
        result = ('.').join(reversed((dbf_str[:4], dbf_str[4:6], dbf_str[6:8])))
    return result


def str2dbf(dt_str):
    """
    Converts from string to dbf-date (string in format YYYYMMDD)
    
    Args:
        `dt_str`:
            string in format DD.MM.YYYY
    """
    if not isinstance(dt_str, basestring):
        raise TypeError('Espects string or unicode instead of %s' % type(dt_str))
    str_l = len(dt_str)
    if str_l != 10:
        raise ValueError('Datestring must be 10 symbols (DD.MM.YYYY) length instead of %d' % str_l)
    (d, m, y) = dt_str.split('.')
    return ('').join((y, m, d))