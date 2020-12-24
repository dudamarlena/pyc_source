# uncompyle6 version 3.6.7
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/pyogp/lib/base/message/tests/test_message_dot_xml.py
# Compiled at: 2010-02-07 17:28:31
__doc__ = '\nContributors can be viewed at:\nhttp://svn.secondlife.com/svn/linden/projects/2008/pyogp/lib/base/trunk/CONTRIBUTORS.txt \n\n$LicenseInfo:firstyear=2008&license=apachev2$\n\nCopyright 2009, Linden Research, Inc.\n\nLicensed under the Apache License, Version 2.0.\nYou may obtain a copy of the License at:\n    http://www.apache.org/licenses/LICENSE-2.0\nor in \n    http://svn.secondlife.com/svn/linden/projects/2008/pyogp/lib/base/LICENSE.txt\n\n$/LicenseInfo$\n'
import unittest, doctest
from uuid import UUID
from pyogp.lib.base.message.message_dot_xml import MessageDotXML

class TestMessageDotXML(unittest.TestCase):
    __module__ = __name__

    def setUp(self):
        self.message_xml = MessageDotXML()

    def tearDown(self):
        pass

    def test_constructor(self):
        self.assert_(self.message_xml.serverDefaults)
        self.assert_(self.message_xml.messages)
        self.assert_(self.message_xml.capBans)
        self.assert_(self.message_xml.maxQueuedEvents)
        self.assert_(self.message_xml.messageBans)

    def test_validate_udp_msg_false(self):
        self.assertEquals(self.message_xml.validate_udp_msg('ParcelProperties'), False)

    def test_validate_udp_msg_true(self):
        self.assertEquals(self.message_xml.validate_udp_msg('OpenCircuit'), True)


def test_suite():
    from unittest import TestSuite, makeSuite
    suite = TestSuite()
    suite.addTest(makeSuite(TestMessageDotXML))
    return suite