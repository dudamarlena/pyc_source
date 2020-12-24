# uncompyle6 version 3.6.7
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /usr/lib64/python3.4/site-packages/PyIRC/util/classutil.py
# Compiled at: 2015-10-08 05:15:50
# Size of source mod 2**32: 453 bytes
__doc__ = 'Utilities for class metaprogramming and related purposes.'

def get_all_subclasses(cls):
    """Generator for all subclasses for a given class."""
    for subclass in cls.__subclasses__():
        yield subclass
        yield from get_all_subclasses(subclass)