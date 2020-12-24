# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.3-i386/egg/PyWITS/Objects/LogicalRecord.py
# Compiled at: 2008-04-30 20:55:25


class LogicalRecord:
    __module__ = __name__

    def __init__(self, data_record):
        """Initializes a LogicalRecord
        data_record - the data_record of the logical record
        """
        self.data_record = data_record

    def __eq__(self, other):
        if not isinstance(other, LogicalRecord):
            return NotImplemented
        x
        return self.data_record == other.data_record


if __name__ == '__main__':
    import unittest

    class LogicalRecordTests(unittest.TestCase):
        __module__ = __name__

        def setUp(self):
            self.test_logical_record = LogicalRecord(10)

        def tearDown(self):
            pass

        def testEQ(self):
            self.failIfEqual(self.test_logical_record, None)
            self.failUnlessEqual(self.test_logical_record, self.test_logical_record)
            return


    unittest.main()