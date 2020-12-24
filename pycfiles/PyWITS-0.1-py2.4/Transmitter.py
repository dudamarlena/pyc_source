# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.3-i386/egg/PyWITS/Transmitter.py
# Compiled at: 2008-05-02 02:31:14
from PyWITS.Objects.DataRecord import DataRecord
from PyWITS import Globals

class Transmitter:
    __module__ = __name__

    def __init__(self, device, mode=0):
        self.device = device
        self.mode = mode

    def write(self, data_record):
        if not isinstance(data_record, DataRecord):
            return ValueError('This is not valid data:', data_record)
        print repr(data_record.serialize())
        self.device.write(data_record.serialize())