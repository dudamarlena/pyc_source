# uncompyle6 version 3.6.7
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/pyogp/lib/base/message/tests/test_udp_serializer.py
# Compiled at: 2010-02-07 17:28:31
__doc__ = '\nContributors can be viewed at:\nhttp://svn.secondlife.com/svn/linden/projects/2008/pyogp/lib/base/trunk/CONTRIBUTORS.txt \n\n$LicenseInfo:firstyear=2008&license=apachev2$\n\nCopyright 2009, Linden Research, Inc.\n\nLicensed under the Apache License, Version 2.0.\nYou may obtain a copy of the License at:\n    http://www.apache.org/licenses/LICENSE-2.0\nor in \n    http://svn.secondlife.com/svn/linden/projects/2008/pyogp/lib/base/LICENSE.txt\n\n$/LicenseInfo$\n'
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