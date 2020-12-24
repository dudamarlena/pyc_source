# uncompyle6 version 3.6.7
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/ant/core/message.py
# Compiled at: 2011-10-07 13:51:02
import struct
from ant.core.exceptions import MessageError
from ant.core.constants import *

class Message(object):

    def __init__(self, type_=0, payload=''):
        self.setType(type_)
        self.setPayload(payload)

    def getPayload(self):
        return ('').join(self.payload)

    def setPayload(self, payload):
        if len(payload) > 9:
            raise MessageError('Could not set payload (payload too long).')
        self.payload = []
        for byte in payload:
            self.payload += byte

    def getType(self):
        return self.type_

    def setType(self, type_):
        if type_ > 255 or type_ < 0:
            raise MessageError('Could not set type (type out of range).')
        self.type_ = type_

    def getChecksum(self):
        data = chr(len(self.getPayload()))
        data += chr(self.getType())
        data += self.getPayload()
        checksum = MESSAGE_TX_SYNC
        for byte in data:
            checksum = (checksum ^ ord(byte)) % 255

        return checksum

    def getSize(self):
        return len(self.getPayload()) + 4

    def encode(self):
        raw = struct.pack('BBB', MESSAGE_TX_SYNC, len(self.getPayload()), self.getType())
        raw += self.getPayload()
        raw += chr(self.getChecksum())
        return raw

    def decode(self, raw):
        if len(raw) < 5:
            raise MessageError('Could not decode (message is incomplete).')
        (sync, length, type_) = struct.unpack('BBB', raw[:3])
        if sync != MESSAGE_TX_SYNC:
            raise MessageError('Could not decode (expected TX sync).')
        if length > 9:
            raise MessageError('Could not decode (payload too long).')
        if len(raw) < length + 4:
            raise MessageError('Could not decode (message is incomplete).')
        self.setType(type_)
        self.setPayload(raw[3:length + 3])
        if self.getChecksum() != ord(raw[(length + 3)]):
            raise MessageError('Could not decode (bad checksum).', internal='CHECKSUM')
        return self.getSize()

    def getHandler(self, raw=None):
        if raw:
            self.decode(raw)
        msg = None
        if self.type_ == MESSAGE_CHANNEL_UNASSIGN:
            msg = ChannelUnassignMessage()
        elif self.type_ == MESSAGE_CHANNEL_ASSIGN:
            msg = ChannelAssignMessage()
        elif self.type_ == MESSAGE_CHANNEL_ID:
            msg = ChannelIDMessage()
        elif self.type_ == MESSAGE_CHANNEL_PERIOD:
            msg = ChannelPeriodMessage()
        elif self.type_ == MESSAGE_CHANNEL_SEARCH_TIMEOUT:
            msg = ChannelSearchTimeoutMessage()
        elif self.type_ == MESSAGE_CHANNEL_FREQUENCY:
            msg = ChannelFrequencyMessage()
        elif self.type_ == MESSAGE_CHANNEL_TX_POWER:
            msg = ChannelTXPowerMessage()
        elif self.type_ == MESSAGE_NETWORK_KEY:
            msg = NetworkKeyMessage()
        elif self.type_ == MESSAGE_TX_POWER:
            msg = TXPowerMessage()
        elif self.type_ == MESSAGE_SYSTEM_RESET:
            msg = SystemResetMessage()
        elif self.type_ == MESSAGE_CHANNEL_OPEN:
            msg = ChannelOpenMessage()
        elif self.type_ == MESSAGE_CHANNEL_CLOSE:
            msg = ChannelCloseMessage()
        elif self.type_ == MESSAGE_CHANNEL_REQUEST:
            msg = ChannelRequestMessage()
        elif self.type_ == MESSAGE_CHANNEL_BROADCAST_DATA:
            msg = ChannelBroadcastDataMessage()
        elif self.type_ == MESSAGE_CHANNEL_ACKNOWLEDGED_DATA:
            msg = ChannelAcknowledgedDataMessage()
        elif self.type_ == MESSAGE_CHANNEL_BURST_DATA:
            msg = ChannelBurstDataMessage()
        elif self.type_ == MESSAGE_CHANNEL_EVENT:
            msg = ChannelEventMessage()
        elif self.type_ == MESSAGE_CHANNEL_STATUS:
            msg = ChannelStatusMessage()
        elif self.type_ == MESSAGE_VERSION:
            msg = VersionMessage()
        elif self.type_ == MESSAGE_CAPABILITIES:
            msg = CapabilitiesMessage()
        elif self.type_ == MESSAGE_SERIAL_NUMBER:
            msg = SerialNumberMessage()
        else:
            raise MessageError('Could not find message handler (unknown message type).')
        msg.setPayload(self.getPayload())
        return msg


class ChannelMessage(Message):

    def __init__(self, type_, payload='', number=0):
        Message.__init__(self, type_, '\x00' + payload)
        self.setChannelNumber(number)

    def getChannelNumber(self):
        return ord(self.payload[0])

    def setChannelNumber(self, number):
        if number > 255 or number < 0:
            raise MessageError('Could not set channel number (out of range).')
        self.payload[0] = chr(number)


class ChannelUnassignMessage(ChannelMessage):

    def __init__(self, number=0):
        ChannelMessage.__init__(self, type_=MESSAGE_CHANNEL_UNASSIGN, number=number)


class ChannelAssignMessage(ChannelMessage):

    def __init__(self, number=0, type_=0, network=0):
        payload = struct.pack('BB', type_, network)
        ChannelMessage.__init__(self, type_=MESSAGE_CHANNEL_ASSIGN, payload=payload, number=number)

    def getChannelType(self):
        return ord(self.payload[1])

    def setChannelType(self, type_):
        self.payload[1] = chr(type_)

    def getNetworkNumber(self):
        return ord(self.payload[2])

    def setNetworkNumber(self, number):
        self.payload[2] = chr(number)


class ChannelIDMessage(ChannelMessage):

    def __init__(self, number=0, device_number=0, device_type=0, trans_type=0):
        ChannelMessage.__init__(self, type_=MESSAGE_CHANNEL_ID, payload='\x00\x00\x00\x00', number=number)
        self.setDeviceNumber(device_number)
        self.setDeviceType(device_type)
        self.setTransmissionType(trans_type)

    def getDeviceNumber(self):
        return struct.unpack('<H', self.getPayload()[1:3])[0]

    def setDeviceNumber(self, device_number):
        self.payload[1:3] = struct.pack('<H', device_number)

    def getDeviceType(self):
        return ord(self.payload[3])

    def setDeviceType(self, device_type):
        self.payload[3] = chr(device_type)

    def getTransmissionType(self):
        return ord(self.payload[4])

    def setTransmissionType(self, trans_type):
        self.payload[4] = chr(trans_type)


class ChannelPeriodMessage(ChannelMessage):

    def __init__(self, number=0, period=8192):
        ChannelMessage.__init__(self, type_=MESSAGE_CHANNEL_PERIOD, payload='\x00\x00', number=number)
        self.setChannelPeriod(period)

    def getChannelPeriod(self):
        return struct.unpack('<H', self.getPayload()[1:3])[0]

    def setChannelPeriod(self, period):
        self.payload[1:3] = struct.pack('<H', period)


class ChannelSearchTimeoutMessage(ChannelMessage):

    def __init__(self, number=0, timeout=255):
        ChannelMessage.__init__(self, type_=MESSAGE_CHANNEL_SEARCH_TIMEOUT, payload='\x00', number=number)
        self.setTimeout(timeout)

    def getTimeout(self):
        return ord(self.payload[1])

    def setTimeout(self, timeout):
        self.payload[1] = chr(timeout)


class ChannelFrequencyMessage(ChannelMessage):

    def __init__(self, number=0, frequency=66):
        ChannelMessage.__init__(self, type_=MESSAGE_CHANNEL_FREQUENCY, payload='\x00', number=number)
        self.setFrequency(frequency)

    def getFrequency(self):
        return ord(self.payload[1])

    def setFrequency(self, frequency):
        self.payload[1] = chr(frequency)


class ChannelTXPowerMessage(ChannelMessage):

    def __init__(self, number=0, power=0):
        ChannelMessage.__init__(self, type_=MESSAGE_CHANNEL_TX_POWER, payload='\x00', number=number)

    def getPower(self):
        return ord(self.payload[1])

    def setPower(self, power):
        self.payload[1] = chr(power)


class NetworkKeyMessage(Message):

    def __init__(self, number=0, key='\x00\x00\x00\x00\x00\x00\x00\x00'):
        Message.__init__(self, type_=MESSAGE_NETWORK_KEY, payload='\x00\x00\x00\x00\x00\x00\x00\x00\x00')
        self.setNumber(number)
        self.setKey(key)

    def getNumber(self):
        return ord(self.payload[0])

    def setNumber(self, number):
        self.payload[0] = chr(number)

    def getKey(self):
        return self.getPayload()[1:]

    def setKey(self, key):
        self.payload[1:] = key


class TXPowerMessage(Message):

    def __init__(self, power=0):
        Message.__init__(self, type_=MESSAGE_TX_POWER, payload='\x00\x00')
        self.setPower(power)

    def getPower(self):
        return ord(self.payload[1])

    def setPower(self, power):
        self.payload[1] = chr(power)


class SystemResetMessage(Message):

    def __init__(self):
        Message.__init__(self, type_=MESSAGE_SYSTEM_RESET, payload='\x00')


class ChannelOpenMessage(ChannelMessage):

    def __init__(self, number=0):
        ChannelMessage.__init__(self, type_=MESSAGE_CHANNEL_OPEN, number=number)


class ChannelCloseMessage(ChannelMessage):

    def __init__(self, number=0):
        ChannelMessage.__init__(self, type_=MESSAGE_CHANNEL_CLOSE, number=number)


class ChannelRequestMessage(ChannelMessage):

    def __init__(self, number=0, message_id=MESSAGE_CHANNEL_STATUS):
        ChannelMessage.__init__(self, type_=MESSAGE_CHANNEL_REQUEST, number=number, payload='\x00')
        self.setMessageID(message_id)

    def getMessageID(self):
        return ord(self.payload[1])

    def setMessageID(self, message_id):
        if message_id > 255 or message_id < 0:
            raise MessageError('Could not set message ID (out of range).')
        self.payload[1] = chr(message_id)


class RequestMessage(ChannelRequestMessage):
    pass


class ChannelBroadcastDataMessage(ChannelMessage):

    def __init__(self, number=0, data='\x00\x00\x00\x00\x00\x00\x00'):
        ChannelMessage.__init__(self, type_=MESSAGE_CHANNEL_BROADCAST_DATA, payload=data, number=number)


class ChannelAcknowledgedDataMessage(ChannelMessage):

    def __init__(self, number=0, data='\x00\x00\x00\x00\x00\x00\x00'):
        ChannelMessage.__init__(self, type_=MESSAGE_CHANNEL_ACKNOWLEDGED_DATA, payload=data, number=number)


class ChannelBurstDataMessage(ChannelMessage):

    def __init__(self, number=0, data='\x00\x00\x00\x00\x00\x00\x00'):
        ChannelMessage.__init__(self, type_=MESSAGE_CHANNEL_BURST_DATA, payload=data, number=number)


class ChannelEventMessage(ChannelMessage):

    def __init__(self, number=0, message_id=0, message_code=0):
        ChannelMessage.__init__(self, type_=MESSAGE_CHANNEL_EVENT, number=number, payload='\x00\x00')
        self.setMessageID(message_id)
        self.setMessageCode(message_code)

    def getMessageID(self):
        return ord(self.payload[1])

    def setMessageID(self, message_id):
        if message_id > 255 or message_id < 0:
            raise MessageError('Could not set message ID (out of range).')
        self.payload[1] = chr(message_id)

    def getMessageCode(self):
        return ord(self.payload[2])

    def setMessageCode(self, message_code):
        if message_code > 255 or message_code < 0:
            raise MessageError('Could not set message code (out of range).')
        self.payload[2] = chr(message_code)


class ChannelStatusMessage(ChannelMessage):

    def __init__(self, number=0, status=0):
        ChannelMessage.__init__(self, type_=MESSAGE_CHANNEL_STATUS, payload='\x00', number=number)
        self.setStatus(status)

    def getStatus(self):
        return ord(self.payload[1])

    def setStatus(self, status):
        if status > 255 or status < 0:
            raise MessageError('Could not set channel status (out of range).')
        self.payload[1] = chr(status)


class VersionMessage(Message):

    def __init__(self, version='\x00\x00\x00\x00\x00\x00\x00\x00\x00'):
        Message.__init__(self, type_=MESSAGE_VERSION, payload='\x00\x00\x00\x00\x00\x00\x00\x00\x00')
        self.setVersion(version)

    def getVersion(self):
        return self.getPayload()

    def setVersion(self, version):
        if len(version) != 9:
            raise MessageError('Could not set ANT version (expected 9 bytes).')
        self.setPayload(version)


class CapabilitiesMessage(Message):

    def __init__(self, max_channels=0, max_nets=0, std_opts=0, adv_opts=0, adv_opts2=0):
        Message.__init__(self, type_=MESSAGE_CAPABILITIES, payload='\x00\x00\x00\x00')
        self.setMaxChannels(max_channels)
        self.setMaxNetworks(max_nets)
        self.setStdOptions(std_opts)
        self.setAdvOptions(adv_opts)
        if adv_opts2 is not None:
            self.setAdvOptions2(adv_opts2)
        return

    def getMaxChannels(self):
        return ord(self.payload[0])

    def getMaxNetworks(self):
        return ord(self.payload[1])

    def getStdOptions(self):
        return ord(self.payload[2])

    def getAdvOptions(self):
        return ord(self.payload[3])

    def getAdvOptions2(self):
        if len(self.payload) == 5:
            return ord(self.payload[4])
        return 0

    def setMaxChannels(self, num):
        if num > 255 or num < 0:
            raise MessageError('Could not set max channels (out of range).')
        self.payload[0] = chr(num)

    def setMaxNetworks(self, num):
        if num > 255 or num < 0:
            raise MessageError('Could not set max networks (out of range).')
        self.payload[1] = chr(num)

    def setStdOptions(self, num):
        if num > 255 or num < 0:
            raise MessageError('Could not set std options (out of range).')
        self.payload[2] = chr(num)

    def setAdvOptions(self, num):
        if num > 255 or num < 0:
            raise MessageError('Could not set adv options (out of range).')
        self.payload[3] = chr(num)

    def setAdvOptions2(self, num):
        if num > 255 or num < 0:
            raise MessageError('Could not set adv options 2 (out of range).')
        if len(self.payload) == 4:
            self.payload.append('\x00')
        self.payload[4] = chr(num)


class SerialNumberMessage(Message):

    def __init__(self, serial='\x00\x00\x00\x00'):
        Message.__init__(self, type_=MESSAGE_SERIAL_NUMBER)
        self.setSerialNumber(serial)

    def getSerialNumber(self):
        return self.getPayload()

    def setSerialNumber(self, serial):
        if len(serial) != 4:
            raise MessageError('Could not set serial number (expected 4 bytes).')
        self.setPayload(serial)