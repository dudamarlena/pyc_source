# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.11-intel/egg/utils/common.py
# Compiled at: 2016-08-05 06:53:55
import datetime
from app import db, CobraAuth

def convert_timestamp(stamp):
    """returns a datetime.date object off a timestamp"""
    date_shards = stamp.split()
    date_shards = date_shards[0].split('-')
    date_shards = [ x.lstrip('0') for x in date_shards ]
    processed_date = datetime.date(int(date_shards[0]), int(date_shards[1]), int(date_shards[2]))
    return processed_date


def convert_time(seconds):
    one_minute = 60
    minute = seconds / one_minute
    if minute == 0:
        return str(seconds % one_minute) + "'"
    else:
        return str(minute) + "''" + str(seconds % one_minute) + "'"


def convert_number(number):
    if number is None or number == 0:
        return 0
    number = int(number)
    return ('{:20,}').format(number)


def verify_key(key):
    """verify api key"""
    auth = CobraAuth.query.filter_by(key=key).first()
    return auth is not None