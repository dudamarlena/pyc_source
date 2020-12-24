# uncompyle6 version 3.6.7
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/pyogp/lib/base/message/tests/test_llsd_builder.py
# Compiled at: 2010-02-07 17:28:31
__doc__ = '\nContributors can be viewed at:\nhttp://svn.secondlife.com/svn/linden/projects/2008/pyogp/lib/base/trunk/CONTRIBUTORS.txt \n\n$LicenseInfo:firstyear=2008&license=apachev2$\n\nCopyright 2009, Linden Research, Inc.\n\nLicensed under the Apache License, Version 2.0.\nYou may obtain a copy of the License at:\n    http://www.apache.org/licenses/LICENSE-2.0\nor in \n    http://svn.secondlife.com/svn/linden/projects/2008/pyogp/lib/base/LICENSE.txt\n\n$/LicenseInfo$\n'
import unittest, doctest
from llbase import llsd
from pyogp.lib.base.message.llsd_builder import LLSDMessageBuilder
from pyogp.lib.base.message.msgtypes import MsgType

class TestLLSDBuilder(unittest.TestCase):
    __module__ = __name__

    def tearDown(self):
        pass

    def setUp(self):
        pass

    def test_builder(self):
        builder = LLSDMessageBuilder()
        builder.new_message('TestMessage')
        builder.next_block('TestBlock1')
        builder.add_data('Test1', 1, MsgType.MVT_U32)
        builder.next_block('TestBlock1')
        builder.add_data('Test2', 1, MsgType.MVT_U32)
        builder.next_block('NeighborBlock')
        builder.add_data('Test0', 1, MsgType.MVT_U32)
        builder.add_data('Test1', 1, MsgType.MVT_U32)
        builder.add_data('Test2', 1, MsgType.MVT_U32)
        builder.next_block('NeighborBlock')
        builder.add_data('Test1', 1, MsgType.MVT_U32)
        builder.add_data('Test1', 1, MsgType.MVT_U32)
        builder.add_data('Test1', 1, MsgType.MVT_U32)
        builder.next_block('NeighborBlock')
        builder.add_data('Test2', 1, MsgType.MVT_U32)
        builder.add_data('Test2', 1, MsgType.MVT_U32)
        builder.add_data('Test2', 1, MsgType.MVT_U32)
        builder.next_block('TestBlock2')
        builder.add_data('Test1', 1, MsgType.MVT_U32)
        (msg, size) = builder.build_message()
        try:
            assert len(msg['NeighborBlock']) == 3, 'Multiple blocks not' + ' correct'
        except:
            assert False, 'Message not set up properly'

        try:
            msg = llsd.format_xml(msg)
        except:
            assert False, 'Message not built correctly so it can be formatted'


def test_suite():
    from unittest import TestSuite, makeSuite
    suite = TestSuite()
    suite.addTest(makeSuite(TestLLSDBuilder))
    return suite