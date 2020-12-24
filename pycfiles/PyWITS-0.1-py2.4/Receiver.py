# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.3-i386/egg/PyWITS/Receiver.py
# Compiled at: 2008-05-02 02:41:05
from PyWITS import Globals
from PyWITS.Objects.DataRecord import DataRecord

def WITS0(func):

    def inner_func(*args, **kwargs):
        import re
        obj = args[0]
        if obj.mode == 0:
            pass
        data = func(*args, **kwargs)
        if obj.mode == 0:
            set_re = re.compile(Globals.DATA_RECORD_BEGIN + '[^&^!]*' + Globals.DATA_RECORD_END, re.DOTALL)
            data_records = set_re.findall(data)
            new_data_records = []
            for data_record in data_records:
                new_data_records.append(DataRecord(raw=data_record))

            return data_records
        return data

    return inner_func


class Receiver:
    __module__ = __name__

    def __init__(self, device, mode=0):
        self.device = device
        self.mode = mode

    def ask(self, question):
        self.device.write(question)
        return self.read()

    def read(self):
        data = ''
        new_data = None
        while new_data != '':
            new_data = self.device.read()
            data += new_data

        print repr(data)
        return data


if __name__ == '__main__':
    import unittest, serial

    class ReceiverTestCases(unittest.TestCase):
        __module__ = __name__

        def setUp(self):
            pass

        def tearDown(self):
            pass


    unittest.main()