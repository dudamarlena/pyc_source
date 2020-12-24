# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.10-x86_64/egg/dhcpkit/ipv6/server/listeners/udp.py
# Compiled at: 2016-11-14 15:54:22
# Size of source mod 2**32: 8007 bytes
"""
UDP implementations of listeners and repliers
"""
import logging, socket
from ipaddress import IPv6Address
from dhcpkit.common.server.logging import DEBUG_PACKETS
from dhcpkit.ipv6 import CLIENT_PORT, SERVER_PORT
from dhcpkit.ipv6.messages import RelayReplyMessage
from dhcpkit.ipv6.options import InterfaceIdOption
from dhcpkit.ipv6.server.listeners import IncomingPacketBundle, Listener, ListeningSocketError, Replier, increase_message_counter
from typing import Iterable, Tuple
logger = logging.getLogger(__name__)

class UDPListener(Listener):
    __doc__ = '\n    A wrapper for a normal socket that bundles a socket to listen on with a (potentially different) socket\n    to send replies from.\n\n    :type interface_name: str\n    :type interface_index: int\n    :type listen_socket: socket.socket\n    :type listen_address: IPv6Address\n    :type reply_socket: socket.socket\n    :type reply_address: IPv6Address\n    :type global_address: IPv6Address\n    '

    def __init__(self, interface_name: str, listen_socket: socket.socket, reply_socket: socket.socket=None,
                 global_address: IPv6Address=None,
                 marks: Iterable[str]=None):
        """
        Initialise listener.

        :param interface_name: The name of the interface
        :param listen_socket: The socket we are listening on, may be a unicast or multicast socket
        :param reply_socket: The socket replies are sent from, must be a unicast socket
        :param global_address: The global address on the listening interface
        :param marks: Marks attached to this listener
        """
        self.interface_name = interface_name
        self.interface_id = interface_name.encode('utf-8')
        self.listen_socket = listen_socket
        self.reply_socket = reply_socket
        self.marks = list(marks or [])
        if self.reply_socket is None:
            self.reply_socket = self.listen_socket
        if self.listen_socket.family != socket.AF_INET6 or self.listen_socket.proto != socket.IPPROTO_UDP or self.reply_socket.family != socket.AF_INET6 or self.reply_socket.proto != socket.IPPROTO_UDP:
            raise ListeningSocketError('Listen and reply sockets have to be IPv6 UDP sockets')
        listen_sockname = self.listen_socket.getsockname()
        reply_sockname = self.reply_socket.getsockname()
        if listen_sockname[1] != SERVER_PORT or reply_sockname[1] != SERVER_PORT:
            raise ListeningSocketError('Listen and reply sockets have to be on port {}'.format(SERVER_PORT))
        if listen_sockname[3] != reply_sockname[3]:
            raise ListeningSocketError('Listen and reply sockets have to be on same interface')
        self.interface_index = listen_sockname[3]
        self.listen_address = IPv6Address(listen_sockname[0].split('%')[0])
        self.reply_address = IPv6Address(reply_sockname[0].split('%')[0])
        if global_address:
            self.global_address = global_address
        else:
            if not self.listen_address.is_link_local and not self.listen_address.is_multicast:
                self.global_address = self.listen_address
            else:
                raise ListeningSocketError('Cannot determine global address on interface {}'.format(self.interface_name))
        if self.listen_address.is_unspecified or self.reply_address.is_unspecified:
            raise ListeningSocketError('This server only supports listening on explicit address, not on wildcard')
        if self.listen_address.is_multicast:
            if not self.reply_address.is_link_local:
                raise ListeningSocketError('Multicast listening addresses need link-local reply socket')
        if not self.listen_address.is_multicast:
            if self.reply_socket != self.listen_socket:
                raise ListeningSocketError("Unicast listening addresses can't use separate reply sockets")

    def recv_request(self) -> Tuple[(IncomingPacketBundle, Replier)]:
        """
        Receive incoming messages

        :return: The incoming packet data and a replier object
        """
        data, sender = self.listen_socket.recvfrom(65536)
        message_counter = increase_message_counter()
        message_id = '#{:06X}'.format(message_counter)
        logger.log(DEBUG_PACKETS, '{message_id}: Received message from {client_addr} port {port} on {interface}'.format(message_id=message_id, client_addr=sender[0], port=sender[1], interface=self.interface_name))
        interface_id_option = InterfaceIdOption(interface_id=self.interface_id)
        packet_bundle = IncomingPacketBundle(message_id=message_id, data=data, source_address=IPv6Address(sender[0].split('%')[0]), link_address=self.global_address, interface_index=self.interface_index, received_over_multicast=self.listen_address.is_multicast, received_over_tcp=False, marks=self.marks, relay_options=[
         interface_id_option])
        replier = UDPReplier(self.reply_socket)
        return (
         packet_bundle, replier)

    def fileno(self) -> int:
        """
        The fileno of the listening socket, so this object can be used by select()

        :return: The file descriptor
        """
        return self.listen_socket.fileno()


class UDPReplier(Replier):
    __doc__ = '\n    A class to send replies to the client\n    '

    def __init__(self, reply_socket: socket.socket):
        self.reply_socket = reply_socket

    def send_reply(self, outgoing_message: RelayReplyMessage) -> bool:
        """
        Send a reply to the client

        :param outgoing_message: The message to send, including a wrapping RelayReplyMessage
        :return: Whether sending was successful
        """
        reply = outgoing_message.relayed_message
        port = isinstance(reply, RelayReplyMessage) and SERVER_PORT or CLIENT_PORT
        destination_address = str(outgoing_message.peer_address)
        data = reply.save()
        interface_index = 0
        interface_name = 'unknown'
        interface_id_option = outgoing_message.get_option_of_type(InterfaceIdOption)
        if interface_id_option:
            try:
                interface_name = interface_id_option.interface_id.decode(encoding='utf-8', errors='replace')
                interface_index = socket.if_nametoindex(interface_id_option.interface_id)
            except OSError:
                pass

        destination = (destination_address, port, 0, interface_index)
        sent_length = self.reply_socket.sendto(data, destination)
        success = len(data) == sent_length
        if success:
            logger.log(DEBUG_PACKETS, 'Sent {message_type} to {client_addr} port {port} on {interface}'.format(message_type=outgoing_message.inner_message.__class__.__name__, client_addr=destination_address, port=port, interface=interface_name))
        else:
            logger.error('Could not send {message_type} to {client_addr} port {port} on {interface}'.format(message_type=outgoing_message.inner_message.__class__.__name__, client_addr=destination_address, port=port, interface=interface_name))
        return success