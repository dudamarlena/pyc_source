# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/val/Projects/workon/mpro/doozdev/backend/restful-backend/apps/geoware/management/utils/common.py
# Compiled at: 2017-01-27 09:53:00
# Size of source mod 2**32: 1408 bytes
import os, sys, resource
from progressbar.widgets import SamplesMixin
from django.utils.encoding import smart_str

def parse_data(content):
    """
    Return a file or content one line at a time.
    """
    for line in content:
        line = line.strip()
        if not len(line) < 1:
            if line.strip()[0] == '#':
                continue
            yield [e.strip() for e in line.split('\t')]


def get_float(item, index):
    """
    Given an record list & an index, it returns a float or 0.0.
    """
    value = 0.0
    try:
        value = float(smart_str(item[index].strip()))
    except:
        pass

    return value


def get_int(item, index):
    """
    Given an record list & an index, it returns an int or 0.
    """
    value = 0
    try:
        value = int(smart_str(item[index].strip()))
    except:
        pass

    return value


def get_str(item, index):
    """
    Given an record list & an index, it returns a str or ''.
    """
    value = ''
    try:
        value = smart_str(item[index].strip())
    except:
        pass

    return value


class MemoryUsage(SamplesMixin):
    __doc__ = '\n    Widget for showing the amount of memory used by a command.\n    '

    def __call__(self, progress, data):
        value = int(resource.getrusage(resource.RUSAGE_SELF).ru_maxrss)
        value = value // 1000000
        output = 'Mem Usage: {mem} MB |'.format(mem=value)
        return output