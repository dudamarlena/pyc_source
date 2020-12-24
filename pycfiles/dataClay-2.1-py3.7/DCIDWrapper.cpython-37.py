# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/dataclay/serialization/python/lang/DCIDWrapper.py
# Compiled at: 2019-10-28 11:50:26
# Size of source mod 2**32: 1044 bytes
""" Class description goes here. """
import uuid
import dataclay.serialization.python.DataClayPythonWrapper as DataClayPythonWrapper
import dataclay.serialization.python.lang.BooleanWrapper as BooleanWrapper
__author__ = 'Alex Barcelo <alex.barcelo@bsc.es>'
__copyright__ = '2015 Barcelona Supercomputing Center (BSC-CNS)'

class DCIDWrapper(DataClayPythonWrapper):
    __doc__ = 'dataClay UUID (straightforward serialization).'
    __slots__ = ('_nullable', )

    def __init__(self, nullable=False):
        self._nullable = nullable

    def read(self, io_file):
        if self._nullable:
            present = BooleanWrapper().read(io_file)
            if not present:
                return
        return uuid.UUID(bytes=(str(io_file.read(16))))

    def write(self, io_file, value):
        if self._nullable:
            if value is None:
                BooleanWrapper().write(io_file, False)
                return
            BooleanWrapper().write(io_file, True)
        io_file.write(value.get_bytes())