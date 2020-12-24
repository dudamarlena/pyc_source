# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/dataclay/serialization/python/lang/NotImplementedType.py
# Compiled at: 2019-10-28 11:50:26
# Size of source mod 2**32: 585 bytes
""" Class description goes here. """
import dataclay.serialization.python.DataClayPythonWrapper as DataClayPythonWrapper
__author__ = 'Alex Barcelo <alex.barcelo@bsc.es>'
__copyright__ = '2015 Barcelona Supercomputing Center (BSC-CNS)'

class NotImplementedType(DataClayPythonWrapper):
    __slots__ = ()

    def __init__(self):
        pass

    def read(self, io_file):
        raise NotImplementedError('Trying to deserialize something not implemented')

    def write(self, io_file, value):
        raise NotImplementedError('Trying to serialize something not implemented')