# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.3-i386/egg/PyWITS/Objects/PhysicalRecord.py
# Compiled at: 2008-04-30 20:55:28


class PhysicalRecord:
    __module__ = __name__

    def __init__(self, logical_records):
        """Initializes a Physical Record
        logical_records - A collection of logical_records"""
        self.logical_records = logical_records

    def __eq__(self, other):
        if not isinstance(other, PhysicalRecord):
            return NotImplemented
        return self.logical_records == other.logical_records


if __name__ == '__main__':
    import unittest

    class PhysicalRecordTests(unittest.TestCase):
        __module__ = __name__

        def setUp(self):
            self.test_physical_record = PhysicalRecord(10)

        def tearDown(self):
            pass

        def testEQ(self):
            self.failIfEqual(self.test_physical_record, None)
            self.failUnlessEqual(self.test_physical_record, self.test_physical_record)
            return


    unittest.main()