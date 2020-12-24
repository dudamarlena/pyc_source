# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/linseed/util.py
# Compiled at: 2011-05-31 11:44:21


def pct(val):
    """Convert a value to an integer percentage.
    """
    return int(val * 100)


def div(num, den):
    """A "safe" divide which returns 0 on zero-division.
    """
    try:
        return float(num) / den
    except ZeroDivisionError:
        return 0


class Quantity(object):
    """A value along with its units.

    Args:
      * value: The numeric value of the quantity.
      * unit: The units of the quantity (string).
    """

    def __init__(self, value, unit):
        self.value = value
        self.unit = unit