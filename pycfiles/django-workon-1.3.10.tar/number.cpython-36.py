# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/dalou/www/PACKAGES/WORKON/workon/utils/number.py
# Compiled at: 2018-03-15 11:27:01
# Size of source mod 2**32: 1083 bytes
import re
__all__ = [
 'numbers', 'rate_repr', 'to_int', 'to_float', 'str_to_float', 'is_float']

def numbers(value):
    if value is not None:
        value = str(value)
        if value:
            value = re.sub('^(-?\\d+)(\\d{3})', '\\g<1> \\g<2>', value)
    return value


def rate_repr(value, decimal=2):
    try:
        value = round(float(value), decimal)
        if value > 0:
            return f"+{value}"
        else:
            if value < 0:
                return (f"{value}")
            return f"~{value}"
    except:
        return 0


def to_int(value):
    number = ''
    for c in value[::-1]:
        if c.isdigit():
            number += c

    return int(number)


def to_float(value, default=None):
    try:
        return float(value.replace(',', '.').replace(' ', ''))
    except:
        return default


def str_to_float(str, default=None):
    try:
        return float(str.replace(',', '.').strip())
    except:
        return default


def is_float(var):
    try:
        float(var)
    except (TypeError, ValueError):
        return False
    else:
        return True