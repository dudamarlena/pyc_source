# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.3-i386/egg/PyWITS/Objects/DataRecord.py
# Compiled at: 2008-05-02 01:56:30
from PyWITS import Globals

class DataRecord:
    __module__ = __name__

    def __init__(self, data_items=None, raw=None):
        """Initializes a DataRecord
        """
        if data_items is None:
            self.data_items = []
        else:
            self.data_items = data_items
        if raw is not None:
            self.construct(raw)
        return

    def serialize(self):
        ser_str = Globals.DATA_RECORD_BEGIN
        for data_item in self.data_items:
            ser_str += data_item.serialize()

        ser_str += Globals.DATA_RECORD_END
        return ser_str

    def construct(self, raw):
        import re
        from PyWITS.Objects.DataItem import DataItem
        data_item_re = re.compile('[^!^&^\r^\n]+\r\n')
        raw_data_items = data_item_re.findall(raw)
        data_items = []
        for raw_data_item in raw_data_items:
            data_items.append(DataItem(raw=raw_data_item))

    def __eq__(self, other):
        if not isinstance(other, DataRecord):
            return NotImplemented
        return self.data_items == other.data_items


if __name__ == '__main__':
    import unittest

    class DataRecordTests(unittest.TestCase):
        __module__ = __name__

        def setUp(self):
            self.test_data_record = DataRecord(10)

        def tearDown(self):
            pass

        def testEQ(self):
            self.failIfEqual(self.test_data_record, None)
            self.failUnlessEqual(self.test_data_record, self.test_data_record)
            return


    unittest.main()