# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build\bdist.win32\egg\pyhexad\table_helpers.py
# Compiled at: 2014-12-08 16:27:39
import numpy as np
from type_helpers import parse_dtype

def parse_col_names(s):
    """
    When passed a string containing a comma-separated list of column names,
    this function returns a Python list of strings.
    """
    if not isinstance(s, str):
        raise TypeError('String expected')
    slen = len(s)
    if slen == 0:
        raise Exception('Empty string')
    lst = []
    low = 0
    high = 0
    while high < slen:
        high += 1
        if high == slen:
            if high == low:
                raise Exception('Empty column name found.')
            lst.append(s[low:high])
            break
        if s[high] == ',':
            if s[(high - 1)] == '\\':
                continue
            elif high == low:
                raise Exception('Empty column name found.')
            else:
                lst.append(s[low:high])
                low = high + 1
        else:
            continue

    for i in range(len(lst)):
        lst[i] = lst[i].replace('\\,', ',')

    return lst


def parse_heading(s):
    """
    When passed a correctly formatted header, this function returns a list with
    an even number of elements. Even entries contain column names and odd
    entries contain type decriptions. The latter must be verified separately.
    """
    if not isinstance(s, str):
        raise TypeError('String expected')
    slen = len(s)
    if slen == 0:
        raise Exception('Empty heading')
    lst = []
    low = 0
    high = 0
    while high < slen:
        high += 1
        if high == slen:
            if high == low:
                raise Exception('Empty value in heading found.')
            lst.append(s[low:high])
            break
        if s[high] == ',':
            if s[(high - 1)] == '\\':
                continue
            elif high == low:
                raise Exception('Empty value in heading found.')
            else:
                lst.append(s[low:high])
                low = high + 1
        else:
            continue

    if len(lst) == 0 or not len(lst) % 2 == 0:
        raise Exception('Invalid value count in heading.')
    for i in range(0, len(lst), 2):
        lst[i] = lst[i].replace('\\,', ',')
        if lst[(i + 1)].count(':') > 1:
            raise Exception('Invalid type specification in heading')

    return lst


def dtype_from_heading(s):
    """
    Construct the Numpy dtype from a string description of the form
    Name1,Type1[:Fill1],...,NameN,TypeN[:FillN]
    """
    lst = parse_heading(str(s))
    check = set()
    descr = []
    for i in range(0, len(lst), 2):
        f = lst[i]
        check.add(f)
        t = lst[(i + 1)]
        descr.append((f, parse_dtype(t)))

    if len(check) != len(lst) / 2:
        raise Exception('Duplicate column name in heading found.')
    return np.dtype(descr)