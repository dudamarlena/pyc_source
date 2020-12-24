# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.3-ppc/egg/nva/stormcontainer/tests/test_unittests.py
# Compiled at: 2008-01-27 03:34:49
import unittest
from nva.stormcontainer.utils import *
from base64 import urlsafe_b64encode
from base64 import urlsafe_b64decode

class TestUtils(unittest.TestCase):
    __module__ = __name__
    ids = (1, 'klaus')
    string = 'int:1;str:klaus;'
    encode_string = urlsafe_b64encode(string)
    oneids = (5, )
    onestring = 'int:5;'
    oneencode_string = urlsafe_b64encode(onestring)

    def test_encodePKString(self):
        self.assertEqual(encodePKString(self.ids), self.encode_string)

    def test_decodePKString(self):
        self.assertEqual(decodePKString(self.encode_string), self.ids)

    def test_oneencodePKString(self):
        self.assertEqual(encodePKString(self.oneids), self.oneencode_string)

    def test_onedecodePKString(self):
        self.assertEqual(decodePKString(self.oneencode_string), self.oneids)


def test_suite():
    return unittest.TestSuite(unittest.makeSuite(TestUtils))


if __name__ == '__main__':
    unittest.main()