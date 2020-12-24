# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/Seth/Programming/input_reader/input_reader/__init__.py
# Compiled at: 2014-03-01 14:21:20
from __future__ import unicode_literals
from os.path import dirname, join
from .input_reader import InputReader
from .helpers import ReaderError, SUPPRESS, Namespace
from .files import file_safety_check, abs_file_path
from ._version import __version__
__all__ = [
 b'InputReader',
 b'ReaderError',
 b'SUPPRESS',
 b'abs_file_path',
 b'file_safety_check',
 b'range_check',
 b'include_path']
include_path = join(dirname(__file__), b'include')

def range_check(low, high, expand=False, asint=False):
    """    :py:func:`range_check` will verify that that given range has a
    *low* lower than the *high*.  If both numbers are integers, it
    will return a list of the expanded range unless *expand* is
    :py:const:`False`, in which it will just return the high and low.
    If *low* or *high* is not an integers, it will return the *low*
    and *high* values as floats.

    :argument low:
       The low value if the range to check.
    :type low: float, int
    :argument high:
       The high value if the range to check.
    :type high: float, int
    :keyword expand:
        If :py:obj:`True` and both *low* or *high* are integers, then
        :py:func:`range_check` will return the range of integers between
        *low* and *high*, inclusive. Otherwise, :py:func:`range_check`
        just returns *low* and *high*.
    :type expand: bool, optional
    :keyword asint:
        If *expand* is :py:obj:`False`, this will attempt to return the
        *low* and *high* as integers instead of floats.
    :type expand: bool, optional
    :rtype:
        See the explanation of *expand*.
    :exception:
        * :py:exc:`ValueError`: *low* > *high*.
        * :py:exc:`ValueError`: *low* or *high* cannot be converted to a
          :py:obj:`float`.
    """
    low = float(low)
    high = float(high)
    if low >= high:
        raise ValueError(b'low >= high')
    if (expand or asint) and int(low) == low and int(high) == high:
        if expand:
            return tuple(range(int(low), int(high) + 1))
        else:
            return (
             int(low), int(high))

    else:
        return (
         low, high)