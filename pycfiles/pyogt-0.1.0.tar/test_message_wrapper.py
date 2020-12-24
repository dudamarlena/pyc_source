# uncompyle6 version 3.6.7
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/pyogp/lib/base/message/tests/test_message_wrapper.py
# Compiled at: 2010-02-07 17:28:31
__doc__ = '\nContributors can be viewed at:\nhttp://svn.secondlife.com/svn/linden/projects/2008/pyogp/lib/base/trunk/CONTRIBUTORS.txt \n\n$LicenseInfo:firstyear=2008&license=apachev2$\n\nCopyright 2009, Linden Research, Inc.\n\nLicensed under the Apache License, Version 2.0.\nYou may obtain a copy of the License at:\n    http://www.apache.org/licenses/LICENSE-2.0\nor in \n    http://svn.secondlife.com/svn/linden/projects/2008/pyogp/lib/base/LICENSE.txt\n\n$/LicenseInfo$\n'
import unittest, doctest
from uuid import UUID
from pyogp.lib.base.message.data import msg_tmpl
from pyogp.lib.base.message.msgtypes import MsgType
from pyogp.lib.base.message.message import Message, Block
from pyogp.lib.base.message.udpdeserializer import UDPMessageDeserializer

class TestMessage(unittest.TestCase):
    __module__ = __name__

    def tearDown(self):
        pass

    def setUp(self):
        pass

    def test_block(self):
        block = Block('CircuitCode', ID=1234, Code=531)

    def test_build(self):
        msg = Message('TestPacket', Block('CircuitCode', ID=1234, Code=531))
        assert msg.blocks['CircuitCode'][0].vars['ID'].data == 1234, 'Incorrect data in block ID'
        assert msg.blocks['CircuitCode'][0].vars['Code'].data == 531, 'Incorrect data in block Code'

    def test_build_multiple(self):
        msg = Message('TestPacket', Block('CircuitCode', ID=1234, Code=789), Block('CircuitCode', ID=5678, Code=456), Block('Test', ID=9101, Code=123))
        assert msg.blocks['CircuitCode'][0].vars['ID'].data == 1234, 'Incorrect data in block ID'
        assert msg.blocks['CircuitCode'][1].vars['ID'].data == 5678, 'Incorrect data in block 2 ID'
        assert msg.blocks['CircuitCode'][0].vars['Code'].data == 789, 'Incorrect data in block Code'
        assert msg.blocks['CircuitCode'][1].vars['Code'].data == 456, 'Incorrect data in block 2 Code'
        assert msg.blocks['Test'][0].vars['ID'].data == 9101, 'Incorrect data in block Test ID'
        assert msg.blocks['Test'][0].vars['Code'].data == 123, 'Incorrect data in block Test ID'

    def test_getitem_helpers(self):
        msg = Message('TestPacket', Block('CircuitCode', ID=1234, Code=789), Block('CircuitCode', ID=5678, Code=456), Block('Test', ID=9101, Code=123))
        assert msg.blocks['CircuitCode'][0].vars['ID'].data == msg['CircuitCode'][0]['ID'], "Explicit blocks/vars/data doesn't match __getitem__ shortcut"
        assert msg.blocks['CircuitCode'][1].vars['ID'].data == msg['CircuitCode'][1]['ID'], "Explicit blocks/vars/data doesn't match __getitem__ shortcut"
        assert msg.blocks['CircuitCode'][0].vars['Code'].data == msg['CircuitCode'][0]['Code'], "Explicit blocks/vars/data doesn't match __getitem__ shortcut"
        assert msg.blocks['CircuitCode'][1].vars['Code'].data == msg['CircuitCode'][1]['Code'], "Explicit blocks/vars/data doesn't match __getitem__ shortcut"
        assert msg.blocks['Test'][0].vars['ID'].data == msg['Test'][0]['ID'], "Explicit blocks/vars/data doesn't match __getitem__ shortcut"
        assert msg.blocks['Test'][0].vars['Code'].data == msg['Test'][0]['Code'], "Explicit blocks/vars/data doesn't match __getitem__ shortcut"

    def test_build_chat(self):
        import uuid
        msg = Message('ChatFromViewer', Block('AgentData', AgentID=uuid.UUID('550e8400-e29b-41d4-a716-446655440000'), SessionID=uuid.UUID('550e8400-e29b-41d4-a716-446655440000')), Block('ChatData', Message='Chatting\n', Type=1, Channel=0))
        assert msg.blocks['ChatData'][0].vars['Type'].data == 1, 'Bad type sent'
        assert msg.blocks['ChatData'][0].vars['Channel'].data == 0, 'Bad Channel sent'
        from pyogp.lib.base.message.udpserializer import UDPMessageSerializer
        serial = UDPMessageSerializer()
        msg = serial.serialize(msg)


def test_suite():
    from unittest import TestSuite, makeSuite
    suite = TestSuite()
    suite.addTest(makeSuite(TestMessage))
    return suite