# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/faamtools/__init__.py
# Compiled at: 2016-02-08 12:55:12
# Size of source mod 2**32: 1166 bytes
from .version import __version__
__all__ = ['ObsData', 'DsFld', 'FaamFld']

class ObsData:
    __doc__ = 'Generic class for storing several fields of observational data.\n\n    Contains methods `__init__` and `__call__` for initialising and adding\n    fields to this class.\n    '

    def __init__(self, **kwds):
        self.__dict__.update(kwds)

    def __call__(self, **kwds):
        self.__dict__.update(kwds)


class DsFld:
    __doc__ = "A class for storing dropsonde data.\n\n    Contains several attributes:\n        raw: array-like, 'raw' data\n        fil: array-like, 'filtered' data\n        units: string, units\n        long_name: string, name\n    "

    def __init__(self, raw=None, fil=None, units='', long_name=''):
        self.raw = raw
        self.fil = fil
        self.units = units
        self.long_name = long_name


class FaamFld:
    __doc__ = 'A class for storing core FAAM aircraft data.\n\n    Contains several attributes:\n        val: array-like, data values\n        units: str, units\n        long_name: str, name\n    '

    def __init__(self, val=None, units='', long_name=''):
        self.val = val
        self.units = units
        self.long_name = long_name