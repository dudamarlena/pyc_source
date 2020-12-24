# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.3-i386/egg/PyWITS/Objects/DataItem.py
# Compiled at: 2008-05-02 02:00:59
from PyWITS import Globals

class DataItem:
    __module__ = __name__

    def __init__(self, identifier=None, value=None, raw=None):
        """Initializes a Physical Record
        """
        self.identifier = identifier
        self.value = value
        if raw is not None:
            self.construct(raw)
        return

    def serialize(self):
        """Returns a serial representation of the object"""
        ser_str = self.identifier.serialize()
        ser_str += str(self.value)
        ser_str += Globals.DATA_ITEM_SEPERATOR
        return ser_str

    def construct(self, raw):
        import string
        from PyWITS.Objects.Identifier import Identifier
        raw = string.strip(raw)
        self.identifier = Identifier(raw=raw[0:3])
        self.value = float(raw[4:])

    def __eq__(self, other):
        if not isinstance(other, DataItem):
            return NotImplemented
        return self.identifier == other.identifier & self.value == other.value


if __name__ == '__main__':
    import unittest

    class DataItemTests(unittest.TestCase):
        __module__ = __name__

        def setUp(self):
            self.test_data_item = DataItem()

        def tearDown(self):
            pass

        def testEQ(self):
            self.failIfEqual(self.test_data_item, None)
            self.failUnlessEqual(self.test_data_item, self.test_data_item)
            return


    unittest.main()