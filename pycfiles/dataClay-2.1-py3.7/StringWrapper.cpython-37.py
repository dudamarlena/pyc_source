# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/dataclay/serialization/python/lang/StringWrapper.py
# Compiled at: 2019-10-28 11:50:26
# Size of source mod 2**32: 2229 bytes
""" Class description goes here. """
from io import BytesIO
import six
import dataclay.serialization.python.DataClayPythonWrapper as DataClayPythonWrapper
import dataclay.serialization.python.lang.BooleanWrapper as BooleanWrapper
import dataclay.serialization.python.lang.IntegerWrapper as IntegerWrapper
__author__ = 'Alex Barcelo <alex.barcelo@bsc.es>'
__copyright__ = '2015 Barcelona Supercomputing Center (BSC-CNS)'

class StringWrapper(DataClayPythonWrapper):
    __doc__ = 'String with different modes/encodings.'
    __slots__ = ('_mode', '_nullable')
    modes = {
     'utf-8', 'utf-16', 'binary'}

    def __init__(self, mode='utf-16', nullable=False):
        assert mode in self.modes, 'The String mode should be one in {}'.format(self.modes)
        self._mode = mode
        self._nullable = nullable

    def read(self, io_file):
        if self._nullable:
            is_not_null = BooleanWrapper().read(io_file)
            if not is_not_null:
                return
        size = IntegerWrapper(32).read(io_file)
        ba = io_file.read(size)
        if self._mode == 'utf-8':
            return ba.decode('utf-8')
        if self._mode == 'utf-16':
            return ba.decode('utf-16-be')
        if self._mode == 'binary':
            return ba
        raise TypeError('Internal mode {} not recognized'.format(self._mode))

    def write(self, io_file, value):
        if self._nullable:
            if value is None:
                BooleanWrapper().write(io_file, False)
                return
            BooleanWrapper().write(io_file, True)
        elif self._mode == 'utf-8':
            ba = value.encode('utf-8')
        else:
            if self._mode == 'utf-16':
                ba = value.encode('utf-16-be')
            else:
                if self._mode == 'binary':
                    if isinstance(value, BytesIO):
                        ba = value.getvalue()
                    elif six.PY2:
                        ba = bytes(value)
                    elif six.PY3:
                        ba = bytes(value, 'utf-8')
                else:
                    raise TypeError('Internal mode {} not recognized'.format(self._mode))
        IntegerWrapper(32).write(io_file, len(ba))
        io_file.write(ba)