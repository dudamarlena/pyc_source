# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/ant/core/tests/message_tests.py
# Compiled at: 2011-10-07 13:55:30
import unittest
from ant.core.message import *

class MessageTest(unittest.TestCase):

    def setUp(self):
        self.message = Message()

    def test_get_setPayload(self):
        self.assertRaises(MessageError, self.message.setPayload, b'\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff')
        self.message.setPayload('\x11\x11\x11\x11\x11')
        self.assertEquals(self.message.getPayload(), '\x11\x11\x11\x11\x11')

    def test_get_setType(self):
        self.assertRaises(MessageError, self.message.setType, -1)
        self.assertRaises(MessageError, self.message.setType, 300)
        self.message.setType(35)
        self.assertEquals(self.message.getType(), 35)

    def test_getChecksum(self):
        self.message = Message(type_=MESSAGE_SYSTEM_RESET, payload='\x00')
        self.assertEquals(self.message.getChecksum(), 239)
        self.message = Message(type_=MESSAGE_CHANNEL_ASSIGN, payload='\x00\x00\x00')
        self.assertEquals(self.message.getChecksum(), 229)

    def test_getSize(self):
        self.message.setPayload('\x11\x11\x11\x11\x11\x11\x11')
        self.assertEquals(self.message.getSize(), 11)

    def test_encode(self):
        self.message = Message(type_=MESSAGE_CHANNEL_ASSIGN, payload='\x00\x00\x00')
        self.assertEqual(self.message.encode(), b'\xa4\x03B\x00\x00\x00\xe5')

    def test_decode(self):
        self.assertRaises(MessageError, self.message.decode, b'\xa5\x03B\x00\x00\x00\xe5')
        self.assertRaises(MessageError, self.message.decode, b'\xa4\x14B' + '\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00' + b'\xe5')
        self.assertRaises(MessageError, self.message.decode, b'\xa4\x03B\x01\x02\xf3\xe5')
        self.assertEqual(self.message.decode(b'\xa4\x03B\x00\x00\x00\xe5'), 7)
        self.assertEqual(self.message.getType(), MESSAGE_CHANNEL_ASSIGN)
        self.assertEqual(self.message.getPayload(), '\x00\x00\x00')
        self.assertEqual(self.message.getChecksum(), 229)

    def test_getHandler(self):
        handler = self.message.getHandler(b'\xa4\x03B\x00\x00\x00\xe5')
        self.assertTrue(isinstance(handler, ChannelAssignMessage))
        self.assertRaises(MessageError, self.message.getHandler, b'\xa4\x03\xff\x00\x00\x00\xe5')
        self.assertRaises(MessageError, self.message.getHandler, b'\xa4\x03B')
        self.assertRaises(MessageError, self.message.getHandler, b'\xa4\x05B\x00\x00\x00\x00')


class ChannelMessageTest(unittest.TestCase):

    def setUp(self):
        self.message = ChannelMessage(type_=MESSAGE_SYSTEM_RESET)

    def test_get_setChannelNumber(self):
        self.assertEquals(self.message.getChannelNumber(), 0)
        self.message.setChannelNumber(3)
        self.assertEquals(self.message.getChannelNumber(), 3)


class ChannelUnassignMessageTest(unittest.TestCase):
    pass


class ChannelAssignMessageTest(unittest.TestCase):

    def setUp(self):
        self.message = ChannelAssignMessage()

    def test_get_setChannelType(self):
        self.message.setChannelType(16)
        self.assertEquals(self.message.getChannelType(), 16)

    def test_get_setNetworkNumber(self):
        self.message.setNetworkNumber(17)
        self.assertEquals(self.message.getNetworkNumber(), 17)

    def test_payload(self):
        self.message.setChannelNumber(1)
        self.message.setChannelType(2)
        self.message.setNetworkNumber(3)
        self.assertEquals(self.message.getPayload(), '\x01\x02\x03')


class ChannelIDMessageTest(unittest.TestCase):

    def setUp(self):
        self.message = ChannelIDMessage()

    def test_get_setDeviceNumber(self):
        self.message.setDeviceNumber(4346)
        self.assertEquals(self.message.getDeviceNumber(), 4346)

    def test_get_setDeviceType(self):
        self.message.setDeviceType(16)
        self.assertEquals(self.message.getDeviceType(), 16)

    def test_get_setTransmissionType(self):
        self.message.setTransmissionType(17)
        self.assertEquals(self.message.getTransmissionType(), 17)

    def test_payload(self):
        self.message.setChannelNumber(1)
        self.message.setDeviceNumber(770)
        self.message.setDeviceType(4)
        self.message.setTransmissionType(5)
        self.assertEquals(self.message.getPayload(), '\x01\x02\x03\x04\x05')


class ChannelPeriodMessageTest(unittest.TestCase):

    def setUp(self):
        self.message = ChannelPeriodMessage()

    def test_get_setChannelPeriod(self):
        self.message.setChannelPeriod(4346)
        self.assertEquals(self.message.getChannelPeriod(), 4346)

    def test_payload(self):
        self.message.setChannelNumber(1)
        self.message.setChannelPeriod(770)
        self.assertEquals(self.message.getPayload(), '\x01\x02\x03')


class ChannelSearchTimeoutMessageTest(unittest.TestCase):

    def setUp(self):
        self.message = ChannelSearchTimeoutMessage()

    def test_get_setTimeout(self):
        self.message.setTimeout(16)
        self.assertEquals(self.message.getTimeout(), 16)

    def test_payload(self):
        self.message.setChannelNumber(1)
        self.message.setTimeout(2)
        self.assertEquals(self.message.getPayload(), '\x01\x02')


class ChannelFrequencyMessageTest(unittest.TestCase):

    def setUp(self):
        self.message = ChannelFrequencyMessage()

    def test_get_setFrequency(self):
        self.message.setFrequency(22)
        self.assertEquals(self.message.getFrequency(), 22)

    def test_payload(self):
        self.message.setChannelNumber(1)
        self.message.setFrequency(2)
        self.assertEquals(self.message.getPayload(), '\x01\x02')


class ChannelTXPowerMessageTest(unittest.TestCase):

    def setUp(self):
        self.message = ChannelTXPowerMessage()

    def test_get_setPower(self):
        self.message.setPower(250)
        self.assertEquals(self.message.getPower(), 250)

    def test_payload(self):
        self.message.setChannelNumber(1)
        self.message.setPower(2)
        self.assertEquals(self.message.getPayload(), '\x01\x02')


class NetworkKeyMessageTest(unittest.TestCase):

    def setUp(self):
        self.message = NetworkKeyMessage()

    def test_get_setNumber(self):
        self.message.setNumber(250)
        self.assertEquals(self.message.getNumber(), 250)

    def test_get_setKey(self):
        self.message.setKey(b'\xfd\xfd\xfd\xfd\xfd\xfd\xfd\xfd')
        self.assertEquals(self.message.getKey(), b'\xfd\xfd\xfd\xfd\xfd\xfd\xfd\xfd')

    def test_payload(self):
        self.message.setNumber(1)
        self.message.setKey('\x02\x03\x04\x05\x06\x07\x08\t')
        self.assertEquals(self.message.getPayload(), '\x01\x02\x03\x04\x05\x06\x07\x08\t')


class TXPowerMessageTest(unittest.TestCase):

    def setUp(self):
        self.message = TXPowerMessage()

    def test_get_setPower(self):
        self.message.setPower(250)
        self.assertEquals(self.message.getPower(), 250)

    def test_payload(self):
        self.message.setPower(1)
        self.assertEquals(self.message.getPayload(), '\x00\x01')


class SystemResetMessageTest(unittest.TestCase):
    pass


class ChannelOpenMessageTest(unittest.TestCase):
    pass


class ChannelCloseMessageTest(unittest.TestCase):
    pass


class ChannelRequestMessageTest(unittest.TestCase):

    def setUp(self):
        self.message = ChannelRequestMessage()

    def test_get_setMessageID(self):
        self.message.setMessageID(250)
        self.assertEquals(self.message.getMessageID(), 250)
        self.assertRaises(MessageError, self.message.setMessageID, 65535)

    def test_payload(self):
        self.message.setChannelNumber(1)
        self.message.setMessageID(2)
        self.assertEquals(self.message.getPayload(), '\x01\x02')


class ChannelBroadcastDataMessageTest(unittest.TestCase):
    pass


class ChannelAcknowledgedDataMessageTest(unittest.TestCase):
    pass


class ChannelBurstDataMessageTest(unittest.TestCase):
    pass


class ChannelEventMessageTest(unittest.TestCase):

    def setUp(self):
        self.message = ChannelEventMessage()

    def test_get_setMessageID(self):
        self.message.setMessageID(250)
        self.assertEquals(self.message.getMessageID(), 250)
        self.assertRaises(MessageError, self.message.setMessageID, 65535)

    def test_get_setMessageCode(self):
        self.message.setMessageCode(250)
        self.assertEquals(self.message.getMessageCode(), 250)
        self.assertRaises(MessageError, self.message.setMessageCode, 65535)

    def test_payload(self):
        self.message.setChannelNumber(1)
        self.message.setMessageID(2)
        self.message.setMessageCode(3)
        self.assertEquals(self.message.getPayload(), '\x01\x02\x03')


class ChannelStatusMessageTest(unittest.TestCase):

    def setUp(self):
        self.message = ChannelStatusMessage()

    def test_get_setStatus(self):
        self.message.setStatus(250)
        self.assertEquals(self.message.getStatus(), 250)
        self.assertRaises(MessageError, self.message.setStatus, 65535)

    def test_payload(self):
        self.message.setChannelNumber(1)
        self.message.setStatus(2)
        self.assertEquals(self.message.getPayload(), '\x01\x02')


class VersionMessageTest(unittest.TestCase):

    def setUp(self):
        self.message = VersionMessage()

    def test_get_setVersion(self):
        self.message.setVersion(b'\xab\xab\xab\xab\xab\xab\xab\xab\xab')
        self.assertEquals(self.message.getVersion(), b'\xab\xab\xab\xab\xab\xab\xab\xab\xab')
        self.assertRaises(MessageError, self.message.setVersion, '1234')

    def test_payload(self):
        self.message.setVersion('\x01\x01\x01\x01\x01\x01\x01\x01\x01')
        self.assertEquals(self.message.getPayload(), '\x01\x01\x01\x01\x01\x01\x01\x01\x01')


class CapabilitiesMessageTest(unittest.TestCase):

    def setUp(self):
        self.message = CapabilitiesMessage()

    def test_get_setMaxChannels(self):
        self.message.setMaxChannels(250)
        self.assertEquals(self.message.getMaxChannels(), 250)
        self.assertRaises(MessageError, self.message.setMaxChannels, 65535)

    def test_get_setMaxNetworks(self):
        self.message.setMaxNetworks(250)
        self.assertEquals(self.message.getMaxNetworks(), 250)
        self.assertRaises(MessageError, self.message.setMaxNetworks, 65535)

    def test_get_setStdOptions(self):
        self.message.setStdOptions(250)
        self.assertEquals(self.message.getStdOptions(), 250)
        self.assertRaises(MessageError, self.message.setStdOptions, 65535)

    def test_get_setAdvOptions(self):
        self.message.setAdvOptions(250)
        self.assertEquals(self.message.getAdvOptions(), 250)
        self.assertRaises(MessageError, self.message.setAdvOptions, 65535)

    def test_get_setAdvOptions2(self):
        self.message.setAdvOptions2(250)
        self.assertEquals(self.message.getAdvOptions2(), 250)
        self.assertRaises(MessageError, self.message.setAdvOptions2, 65535)
        self.message = CapabilitiesMessage(adv_opts2=None)
        self.assertEquals(len(self.message.payload), 4)
        return

    def test_payload(self):
        self.message.setMaxChannels(1)
        self.message.setMaxNetworks(2)
        self.message.setStdOptions(3)
        self.message.setAdvOptions(4)
        self.message.setAdvOptions2(5)
        self.assertEquals(self.message.getPayload(), '\x01\x02\x03\x04\x05')


class SerialNumberMessageTest(unittest.TestCase):

    def setUp(self):
        self.message = SerialNumberMessage()

    def test_get_setSerialNumber(self):
        self.message.setSerialNumber(b'\xfa\xfb\xfc\xfd')
        self.assertEquals(self.message.getSerialNumber(), b'\xfa\xfb\xfc\xfd')
        self.assertRaises(MessageError, self.message.setSerialNumber, b'\xff\xff\xff\xff\xff\xff\xff\xff')

    def test_payload(self):
        self.message.setSerialNumber('\x01\x02\x03\x04')
        self.assertEquals(self.message.getPayload(), '\x01\x02\x03\x04')