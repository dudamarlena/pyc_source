# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.15-x86_64/egg/moment/api.py
# Compiled at: 2020-04-11 10:31:37
# Size of source mod 2**32: 518 bytes
"""
Simple API functionality.
"""
from .core import Moment

def date(*args):
    """Create a moment."""
    return Moment(*args)


def now():
    """Create a date from the present time."""
    return Moment.now()


def utc(*args):
    """Create a date using the UTC time zone."""
    return (Moment.utc)(*args)


def utcnow():
    """UTC equivalent to `now` function."""
    return Moment.utcnow()


def unix(timestamp, utc=False):
    """Create a date from a Unix timestamp."""
    return Moment.unix(timestamp, utc)