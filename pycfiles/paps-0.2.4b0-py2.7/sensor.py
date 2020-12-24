# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\paps\si\app\sensor.py
# Compiled at: 2016-04-01 12:20:26
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals
__author__ = b'd01'
__email__ = b'jungflor@gmail.com'
__copyright__ = b'Copyright (C) 2015-16, Florian JUNG'
__license__ = b'MIT'
__version__ = b'0.1.0'
__date__ = b'2016-03-29'
try:
    import Queue as queue
except ImportError:
    import queue

import select, socket, threading, time
from abc import ABCMeta
from flotils.runable import StartStopable
from flotils.loadable import Loadable
from paps.si.app.message import MsgType, Id, APPHeader, APPMessage, guess_class
from paps.si.sensorInterface import SensorStartException

class Sensor(Loadable, StartStopable):
    """ Base class for communication using the APP """
    __metaclass__ = ABCMeta

    def __init__(self, settings=None):
        if settings is None:
            settings = {}
        super(Sensor, self).__init__(settings)
        self._multicast_group = settings.get(b'multicast_group', b'239.255.136.245')
        self._multicast_ip = settings.get(b'multicast_bind_ip', self._get_local_ip())
        self._multicast_port = settings.get(b'multicast_port', 2345)
        self._multicast_ttl = settings.get(b'multicast_ttl', 3)
        self._listen_ip = settings.get(b'listen_bind_ip', self._get_local_ip())
        self._listen_port = settings.get(b'listen_port', 2346)
        self._select_timeout = settings.get(b'select_timeout', 2.5)
        self._start_block_timeout = self._select_timeout
        self._retransmit_timeout = settings.get(b'retransmit_timeout', 1)
        self._retransmit_max_tries = settings.get(b'retransmit_max_tries', 3)
        self._buffer_size = settings.get(b'receive_buffer_size', 4096)
        self._membership_request = None
        self._listen_socket = None
        self._listening = []
        self._send_seq_num = 0
        self.inbox = queue.Queue()
        self._to_ack = queue.Queue()
        self.new_packet = threading.Event()
        self._seq_ack = set()
        self._seq_ack_lock = threading.Lock()
        self._device_id = settings.get(b'device_id', Id.REQUEST)
        return

    @staticmethod
    def _get_local_ip():
        """
        Get the local ip of this device

        :return: Ip of this computer
        :rtype: str
        """
        return set([ x[4][0] for x in socket.getaddrinfo(socket.gethostname(), 80, socket.AF_INET)
                   ]).pop()

    def _init_listen_socket(self):
        """
        Init listen socket

        :rtype: None
        """
        self.debug(b'()')
        self._listen_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self._listen_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self._listen_socket.bind((self._listen_ip, self._listen_port))
        self._listening.append(self._listen_socket)

    def _shutdown_listen_socket(self):
        """
        Shutdown listening socket

        :rtype: None
        """
        self.debug(b'()')
        if self._listen_socket in self._listening:
            self._listening.remove(self._listen_socket)
        if self._listen_socket:
            self._listen_socket.close()
        self._listen_socket = None
        return

    def _send(self, ip, port, data):
        """
        Send an UDP message

        :param ip: Ip to send to
        :type ip: str
        :param port: Port to send to
        :type port: int
        :return: Number of bytes sent
        :rtype: int
        """
        return self._listen_socket.sendto(data, (ip, port))

    def _send_packet(self, ip, port, packet, update_timestamp=True, acknowledge_packet=True):
        """
        Send a packet

        :param ip: Ip to send to
        :type ip: str
        :param port: Port to send to
        :type port: int
        :param packet: Packet to be transmitted
        :type packet: APPMessage
        :param update_timestamp: Should update timestamp to current
        :type update_timestamp: bool
        :param acknowledge_packet: Should packet get acknowledged
        :type acknowledge_packet: bool
        :rtype: None
        """
        if acknowledge_packet:
            packet.header.sequence_number = self._send_seq_num
            self._send_seq_num += 1
        packet.header.device_id = self._device_id
        try:
            packed = packet.pack(update_timestamp=update_timestamp)
        except ValueError:
            self.exception(b'Failed to pack packet')
            return

        self._send(ip, port, packed)
        if acknowledge_packet:
            with self._seq_ack_lock:
                self._seq_ack.add(packet.header.sequence_number)
            self._to_ack.put((
             time.time() + self._retransmit_timeout, 1, (ip, port), packet))
        self.debug((b'Send: {}').format(packet))

    def _send_ack(self, ip, port, packet, update_timestamp=True):
        """
        Send an ack packet

        :param ip: Ip to send to
        :type ip: str
        :param port: Port to send to
        :type port: int
        :param packet: Packet to be acknowledged
        :type packet: APPMessage
        :param update_timestamp: Should update timestamp to current
        :type update_timestamp: bool
        :rtype: None
        """
        ack = APPMessage(message_type=MsgType.ACK)
        ack.header.ack_sequence_number = packet.header.sequence_number
        self._send_packet(ip, port, ack, update_timestamp=update_timestamp, acknowledge_packet=False)

    def _unpack(self, data):
        """
        Unpack data into message

        :param data: Data to be unpacked
        :type data: str | unicode
        :return: Unpacked message
        :rtype: APPMessage | APPUnjoinMessage | APPUpdateMessage  | APPJoinMessage | APPDataMessage | APPConfigMessage
        :raises paps.si.app.message.ProtocolViolation: Failed to decode
        """
        header, _ = APPHeader.unpack(data)
        cls = guess_class(header.message_type)
        if cls is None:
            self.warning((b'Unknown type {}\nHeader: {}').format(header.message_type, header))
            cls = APPMessage
        return cls.unpack(data)

    def _get_packet(self, socket):
        """
        Read packet and put it into inbox

        :param socket: Socket to read from
        :type socket: socket.socket
        :return: Read packet
        :rtype: APPMessage
        """
        data, (ip, port) = socket.recvfrom(self._buffer_size)
        packet, remainder = self._unpack(data)
        self.inbox.put((ip, port, packet))
        self.new_packet.set()
        self.debug((b'RX: {}').format(packet))
        if packet.header.sequence_number is not None:
            self._send_ack(ip, port, packet)
        ack_seq = packet.header.ack_sequence_number
        if ack_seq is not None:
            with self._seq_ack_lock:
                if ack_seq in self._seq_ack:
                    self.debug((b'Seq {} got acked').format(ack_seq))
                    self._seq_ack.remove(ack_seq)
        return packet

    def _thread_wrapper(self, function):
        """
        Wrap function for exception handling with threaded calls

        :param function: Function to call
        :type function: callable
        :rtype: None
        """
        try:
            function()
        except:
            self.exception(b'Threaded execution failed')

    def _receiving(self):
        """
        Receiving loop

        :rtype: None
        """
        while self._is_running:
            try:
                rlist, wlist, xlist = select.select(self._listening, [], [], self._select_timeout)
            except:
                self.exception(b'Failed to select socket')
                continue

            for sock in rlist:
                try:
                    self._get_packet(sock)
                except:
                    self.exception(b'Failed to receive packet')

    def _acking(self, params=None):
        """
        Packet acknowledge and retry loop

        :param params: Ignore
        :type params: None
        :rtype: None
        """
        while self._is_running:
            try:
                t, num_try, (ip, port), packet = self._to_ack.get(timeout=self._select_timeout)
            except queue.Empty:
                continue

            diff = t - time.time()
            if diff > 0:
                time.sleep(diff)
            with self._seq_ack_lock:
                if packet.header.sequence_number not in self._seq_ack:
                    continue
            if num_try <= self._retransmit_max_tries:
                self._send(ip, port, packet.pack(True))
                self._to_ack.put((
                 time.time() + self._retransmit_timeout,
                 num_try + 1,
                 (
                  ip, port),
                 packet))
            else:
                with self._seq_ack_lock:
                    try:
                        self._seq_ack.remove(packet.header.sequence_number)
                    except KeyError:
                        pass

                self.warning(b'Exceeded max tries')

    def start(self, blocking=False):
        """
        Start the interface

        :param blocking: Should the call block until stop() is called
            (default: False)
        :type blocking: bool
        :rtype: None
        :raises SensorStartException: Failed to start
        """
        try:
            self._init_listen_socket()
        except:
            self.exception((b'Failed to init listen socket ({}:{})').format(self._listen_ip, self._listen_port))
            self._shutdown_listen_socket()
            raise SensorStartException(b'Listen socket init failed')

        self.info((b'Listening on {}:{}').format(self._listen_ip, self._listen_port))
        super(Sensor, self).start(False)
        try:
            a_thread = threading.Thread(target=self._thread_wrapper, args=(
             self._receiving,))
            a_thread.daemon = True
            a_thread.start()
        except:
            self.exception(b'Failed to run receive loop')
            raise SensorStartException(b'Packet loop failed')

        super(Sensor, self).start(blocking)

    def stop(self):
        """
        Stop the interface

        :rtype: None
        """
        should_sleep = self._is_running
        super(Sensor, self).stop()
        if should_sleep:
            time.sleep(max(self._select_timeout, self._retransmit_timeout) + 1)
        if self._listen_socket is not None:
            self._shutdown_listen_socket()
        return