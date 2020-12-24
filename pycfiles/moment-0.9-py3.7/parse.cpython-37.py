# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.15-x86_64/egg/moment/parse.py
# Compiled at: 2020-04-11 10:31:37
# Size of source mod 2**32: 3352 bytes
from datetime import datetime
import dateparser
from .utils import STRING_TYPES

def parse_date_and_formula(*args):
    """Doesn't need to be part of core Moment class."""
    date, formula = _parse_arguments(*args)
    parse_settings = {'PREFER_DAY_OF_MONTH': 'first'}
    if date and formula:
        if isinstance(date, datetime):
            return (
             date, formula)
        if '%' not in formula:
            formula = parse_js_date(formula)
        date = dateparser.parse(date, date_formats=[formula], settings=parse_settings)
    else:
        if isinstance(date, list) or isinstance(date, tuple):
            if len(date) == 1:
                date = [date[0], 1, 1]
            date = datetime(*date)
        else:
            if isinstance(date, STRING_TYPES):
                date = dateparser.parse(date, settings=parse_settings)
                formula = '%Y-%m-%dT%H:%M:%S'
    return (
     date, formula)


def _parse_arguments(*args):
    """Because I'm not particularly Pythonic."""
    formula = None
    if len(args) == 1:
        date = args[0]
    else:
        if len(args) == 2:
            date, formula = args
        else:
            date = args
    return (
     date, formula)


def parse_js_date(date):
    """
    Translate the easy-to-use JavaScript format strings to Python's cumbersome
    strftime format. Also, this is some ugly code -- and it's completely
    order-dependent.
    """
    if 'A' in date:
        date = date.replace('A', '%p')
    else:
        if 'a' in date:
            date = date.replace('a', '%P')
        elif 'HH' in date:
            date = date.replace('HH', '%H')
        else:
            if 'H' in date:
                date = date.replace('H', '%k')
            else:
                if 'hh' in date:
                    date = date.replace('hh', '%I')
                else:
                    if 'h' in date:
                        date = date.replace('h', '%l')
                    elif 'mm' in date:
                        date = date.replace('mm', '%min')
                    else:
                        if 'm' in date:
                            date = date.replace('m', '%min')
                        elif 'ss' in date:
                            date = date.replace('ss', '%S')
                        else:
                            if 's' in date:
                                date = date.replace('s', '%S')
                            else:
                                if 'SSS' in date:
                                    date = date.replace('SSS', '%3')
                                if 'YYYY' in date:
                                    date = date.replace('YYYY', '%Y')
                                else:
                                    if 'YY' in date:
                                        date = date.replace('YY', '%y')
                            if 'MMMM' in date:
                                date = date.replace('MMMM', '%B')
                            else:
                                if 'MMM' in date:
                                    date = date.replace('MMM', '%b')
                                else:
                                    if 'MM' in date:
                                        date = date.replace('MM', '%m')
                                    else:
                                        if 'M' in date:
                                            date = date.replace('M', '%m')
                                        if 'dddd' in date:
                                            date = date.replace('dddd', '%A')
                                        else:
                                            if 'ddd' in date:
                                                date = date.replace('ddd', '%a')
                                            else:
                                                if 'dd' in date:
                                                    date = date.replace('dd', '%w')
                                                else:
                                                    if 'd' in date:
                                                        date = date.replace('d', '%u')
        if 'DDDD' in date:
            date = date.replace('DDDD', '%j')
        else:
            if 'DDD' in date:
                date = date.replace('DDD', '%j')
            else:
                if 'DD' in date:
                    date = date.replace('DD', '%d')
                else:
                    if 'D' in date:
                        date = date.replace('D', '%d')
                    else:
                        if 'L' in date:
                            date = date.replace('L', '%Y-%m-%dT%H:%M:%S')
                        if '%min' in date:
                            date = date.replace('%min', '%M')
                        return date