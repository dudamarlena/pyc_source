# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-universal/egg/picalo/Number.py
# Compiled at: 2010-08-03 16:21:17
import decimal, sys
__all__ = [
 'number']

class number(decimal.Decimal):
    """A number with a decimal point.  This number does correct math while the 
     Python float type contains rounding errors in math."""

    def __new__(cls, value='0', context=None):
        """Creates a new number."""
        if isinstance(value, float):
            return decimal.Decimal.__new__(cls, str(value), context)
        return decimal.Decimal.__new__(cls, value, context)

    def __repr__(self):
        """Returns a string representation of this number"""
        return str(self)

    def __pg_repr__(self):
        """Required for PygreSQL driver"""
        return self


def _convert_other(*args, **kargs):
    """Converts other to a number object"""
    if len(args) == 0:
        return None
    else:
        other = args[0]
        if isinstance(other, decimal.Decimal):
            return other
        if isinstance(other, (str, unicode)) and other == '':
            return number()
        if isinstance(other, (int, long, str, unicode, float)):
            return number(other)
        return NotImplemented


decimal._convert_other = _convert_other