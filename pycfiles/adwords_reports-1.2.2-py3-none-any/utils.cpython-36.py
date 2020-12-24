# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: adwords_client/utils.py
# Compiled at: 2017-07-12 11:02:17
# Size of source mod 2**32: 615 bytes
import re, math
double_regex = re.compile('[^\\d.]+')

def process_double(x):
    """
    Transform a string having a Double to a python Float

    >>> process_double('123.456')
    123.456
    """
    x = double_regex.sub('', x)
    if x:
        return float(x)
    else:
        return 0.0


integer_regex = re.compile('[^\\d]+')

def process_integer(x):
    x = integer_regex.sub('', x)
    if x:
        return int(x)
    else:
        return 0


def float_as_cents(x):
    return max(0.01, float(math.ceil(100.0 * x)) / 100.0)


def money_as_cents(x):
    return float(x) / 1000000


def cents_as_money(x):
    return int(round(float_as_cents(x) * 1000000, 0))