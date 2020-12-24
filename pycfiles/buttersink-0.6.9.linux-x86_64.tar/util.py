# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python2.7/dist-packages/buttersink/util.py
# Compiled at: 2018-05-28 12:06:50
""" Utilities for btrfs and buttersink. """
from __future__ import division
import math, pprint, traceback

def pretty(obj):
    """ Return pretty representation of obj. """
    return pprint.pformat(obj)


def humanize(number):
    """ Return a human-readable string for number. """
    units = ('bytes', 'KiB', 'MiB', 'GiB', 'TiB')
    base = 1024
    if number is None:
        return
    else:
        pow = int(math.log(number, base)) if number > 0 else 0
        pow = min(pow, len(units) - 1)
        mantissa = number / base ** pow
        return '%.4g %s' % (mantissa, units[pow])


def displayTraceBack():
    """ Display traceback useful for debugging. """
    tb = traceback.format_stack()
    return '\n' + ('').join(tb[:-1])


class DefaultList(list):
    """ list that automatically inserts None for missing items. """

    def __setitem__(self, index, value):
        """ Set item. """
        if len(self) > index:
            return list.__setitem__(self, index, value)
        else:
            if len(self) < index:
                self.extend([None] * (index - len(self)))
            list.append(self, value)
            return

    def __getitem__(self, index):
        """ Set item. """
        if index >= len(self):
            return None
        else:
            return list.__getitem__(self, index)