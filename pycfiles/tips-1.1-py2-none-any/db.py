# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/ab/projects/python/tips/build/lib/tips/db.py
# Compiled at: 2015-12-28 12:23:00
"""Database module for tips.py"""
import json, os
from . import dateapi
db_file = os.path.join(os.path.expanduser('~'), '.tips_db')

def _init():
    """Load db, create if nonexistent."""
    try:
        load()
    except IOError:
        file = open(db_file, 'w')
        file.close()
        load()


def load():
    """Get JSON data from db. Return {} if empty. Called on import."""
    global data
    with open(db_file, 'r') as (file):
        try:
            data = json.load(file)
        except ValueError:
            data = {}


def save():
    """Save data as JSON in db."""
    with open(db_file, 'w') as (file):
        json.dump(data, file)


def get_value(date):
    """Get value for corresponding key. Return None if none."""
    try:
        return data[date]
    except KeyError:
        return

    return


def get_item(date):
    """Return 2-tuple with key, value pair. Return None if none."""
    try:
        return (
         date, data[date])
    except KeyError:
        return

    return


def get_range_dates(start, end):
    """Get range of dates, match in data, and return as a list."""
    range = dateapi.range(start, end)
    dates = [ i for i in range if i in data.keys() ]
    if dates == []:
        return
    else:
        return dates
        return


def get_range_values(start, end):
    """Get values under range of dates."""
    results = get_range(start, end)
    try:
        return zip(*results)[1]
    except TypeError:
        return

    return


def get_range(start, end):
    """Return range of date, amount pairs."""
    list = []
    dates = get_range_dates(start, end)
    if dates is None:
        return
    else:
        for i in dates:
            list.append((i, get_value(i)))

        return list
        return


def get_all():
    """Return generator with date, value pairs for every record in db."""
    for date, value in data.iteritems():
        yield (
         date, value)


def add(date, amount):
    """Increase by amount or set to amount if nonexistent."""
    if amount < 0:
        return False
    try:
        data[date] += amount
    except KeyError:
        data[date] = amount


def reduce(date, amount):
    """Reduce by amount. Return False if nonexistent or new amount less than 0."""
    try:
        if data[date] - amount < 0:
            return False
        else:
            if data[date] - amount == 0:
                del data[date]
                return
            data[date] -= amount
            return True

    except KeyError:
        return False

    return


def replace(date, amount):
    """
    Replace value and create if nonexistent.
    Return False if less than 0, delete record if 0.
    """
    if amount > 0:
        data[date] = amount
        return True
    if amount < 0:
        return False
    try:
        del data[date]
    except KeyError:
        pass


if __name__ != '__main__':
    _init()