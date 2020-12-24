# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\paps\si\app\sensorServer.py
# Compiled at: 2016-04-01 12:21:27
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals
__author__ = b'd01'
__email__ = b'jungflor@gmail.com'
__copyright__ = b'Copyright (C) 2015-16, Florian JUNG'
__license__ = b'MIT'
__version__ = b'0.1.0'
__date__ = b'2016-03-31'
import socket, platform, threading
from ..sensorInterface import SensorServerInterface, SensorStartException
from .sensor import Sensor
from .message import Id, MsgType, ProtocolViolation, APPConfigMessage, APPMessage
from ...person import Person

class SensorServer(Sensor, SensorServerInterface):
    """ APP sensor server """

    def __init__(self, settings=None):
        if settings is None:
            settings = {}
        super(SensorServer, self).__init__(settings)
        self._device_id = Id.SERVER
        self._packet_wait = settings.get(b'packet_wait_timeout', 1.5)
        self._multicast_bind_port = settings.get(b'multicast_bind_port', self._multicast_port)
        self._clients = {}
        self._key2deviceId = {}
        self._multicast_socket = None
        self._is_stopped = threading.Event()
        return

    def _packet_loop(self):
        """
        Loop (while running) the inbox and handle incoming packages

        :rtype: None
        """
        while not self._is_stopped.is_set():
            if self.inbox.empty() and not self.new_packet.wait(self._packet_wait):
                continue
            ip, port, packet = self.inbox.get()
            if self.inbox.empty():
                self.new_packet.clear()
            self._do_packet(packet, ip, port)

    def _do_packet(self, packet, ip, port):
        """
        React to incoming packet

        :param packet: Packet to handle
        :type packet: T >= paps.si.app.message.APPMessage
        :param ip: Client ip address
        :type ip: unicode
        :param port: Client port
        :type port: int
        :rtype: None
        """
        msg_type = packet.header.message_type
        if msg_type == MsgType.JOIN:
            self._do_join_packet(packet, ip, port)
        elif msg_type == MsgType.UNJOIN:
            self._do_unjoin_packet(packet, ip, port)
        elif msg_type == MsgType.UPDATE:
            self._do_update_packet(packet, ip, port)

    def _do_join_packet(self, packet, ip, port):
        """
        React to join packet - add a client to this server

        :param packet: Packet from client that wants to join
        :type packet: paps.si.app.message.APPJoinMessage
        :param ip: Client ip address
        :type ip: unicode
        :param port: Client port
        :type port: int
        :rtype: None
        """
        self.debug(b'()')
        device_id = packet.header.device_id
        key = (b'{}:{}').format(ip, port)
        if device_id == Id.REQUEST:
            device_id = self._new_device_id(key)
        client = self._clients.get(device_id, {})
        data = {}
        if packet.payload:
            try:
                data = packet.payload
            except:
                data = {}

        client[b'device_id'] = device_id
        client[b'key'] = key
        people = []
        try:
            for index, person_dict in enumerate(data[b'people']):
                person = Person()
                person.from_dict(person_dict)
                person.id = (b'{}.{}').format(device_id, person.id)
                people.append(person)

            self.changer.on_person_new(people)
        except:
            self.exception(b'Failed to update people')
            return

        client[b'people'] = people
        client_dict = dict(client)
        del client_dict[b'people']
        self._send_packet(ip, port, APPConfigMessage(payload=client_dict))
        self._clients[device_id] = client
        self._key2deviceId[key] = device_id

    def _do_unjoin_packet(self, packet, ip, port):
        """
        React to unjoin packet - remove a client from this server

        :param packet: Packet from client that wants to join
        :type packet: paps.si.app.message.APPJoinMessage
        :param ip: Client ip address
        :type ip: unicode
        :param port: Client port
        :type port: int
        :rtype: None
        """
        self.debug(b'()')
        device_id = packet.header.device_id
        if device_id <= Id.SERVER:
            self.error(b'ProtocolViolation: Invalid device id')
            return
        client = self._clients.get(device_id)
        if not client:
            self.error(b'ProtocolViolation: Client is not registered')
            return
        key = (b'{}:{}').format(ip, port)
        if client[b'key'] != key:
            self.error((b'ProtocolViolation: Client key ({}) has changed: {}').format(client[b'key'], key))
            return
        try:
            self.changer.on_person_leave(client[b'people'])
        except:
            self.exception(b'Failed to remove people')
            return

        del self._clients[device_id]
        del self._key2deviceId[key]
        del client

    def _do_update_packet(self, packet, ip, port):
        """
        React to update packet - people/person on a device have changed

        :param packet: Packet from client with changes
        :type packet: paps.si.app.message.APPUpdateMessage
        :param ip: Client ip address
        :type ip: unicode
        :param port: Client port
        :type port: int
        :rtype: None
        """
        self.debug(b'()')
        device_id = packet.header.device_id
        if device_id <= Id.SERVER:
            self.error(b'ProtocolViolation: Invalid device id')
            return
        else:
            client = self._clients.get(device_id, None)
            if not client:
                self.error(b'ProtocolViolation: Client is not registered')
                return
            key = (b'{}:{}').format(ip, port)
            if client[b'key'] != key:
                self.error((b'ProtocolViolation: Client key ({}) has changed: {}').format(client[b'key'], key))
                return
            try:
                people = packet.people()
            except ProtocolViolation:
                self.exception(b'Failed to decode people from packet')
                return

            if len(people) != len(client[b'people']):
                self.error(b'ProtocolViolation: Incorrect number of people updated')
            changed = []
            for index, person in enumerate(people):
                old = client[b'people'][index]
                person.id = old.id
                if person != old:
                    old.sitting = person.sitting
                    changed.append(old)

            if changed:
                try:
                    self.changer.on_person_update(changed)
                except:
                    self.exception(b'Failed to notify people update')
                    return

            else:
                self.debug(b'No people updated')
            return

    def _new_device_id(self, key):
        """
        Generate a new device id or return existing device id for key

        :param key: Key for device
        :type key: unicode
        :return: The device id
        :rtype: int
        """
        device_id = Id.SERVER + 1
        if key in self._key2deviceId:
            return self._key2deviceId[key]
        while device_id in self._clients:
            device_id += 1

        return device_id

    def _init_multicast_socket(self):
        """
        Init multicast socket

        :rtype: None
        """
        self.debug(b'()')
        self._multicast_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self._multicast_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self._multicast_socket.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_IF, socket.inet_aton(self._multicast_ip))
        self._multicast_socket.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, self._multicast_ttl)
        self._add_membership_multicast_socket()
        if platform.system().lower() == b'darwin':
            self._multicast_socket.bind((b'0.0.0.0', self._multicast_bind_port))
        else:
            self._multicast_socket.bind((
             self._multicast_ip, self._multicast_bind_port))
        self._listening.append(self._multicast_socket)

    def _shutdown_multicast_socket(self):
        """
        Shutdown multicast socket

        :rtype: None
        """
        self.debug(b'()')
        self._drop_membership_multicast_socket()
        self._listening.remove(self._multicast_socket)
        self._multicast_socket.close()
        self._multicast_socket = None
        return

    def _add_membership_multicast_socket(self):
        """
        Make membership request to multicast

        :rtype: None
        """
        self._membership_request = socket.inet_aton(self._multicast_group) + socket.inet_aton(self._multicast_ip)
        self._multicast_socket.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, self._membership_request)

    def _drop_membership_multicast_socket(self):
        """
        Drop membership to multicast

        :rtype: None
        """
        self._multicast_socket.setsockopt(socket.IPPROTO_IP, socket.IP_DROP_MEMBERSHIP, self._membership_request)
        self._membership_request = None
        return

    def start(self, blocking=False):
        """
        Start the interface

        :param blocking: Should the call block until stop() is called
            (default: False)
        :type blocking: bool
        :rtype: None
        :raises SensorStartException: Failed to start
        """
        self.debug(b'()')
        try:
            self._init_multicast_socket()
        except:
            self._multicast_socket = None
            self.exception(b'Failed to init multicast socket')
            raise SensorStartException(b'Multicast socket init failed')

        super(SensorServer, self).start(blocking=False)
        self._is_stopped.clear()
        try:
            a_thread = threading.Thread(target=self._thread_wrapper, args=(
             self._packet_loop,))
            a_thread.daemon = True
            a_thread.start()
        except:
            self.exception(b'Failed to run packet loop')
            raise SensorStartException(b'Packet loop failed')

        self.info(b'Started')
        super(Sensor, self).start(blocking)
        return

    def stop(self):
        """
        Stop the sensor server (soft stop - signal packet loop to stop)
        Warning: Is non blocking (server might still do something after this!)

        :rtype: None
        """
        self.debug(b'()')
        super(SensorServer, self).stop()
        if self._multicast_socket is not None:
            self._shutdown_multicast_socket()
        self._is_stopped.set()
        return