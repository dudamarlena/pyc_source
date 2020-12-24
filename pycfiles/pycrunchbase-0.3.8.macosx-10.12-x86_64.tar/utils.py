# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python2.7/site-packages/pycrunchbase/resource/utils.py
# Compiled at: 2017-01-13 23:45:16
from datetime import datetime

def safe_int(int_like):
    try:
        return int(int_like)
    except TypeError:
        return

    return


def parse_date(datelike):
    """Helper for parsing dates in Organization properties"""
    try:
        return datetime.strptime(datelike, '%Y-%m-%d')
    except ValueError:
        return datelike