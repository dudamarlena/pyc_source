# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/lib/python3.8/site-packages/hbmqtt/mqtt/unsuback.py
# Compiled at: 2020-01-25 09:04:28
# Size of source mod 2**32: 996 bytes
from hbmqtt.mqtt.packet import MQTTPacket, MQTTFixedHeader, UNSUBACK, PacketIdVariableHeader
from hbmqtt.errors import HBMQTTException

class UnsubackPacket(MQTTPacket):
    VARIABLE_HEADER = PacketIdVariableHeader
    PAYLOAD = None

    def __init__(self, fixed=None, variable_header=None, payload=None):
        if fixed is None:
            header = MQTTFixedHeader(UNSUBACK, 0)
        else:
            if fixed.packet_type is not UNSUBACK:
                raise HBMQTTException('Invalid fixed packet type %s for UnsubackPacket init' % fixed.packet_type)
            header = fixed
        super().__init__(header)
        self.variable_header = variable_header
        self.payload = payload

    @classmethod
    def build(cls, packet_id):
        variable_header = PacketIdVariableHeader(packet_id)
        return cls(variable_header=variable_header)