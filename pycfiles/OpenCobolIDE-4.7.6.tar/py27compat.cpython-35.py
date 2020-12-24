# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-build-4yaip7h6/keyring/keyring/py27compat.py
# Compiled at: 2016-12-29 05:40:26
# Size of source mod 2**32: 1008 bytes
"""
Compatibility support for Python 2.7. Remove when Python 2.7 support is
no longer required.
"""
try:
    import configparser
except ImportError:
    import ConfigParser as configparser

try:
    input = raw_input
except NameError:
    input = input

try:
    unicode_str = unicode
except NameError:
    unicode_str = str

try:
    import cPickle as pickle
except ImportError:
    import pickle

try:
    from itertools import ifilter as filter
except ImportError:
    filter = filter

def add_metaclass(metaclass):
    """Class decorator for creating a class with a metaclass."""

    def wrapper(cls):
        orig_vars = cls.__dict__.copy()
        orig_vars.pop('__dict__', None)
        orig_vars.pop('__weakref__', None)
        for slots_var in orig_vars.get('__slots__', ()):
            orig_vars.pop(slots_var)

        return metaclass(cls.__name__, cls.__bases__, orig_vars)

    return wrapper


try:
    import builtins
except ImportError:
    import __builtin__ as builtins