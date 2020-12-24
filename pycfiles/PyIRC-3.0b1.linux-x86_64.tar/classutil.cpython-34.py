# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/lib64/python3.4/site-packages/PyIRC/util/classutil.py
# Compiled at: 2015-10-08 05:15:50
# Size of source mod 2**32: 453 bytes
"""Utilities for class metaprogramming and related purposes."""

def get_all_subclasses(cls):
    """Generator for all subclasses for a given class."""
    for subclass in cls.__subclasses__():
        yield subclass
        yield from get_all_subclasses(subclass)