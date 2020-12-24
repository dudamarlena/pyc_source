# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/lib/python3.8/site-packages/hbmqtt/mqtt/disconnect.py
# Compiled at: 2020-01-25 09:04:28
# Size of source mod 2**32: 728 bytes
from hbmqtt.mqtt.packet import MQTTPacket, MQTTFixedHeader, DISCONNECT
from hbmqtt.errors import HBMQTTException

class DisconnectPacket(MQTTPacket):
    VARIABLE_HEADER = None
    PAYLOAD = None

    def __init__(self, fixed=None):
        if fixed is None:
            header = MQTTFixedHeader(DISCONNECT, 0)
        else:
            if fixed.packet_type is not DISCONNECT:
                raise HBMQTTException('Invalid fixed packet type %s for DisconnectPacket init' % fixed.packet_type)
            header = fixed
        super().__init__(header)
        self.variable_header = None
        self.payload = None