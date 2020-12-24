# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/pyogp/lib/base/message/tests/test_llsd_builder.py
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