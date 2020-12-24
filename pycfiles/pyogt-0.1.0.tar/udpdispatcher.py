# uncompyle6 version 3.6.7
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/pyogp/lib/base/message/udpdispatcher.py
# Compiled at: 2010-02-07 17:28:31
__doc__ = '\nContributors can be viewed at:\nhttp://svn.secondlife.com/svn/linden/projects/2008/pyogp/lib/base/trunk/CONTRIBUTORS.txt \n\n$LicenseInfo:firstyear=2008&license=apachev2$\n\nCopyright 2009, Linden Research, Inc.\n\nLicensed under the Apache License, Version 2.0.\nYou may obtain a copy of the License at:\n    http://www.apache.org/licenses/LICENSE-2.0\nor in \n    http://svn.secondlife.com/svn/linden/projects/2008/pyogp/lib/base/LICENSE.txt\n\n$/LicenseInfo$\n'
from logging import getLogger
import traceback
from circuit import CircuitManager
from msgtypes import MsgType, MsgBlockType, MsgFrequency, PacketLayout, EndianType, PackFlags, sizeof
from udpserializer import UDPMessageSerializer
from udpdeserializer import UDPMessageDeserializer
from data_unpacker import DataUnpacker
from message import Message, Block
from pyogp.lib.base.message.message_dot_xml import MessageDotXML
from pyogp.lib.base.network.net import NetUDPClient
from pyogp.lib.base import exc
from pyogp.lib.base.settings import Settings
from pyogp.lib.base.helpers import Helpers
logger = getLogger('message.udpdispatcher')

class UDPDispatcher(object):
    __module__ = __name__

    def __init__(self, udp_client=None, settings=None, message_handler=None, message_template=None, message_xml=None):
        self.packets_in = 0
        self.packets_out = 0
        self.circuit_manager = CircuitManager()
        self.data_unpacker = DataUnpacker()
        self.receive_packet_id = -1
        self.socket = None
        if udp_client == None:
            self.udp_client = NetUDPClient()
        else:
            self.udp_client = udp_client
        self.socket = self.udp_client.start_udp_connection()
        if settings != None:
            self.settings = settings
        else:
            self.settings = Settings()
        if not message_template:
            self.message_template = None
        elif isinstance(message_template, file):
            self.message_template = message_template
        else:
            log.warning('%s parameter is expected to be a filehandle, it is a %s.                         Using the embedded message_template.msg' % (message_template, type(message_template)))
            self.message_template = None
        if not message_xml:
            self.message_xml = MessageDotXML()
        else:
            self.message_xml = message_xml
        self.helpers = Helpers()
        if message_handler != None:
            self.message_handler = message_handler
        elif self.settings.HANDLE_PACKETS:
            from pyogp.lib.base.message.message_handler import MessageHandler
            self.message_handler = MessageHandler()
        self.udp_deserializer = UDPMessageDeserializer(self.message_handler, self.settings, message_template=self.message_template)
        self.udp_serializer = UDPMessageSerializer(message_template=self.message_template)
        return

    def find_circuit(self, host):
        circuit = self.circuit_manager.get_circuit(host)
        if circuit == None:
            circuit = self.circuit_manager.add_circuit(host, self.receive_packet_id)
        return circuit

    def receive_check(self, host, msg_buf, msg_size):
        recv_packet = None
        if msg_size > 0:
            circuit = self.find_circuit(host)
            if circuit == None:
                raise exc.CircuitNotFound(host, 'preparing to check for packets')
            self.packets_in += 1
            recv_packet = self.udp_deserializer.deserialize(msg_buf)
            if recv_packet == None:
                send_flags = ord(msg_buf[0])
                packet_id = self.data_unpacker.unpack_data(msg_buf, MsgType.MVT_U32, 1, endian_type=EndianType.BIG)
                circuit.collect_ack(packet_id)
                return
            if circuit.is_trusted and recv_packet.trusted == False:
                return
            circuit.handle_packet(recv_packet)
            if self.settings.ENABLE_UDP_LOGGING:
                if self.settings.ENABLE_BYTES_TO_HEX_LOGGING:
                    hex_string = '<=>' + self.helpers.bytes_to_hex(msg_buf)
                else:
                    hex_string = ''
                if self.settings.ENABLE_HOST_LOGGING:
                    host_string = ' (%s)' % host
                else:
                    host_string = ''
                if not self.settings.PROXY_LOGGING:
                    logger.debug('Received packet%s : %s (%s)%s' % (host_string, recv_packet.name, recv_packet.packet_id, hex_string))
            if self.settings.HANDLE_PACKETS:
                self.message_handler.handle(recv_packet)
        return recv_packet

    def send_reliable(self, message, host, retries):
        """ Wants to be acked """
        return self.__send_message(message, host, reliable=True, retries=retries)

    def send_retry(self, message, host):
        """ This is a retry because we didn't get acked """
        return self.__send_message(host, message, retrying=True)

    def send_message(self, message, host):
        return self.__send_message(message, host)

    def __send_message(self, message, host, reliable=False, retries=0, retrying=False):
        """ Sends the message that is currently built to the desired host """
        if host.is_ok() == False:
            return
        if isinstance(message, Message):
            packet = message
        else:
            packet = message()
        if self.settings.HANDLE_OUTGOING_PACKETS:
            self.message_handler.handle(packet)
        circuit = self.find_circuit(host)
        if reliable == True:
            circuit.prepare_packet(packet, PackFlags.LL_RELIABLE_FLAG, retries)
            if circuit.unack_packet_count <= 0:
                self.circuit_manager.unacked_circuits[host] = circuit
        elif retrying == True:
            circuit.prepare_packet(packet, PackFlags.LL_RESENT_FLAG)
        else:
            circuit.prepare_packet(packet)
        try:
            send_buffer = self.udp_serializer.serialize(packet)
            if self.settings.ENABLE_UDP_LOGGING:
                if packet.name in self.settings.UDP_SPAMMERS and self.settings.DISABLE_SPAMMERS:
                    pass
                else:
                    if self.settings.ENABLE_BYTES_TO_HEX_LOGGING:
                        hex_string = '<=>' + self.helpers.bytes_to_hex(send_buffer)
                    else:
                        hex_string = ''
                    if self.settings.ENABLE_HOST_LOGGING:
                        host_string = ' (%s)' % host
                    else:
                        host_string = ''
                    logger.debug('Sent packet    %s : %s (%s)%s' % (host_string, packet.name, packet.packet_id, hex_string))
            self.udp_client.send_packet(self.socket, send_buffer, host)
            self.packets_out += 1
            return send_buffer
        except Exception, error:
            logger.warning('Error trying to serialize the following packet: %s' % packet)
            traceback.print_exc()
            return

    def process_acks(self):
        """ resends all of our messages that were unacked, and acks all
            the messages that others are waiting to be acked. """
        self.__resend_all_unacked()
        self.__send_acks()

    def __resend_all_unacked(self):
        """ Resends all packets sent that haven't yet been acked. """
        for circuit in self.circuit_manager.unacked_circuits.values():
            for unacked_packet in circuit.unacked_packets.values():
                unacked_packet.retries -= 1
                self.send_buffer = ''
                self.send_buffer += unacked_packet.buffer
                self.send_retry(unacked_packet.host, unacked_packet.buffer)
                if unacked_packet.retries <= 0:
                    circuit.final_retry_packets[unacked_packet.packet_id] = unacked_packet
                    del circuit.unacked_packets[unacked_packet.packet_id]

    def __send_acks(self):
        """ Acks all packets received that we haven't acked yet. """
        for circuit in self.circuit_manager.circuit_map.values():
            acks_this_packet = 0
            msg = None
            for packet_id in circuit.acks:
                if acks_this_packet == 0:
                    msg = Message('PacketAck')
                block = Block('Packets', ID=packet_id)
                msg.add_block(block)
                if self.settings.LOG_VERBOSE and not self.settings.DISABLE_SPAMMERS:
                    logger.debug('Acking packet id: %s' % packet_id)
                acks_this_packet += 1
                if acks_this_packet > 250:
                    self.send_message(msg, circuit.host)
                    acks_this_packet = 0

            if acks_this_packet > 0:
                self.send_message(msg, circuit.host)
            circuit.acks = []

        return

    def has_unacked(self):
        for circuit in self.circuit_manager.circuit_map.values():
            if len(circuit.acks) > 0:
                return True

        return False

    def __repr__(self):
        return 'UDPDispatcher to %s' % str(self.udp_client.sender)