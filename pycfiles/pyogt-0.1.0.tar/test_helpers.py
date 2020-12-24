# uncompyle6 version 3.6.7
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/pyogp/lib/base/tests/test_helpers.py
# Compiled at: 2010-02-07 17:28:31
__doc__ = '\nContributors can be viewed at:\nhttp://svn.secondlife.com/svn/linden/projects/2008/pyogp/lib/base/trunk/CONTRIBUTORS.txt \n\n$LicenseInfo:firstyear=2008&license=apachev2$\n\nCopyright 2009, Linden Research, Inc.\n\nLicensed under the Apache License, Version 2.0.\nYou may obtain a copy of the License at:\n    http://www.apache.org/licenses/LICENSE-2.0\nor in \n    http://svn.secondlife.com/svn/linden/projects/2008/pyogp/lib/base/LICENSE.txt\n\n$/LicenseInfo$\n'
import unittest
from pyogp.lib.base.helpers import Helpers, ListLLSDSerializer, DictLLSDSerializer, LLSDDeserializer
from pyogp.lib.base.exc import DataParsingError
import pyogp.lib.base.tests.config

class TestHelpers(unittest.TestCase):
    __module__ = __name__

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_ListLLSDSerializer(self):
        input_data = [
         'ChatSessionRequest', 1]
        serializer = ListLLSDSerializer(input_data)
        self.assertEquals(input_data, serializer.context)
        self.assertEquals('<?xml version="1.0" ?><llsd><array><string>ChatSessionRequest</string><integer>1</integer></array></llsd>', serializer.serialize())

    def test_DictLLSDSerializer(self):
        input_data = {'foo': 'bar', 'test': 1234}
        serializer = ListLLSDSerializer(input_data)
        self.assertEquals(input_data, serializer.context)
        self.assertEquals('<?xml version="1.0" ?><llsd><map><key>test</key><integer>1234</integer><key>foo</key><string>bar</string></map></llsd>', serializer.serialize())

    def test_LLSDDeserializer_deserialize(self):
        string = '<?xml version="1.0" ?><llsd><map><key>test</key><integer>1234</integer><key>foo</key><string>bar</string></map></llsd>'
        deserializer = LLSDDeserializer()
        self.assertEquals({'test': 1234, 'foo': 'bar'}, deserializer.deserialize(string))

    def test_LLSDDeserializer_deserialize_string(self):
        string = '<?xml version="1.0" ?><llsd><map><key>test</key><integer>1234</integer><key>foo</key><string>bar</string></map></llsd>'
        deserializer = LLSDDeserializer()
        self.assertEquals({'test': 1234, 'foo': 'bar'}, deserializer.deserialize(string))

    def test_LLSDDeserializer_deserialize_nonsense(self):
        data = [
         '<?xml version="1.0" ?><llsd><map><key>test</key><integer>1234</integer><key>foo</key><string>bar</string></map></llsd>']
        deserializer = LLSDDeserializer()
        self.assertEquals(None, deserializer.deserialize(data))
        return


def test_suite():
    from unittest import TestSuite, makeSuite
    suite = TestSuite()
    suite.addTest(makeSuite(TestHelpers))
    return suite