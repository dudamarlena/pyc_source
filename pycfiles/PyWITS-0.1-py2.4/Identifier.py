# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.3-i386/egg/PyWITS/Objects/Identifier.py
# Compiled at: 2008-05-02 01:44:16


class Identifier:
    __module__ = __name__

    def __init__(self, record_identifier=None, item_identifier=None, raw=None):
        """Initializes a Physical Record
        """
        self.record_identifier = record_identifier
        self.item_identifier = item_identifier
        if raw is not None:
            self.construct(raw)
        return

    def serialize(self):
        """Returns a serial representation of the object"""
        return str(self.record_identifier) + str(self.item_identifier)

    def construct(self, raw):
        print '??', raw

    def __eq__(self, other):
        if not isinstance(other, Identifier):
            return NotImplemented
        return self.record_identifier == other.record_identifier & self.item_identifier == other.item_identifier


if __name__ == '__main__':
    import unittest

    class IdentifierTests(unittest.TestCase):
        __module__ = __name__

        def setUp(self):
            self.test_identifier = Identifier()

        def tearDown(self):
            pass

        def testEQ(self):
            self.failIfEqual(self.test_identifier, None)
            self.failUnlessEqual(self.test_identifier, self.test_identifier)
            return


    unittest.main()