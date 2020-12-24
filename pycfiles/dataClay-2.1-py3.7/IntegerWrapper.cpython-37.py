# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/dataclay/serialization/python/lang/IntegerWrapper.py
# Compiled at: 2019-10-28 11:50:26
# Size of source mod 2**32: 898 bytes
""" Class description goes here. """
from struct import Struct
import dataclay.serialization.python.DataClayPythonWrapper as DataClayPythonWrapper
__author__ = 'Alex Barcelo <alex.barcelo@bsc.es>'
__copyright__ = '2015 Barcelona Supercomputing Center (BSC-CNS)'

class IntegerWrapper(DataClayPythonWrapper):
    __doc__ = 'Multiple-size integer type.'
    __slots__ = ('_size', '_type')
    sizes = {8:Struct('!b'), 
     16:Struct('!h'), 
     32:Struct('!i'), 
     64:Struct('!q')}

    def __init__(self, size=32):
        assert size in self.sizes, 'Invalid size {:d} for integer type'.format(size)
        self._size = size
        self._type = self.sizes[size]

    def read(self, io_file):
        val = io_file.read(int(self._size / 8))
        return self._type.unpack(val)[0]

    def write(self, io_file, value):
        io_file.write(self._type.pack(value))