# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/pyogp/lib/base/message/tests/test_message_dot_xml.py
# Compiled at: 2010-02-07 17:28:31
"""
Contributors can be viewed at:
http://svn.secondlife.com/svn/linden/projects/2008/pyogp/lib/base/trunk/CONTRIBUTORS.txt 

$LicenseInfo:firstyear=2008&license=apachev2$

Copyright 2009, Linden Research, Inc.

Licensed under the Apache License, Version 2.0.
You may obtain a copy of the License at:
    http://www.apache.org/licenses/LICENSE-2.0
or in 
    http://svn.secondlife.com/svn/linden/projects/2008/pyogp/lib/base/LICENSE.txt

$/LicenseInfo$
"""
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