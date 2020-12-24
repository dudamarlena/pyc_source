# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.10-x86_64/egg/dhcpkit/ipv6/server/listeners/tcp.py
# Compiled at: 2016-11-14 15:54:47
# Size of source mod 2**32: 13199 bytes
"""
Code to keep the receiving and sending sockets together. When receiving traffic on a link-local multicast address
the reply should be sent from a link-local address on the receiving interface. This class makes it easy to keep those
together.
"""
import logging, multiprocessing, socket, weakref
from ipaddress import IPv6Address, IPv6Network
from multiprocessing import Lock
from struct import pack, unpack_from
from dhcpkit.common.server.logging import DEBUG_PACKETS
from dhcpkit.ipv6 import SERVER_PORT
from dhcpkit.ipv6.messages import RelayReplyMessage
from dhcpkit.ipv6.options import InterfaceIdOption
from dhcpkit.ipv6.server.listeners import ClosedListener, IncomingPacketBundle, IncompleteMessage, Listener, ListenerCreator, ListeningSocketError, Replier, increase_message_counter
from dhcpkit.ipv6.utils import is_global_unicast
from typing import Iterable, Optional, Tuple
logger = logging.getLogger(__name__)

class TCPConnection(Listener):
    __doc__ = '\n    A TCP connection listener for DHCPv6 messages\n    '

    def __init__(self, interface_name: str, connected_socket: socket.socket, write_lock: Lock, global_address: IPv6Address, marks: Iterable[str]=None):
        """
        Initialise listener.

        :param interface_name: The name of the interface
        :param connected_socket: The socket we are listening on and will send replies to
        :param global_address: The global address on the listening interface
        :param marks: Marks attached to this listener
        """
        self.interface_name = interface_name
        self.interface_id = interface_name.encode('utf-8')
        self.connected_socket = connected_socket
        self.global_address = global_address
        self.marks = list(marks or [])
        self.write_lock = write_lock
        if self.connected_socket.family != socket.AF_INET6 or self.connected_socket.proto != socket.IPPROTO_TCP:
            raise ListeningSocketError('TCP Listen sockets have to be IPv6 TCP sockets')
        our_sockname = self.connected_socket.getsockname()
        if our_sockname[1] != SERVER_PORT:
            raise ListeningSocketError('Connected sockets have to be on port {}'.format(SERVER_PORT))
        self.interface_index = our_sockname[3]
        peer_sockname = self.connected_socket.getpeername()
        self.client_address = IPv6Address(peer_sockname[0].split('%')[0])
        self.client_port = peer_sockname[1]
        self.buffer = b''

    def packet_from_buffer(self):
        """
        Create a packet and replier from the data in the buffer

        :return: The incoming packet data and a replier object
        """
        message_length = unpack_from('!H', self.buffer)[0]
        data = self.buffer[2:2 + message_length]
        self.buffer = self.buffer[2 + message_length:]
        message_counter = increase_message_counter()
        message_id = '#{:06X}'.format(message_counter)
        logger.log(DEBUG_PACKETS, '{message_id}: Received message from {client_addr} port {port}'.format(message_id=message_id, client_addr=str(self.client_address), port=self.client_port))
        interface_id_option = InterfaceIdOption(interface_id=self.interface_id)
        packet_bundle = IncomingPacketBundle(message_id=message_id, data=data, source_address=self.client_address, link_address=self.global_address, interface_index=self.interface_index, received_over_multicast=False, received_over_tcp=True, marks=self.marks, relay_options=[
         interface_id_option])
        replier = TCPReplier(self.connected_socket, self.write_lock)
        return (
         packet_bundle, replier)

    def recv_data_into_buffer(self, amount: int) -> int:
        """
        Receive data into the buffer and do proper error handling

        :param amount: How much data do we want?
        :return: How much data did we receive?
        """
        data = self.connected_socket.recv(amount)
        if data == b'':
            logger.info('TCP connection to {client_addr} port {port} closed'.format(client_addr=str(self.client_address), port=self.client_port))
            raise ClosedListener
        self.buffer += data
        return len(data)

    def recv_request(self) -> Tuple[(IncomingPacketBundle, Replier)]:
        """
        Receive incoming messages

        :return: The incoming packet data and a replier object
        """
        buffer_length = len(self.buffer)
        if buffer_length < 2:
            buffer_length += self.recv_data_into_buffer(2 - buffer_length)
        if buffer_length >= 2:
            message_length = unpack_from('!H', self.buffer)[0]
            we_already_have = buffer_length - 2
            remaining_data = message_length - we_already_have
            if remaining_data > 0:
                buffer_length += self.recv_data_into_buffer(remaining_data)
            we_already_have = buffer_length - 2
            if we_already_have >= message_length:
                return self.packet_from_buffer()
        raise IncompleteMessage

    def fileno(self) -> int:
        """
        The fileno of the listening socket, so this object can be used by select()

        :return: The file descriptor
        """
        return self.connected_socket.fileno()


class TCPReplier(Replier):
    __doc__ = '\n    A class to send replies to the client\n    '
    can_send_multiple = True

    def __init__(self, reply_socket: socket.socket, reply_lock: Lock):
        self.reply_socket = reply_socket
        self.reply_lock = reply_lock
        peer_sockname = self.reply_socket.getpeername()
        self.client_address = IPv6Address(peer_sockname[0].split('%')[0])
        self.client_port = peer_sockname[1]

    def send_reply(self, outgoing_message: RelayReplyMessage) -> bool:
        """
        Send a reply to the client

        :param outgoing_message: The message to send, including a wrapping RelayReplyMessage
        :return: Whether sending was successful
        """
        reply = outgoing_message.relayed_message
        message_data = reply.save()
        data = pack('!H', len(message_data)) + message_data
        try:
            with self.reply_lock:
                self.reply_socket.settimeout(300)
                self.reply_socket.sendall(data)
                self.reply_socket.settimeout(None)
            logger.log(DEBUG_PACKETS, 'Sent {message_type} to {client_addr} port {port}'.format(message_type=outgoing_message.inner_message.__class__.__name__, client_addr=str(self.client_address), port=self.client_port))
            return True
        except OSError as e:
            logger.error('Could not send {message_type} to {client_addr} port {port}: {exception}'.format(message_type=outgoing_message.inner_message.__class__.__name__, client_addr=str(self.client_address), port=self.client_port, exception=e))
            return False


class TCPConnectionListener(ListenerCreator):
    __doc__ = '\n    Wrapper for a listening TCP socket. This is not a listener in the DHCPKit sense of the concept. DHCPKit listeners\n    receive DHCPv6 messages, which is done on an established connection.\n\n    :type interface_name: str\n    :type interface_index: int\n    :type listen_socket: socket.socket\n    :type listen_address: IPv6Address\n    :type global_address: IPv6Address\n    '

    def __init__(self, interface_name: str, listen_socket: socket.socket, global_address: IPv6Address=None,
                 marks: Iterable[str]=None,
                 max_connections: int=10, allow_from: Iterable[IPv6Network]=None):
        """
        Initialise TCP listener.

        :param interface_name: The name of the interface
        :param listen_socket: The socket we are listening on, may be a unicast or multicast socket
        :param global_address: The global address on the listening interface
        :param marks: Marks attached to this listener
        """
        self.interface_name = interface_name
        self.interface_id = interface_name.encode('utf-8')
        self.marks = list(marks or [])
        self.max_connections = max_connections
        self.allow_from = list(allow_from or [])
        self.listen_socket = listen_socket
        self.listen_socket.setblocking(False)
        if self.listen_socket.family != socket.AF_INET6 or self.listen_socket.proto != socket.IPPROTO_TCP:
            raise ListeningSocketError('TCP Listen sockets have to be IPv6 TCP sockets')
        listen_sockname = self.listen_socket.getsockname()
        if listen_sockname[1] != SERVER_PORT:
            raise ListeningSocketError('TCP Listen sockets have to be on port {}'.format(SERVER_PORT))
        self.interface_index = listen_sockname[3]
        self.listen_address = IPv6Address(listen_sockname[0].split('%')[0])
        if global_address:
            self.global_address = global_address
        else:
            if is_global_unicast(self.listen_address):
                self.global_address = self.listen_address
            else:
                raise ListeningSocketError('Cannot determine global address on interface {}'.format(self.interface_name))
        if self.listen_address.is_unspecified:
            raise ListeningSocketError('This server only supports listening on explicit address, not on wildcard')
        self.manager = multiprocessing.Manager()
        self.open_sockets = weakref.WeakSet()

    def create_listener(self) -> Optional[TCPConnection]:
        """
        Accept incoming connection

        :return: The connection object
        """
        try:
            connected_socket, client = self.listen_socket.accept()
        except OSError:
            return

        if len(self.open_sockets) >= self.max_connections:
            logger.warning('More than {max_connections} open TCP connections, rejecting connection from {client_addr} port {port}'.format(max_connections=self.max_connections, client_addr=client[0], port=client[1]))
            connected_socket.shutdown(socket.SHUT_RDWR)
            connected_socket.close()
            return
        if self.allow_from:
            client_address = IPv6Address(client[0].split('%')[0])
            if not any([client_address in allowed_range for allowed_range in self.allow_from]):
                logger.error('Rejecting TCP connection from {client_addr} port {port}'.format(client_addr=client[0], port=client[1]))
                connected_socket.shutdown(socket.SHUT_RDWR)
                connected_socket.close()
                return
        logger.info('Incoming TCP connection from {client_addr} port {port}'.format(client_addr=client[0], port=client[1]))
        self.open_sockets.add(connected_socket)
        lock = self.manager.Lock()
        return TCPConnection(interface_name=self.interface_name, connected_socket=connected_socket, write_lock=lock, global_address=self.global_address, marks=self.marks)

    def fileno(self) -> int:
        """
        The fileno of the listening socket, so this object can be used by select()

        :return: The file descriptor
        """
        return self.listen_socket.fileno()