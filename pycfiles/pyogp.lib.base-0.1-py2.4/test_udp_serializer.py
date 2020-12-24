# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/pyogp/lib/base/message/tests/test_udp_serializer.py
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
from pyogp.lib.base.settings import Settings
from pyogp.lib.base.message.msgtypes import MsgType
from pyogp.lib.base.message.udpdeserializer import UDPMessageDeserializer
from pyogp.lib.base.message.udpserializer import UDPMessageSerializer

class TestSerializer(unittest.TestCase):
    __module__ = __name__

    def tearDown(self):
        pass

    def setUp(self):
        self.settings = Settings()
        self.settings.ENABLE_DEFERRED_PACKET_PARSING = False

    def test_serialize(self):
        message = b'\xff\xff\xff\xfb' + '\x03' + '\x01\x00\x00\x00' + '\x02\x00\x00\x00' + '\x03\x00\x00\x00'
        message = '\x00' + '\x00\x00\x00\x01' + '\x00' + message
        deserializer = UDPMessageDeserializer(settings=self.settings)
        packet = deserializer.deserialize(message)
        serializer = UDPMessageSerializer()
        packed_data = serializer.serialize(packet)
        assert packed_data == message, 'Incorrect serialization'


def test_suite():
    from unittest import TestSuite, makeSuite
    suite = TestSuite()
    suite.addTest(makeSuite(TestSerializer))
    return suite