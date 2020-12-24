# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
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