# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: D:\BuildAgent\work\test/iobjectspy/rpc\process.py
# Compiled at: 2019-12-31 04:09:05
# Size of source mod 2**32: 1336 bytes
from iobjectspy.enums import PixelFormat
__all__ = ['Tile', 'ProcessInfo']

class Tile:

    def __init__(self, values, no_data_value=None, bands=1, pixel=None):
        self.values = values
        self.no_data_value = no_data_value
        self.bands = bands
        self.pixel = PixelFormat._make(pixel)

    def rows(self):
        if self.values:
            if self.values.ndim == 2:
                return self.values.shape[0]
            if self.values.ndim == 3:
                return self.values.shape[1]
            raise ValueError('Unsupported array, only support 2 or 3 dim array')
        else:
            return

    def cols(self):
        if self.values:
            if self.values.ndim == 2:
                return self.values.shape[1]
            if self.values.ndim == 3:
                return self.values.shape[2]
            raise ValueError('Unsupported array, only support 2 or 3 dim array')
        else:
            return


class ProcessInfo:

    def __init__(self, py_code, entry_class, kvargs):
        self.py_code = py_code
        self.entry_class = entry_class
        self.kvargs = dict()
        if kvargs is not None:
            if isinstance(kvargs, dict):
                for name, value in kvargs.items():
                    self.kvargs[name] = value