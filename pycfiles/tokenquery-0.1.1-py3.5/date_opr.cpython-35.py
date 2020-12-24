# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-x86_64/egg/tokenquery/acceptors/core/date_opr.py
# Compiled at: 2017-01-28 16:45:09
# Size of source mod 2**32: 2426 bytes
import datetime, dateutil.parser

def date_is(token_input, operation_input):
    if 'T' in token_input:
        date1 = token_input.split('T')[0]
    else:
        date1 = token_input
    if 'T' in operation_input:
        date2 = operation_input.split('T')[0]
    else:
        date2 = operation_input
    if date1 == date2:
        return True
    return False


def date_is_after(token_input, operation_input):
    if 'T' in token_input:
        date1 = token_input.split('T')[0]
    else:
        date1 = token_input
    if 'T' in operation_input:
        date2 = operation_input.split('T')[0]
    else:
        date2 = operation_input
    if date1 > date2:
        return True
    return False


def date_is_before(token_input, operation_input):
    if 'T' in token_input:
        date1 = token_input.split('T')[0]
    else:
        date1 = token_input
    if 'T' in operation_input:
        date2 = operation_input.split('T')[0]
    else:
        date2 = operation_input
    if date1 < date2:
        return True
    return False


def date_y_is(token_input, operation_input):
    if 'T' in token_input:
        date1 = token_input.split('T')[0]
        year = date1.split('-')[0]
    else:
        year = token_input.split('-')[0]
    if year == operation_input:
        return True
    return False


def date_m_is(token_input, operation_input):
    if 'T' in token_input:
        date1 = token_input.split('T')[0]
        month = date1.split('-')[1]
    else:
        month = token_input.split('-')[1]
    if month == operation_input:
        return True
    return False


def date_d_is(token_input, operation_input):
    if 'T' in token_input:
        date1 = token_input.split('T')[0]
        day = date1.split('-')[2]
    else:
        day = token_input.split('-')[2]
    if day == operation_input:
        return True
    return False