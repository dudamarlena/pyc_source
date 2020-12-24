# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.3-i386/egg/PyWITS/Objects/Transmission.py
# Compiled at: 2008-04-30 20:55:33
from PyWITS.Objects.WITS0.PhysicalRecord import PhysicalRecord

class Transmission:
    __module__ = __name__

    def __init__(self):
        self.physical_record = PhysicalRecord()


if __name__ == '__main__':
    import unittest

    class TransmissionTests(unittest.TestCase):
        __module__ = __name__

        def setUp(self):
            self.test_transmission = Transmission()

        def testSetup(self):
            pass


    unittest.main()