# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/lib/python3.8/site-packages/hbmqtt/mqtt/pubrel.py
# Compiled at: 2020-01-25 09:04:28
# Size of source mod 2**32: 1184 bytes
from hbmqtt.mqtt.packet import MQTTPacket, MQTTFixedHeader, PUBREL, PacketIdVariableHeader
from hbmqtt.errors import HBMQTTException

class PubrelPacket(MQTTPacket):
    VARIABLE_HEADER = PacketIdVariableHeader
    PAYLOAD = None

    @property
    def packet_id(self):
        return self.variable_header.packet_id

    @packet_id.setter
    def packet_id(self, val: int):
        self.variable_header.packet_id = val

    def __init__(self, fixed=None, variable_header=None):
        if fixed is None:
            header = MQTTFixedHeader(PUBREL, 2)
        else:
            if fixed.packet_type is not PUBREL:
                raise HBMQTTException('Invalid fixed packet type %s for PubrelPacket init' % fixed.packet_type)
            header = fixed
        super().__init__(header)
        self.variable_header = variable_header
        self.payload = None

    @classmethod
    def build(cls, packet_id):
        variable_header = PacketIdVariableHeader(packet_id)
        return PubrelPacket(variable_header=variable_header)