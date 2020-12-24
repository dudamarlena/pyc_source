# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/dataclay/serialization/python/lang/VLQIntegerWrapper.py
# Compiled at: 2019-10-28 11:50:26
# Size of source mod 2**32: 1257 bytes
""" Class description goes here. """
import dataclay.serialization.python.DataClayPythonWrapper as DataClayPythonWrapper
from six import int2byte
__author__ = 'Alex Barcelo <alex.barcelo@bsc.es>'
__copyright__ = '2015 Barcelona Supercomputing Center (BSC-CNS)'

class VLQIntegerWrapper(DataClayPythonWrapper):
    __doc__ = 'Variable Length Quantity.'
    __slots__ = ()

    def __init__(self):
        pass

    def read(self, io_file):
        value = 0
        while 1:
            b = ord(io_file.read(1))
            value = (value << 7) + (b & 127)
            if b & 128 == 0:
                return value

    def write(self, io_file, value):
        if value == 0:
            io_file.write(b'\x00')
            return
        values = []
        while value > 0:
            values.append(value & 127)
            value >>= 7

        for b in reversed(values[1:]):
            io_file.write(int2byte(128 | b))

        io_file.write(int2byte(values[0]))