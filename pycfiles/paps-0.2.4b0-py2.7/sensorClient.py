# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\paps\si\app\sensorClient.py
# Compiled at: 2016-04-01 12:21:09
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
import time, threading
from .sensor import Sensor
from ..sensorInterface import SensorClientInterface, SensorUpdateException, SensorJoinException, SensorStartException
from .message import MsgType, Id, APPJoinMessage, APPUnjoinMessage, APPUpdateMessage, format_data

class SensorClient(Sensor, SensorClientInterface):
    """ APP sensor client """

    def __init__(self, settings=None):
        if settings is None:
            settings = {}
        super(SensorClient, self).__init__(settings)
        self._packet_timeout = settings.get(b'packet_wait_timeout', 1.5)
        self._start_block_timeout = max(self._packet_timeout, self._select_timeout)
        self._join_retry_timeout = settings.get(b'join_retry_timeout', 5.0)
        self._join_retry_count = settings.get(b'join_retry_number', 3)
        self._server_ip = None
        self._server_port = None
        self._joined = threading.Event()
        return

    def join(self, people):
        """
        Join the local audience
        (a config message should be received on success)
        Validates that there are people to join and that each of them
        has a valid unique id

        :param people: Which people does this sensor have
        :type people: list[paps.person.Person]
        :rtype: None
        :raises SensorJoinException: Failed to join
        """
        tries = 0
        if not people:
            raise SensorJoinException(b'No people given')
        ids = set()
        for person in people:
            if not person.id and person.id != 0:
                raise SensorJoinException(b'Invalid id for one or more people')
            if person.id in ids:
                raise SensorJoinException((b'Id {} not unique').format(person.id))
            ids.add(person.id)

        while self._is_running and tries < self._join_retry_count:
            packet = APPJoinMessage(payload={b'people': [ person.to_dict() for person in people ]})
            self._send_packet(self._multicast_group, self._multicast_port, packet)
            if self._joined.wait(self._join_retry_timeout):
                break
            with self._seq_ack_lock:
                packet_ackd = packet.header.sequence_number not in self._seq_ack
            if packet_ackd and self._joined.wait(1.0):
                break
            tries += 1
            self.warning((b'Unsuccessful attempt joining audience # {}').format(tries))

        if not self._joined.is_set() or tries >= self._join_retry_count:
            raise SensorJoinException(b'No config packet received')
        self.info(b'Joined the audience')

    def unjoin(self):
        """
        Leave the local audience

        :rtype: None
        :raises SensorJoinException: Failed to leave
        """
        self.debug(b'()')
        if self._joined.is_set():
            packet = APPUnjoinMessage(device_id=Id.NOT_SET)
            self._send_packet(self._server_ip, self._server_port, packet)
            self._joined.clear()
            self.info(b'Left the audience')

    def config(self, settings):
        """
        Configuration has changed - config this module and lower layers
        (calls on_config - if set)

        :param settings: New configuration
        :type settings: dict
        :rtype: None
        :raises SensorUpdateException: Failed to update
        """
        self.debug(b'()')
        try:
            self._device_id = settings[b'device_id']
            self._packet_timeout = settings.get(b'packet_wait_timeout', self._packet_timeout)
            self._server_ip = settings.get(b'server_ip', self._server_ip)
            self._server_port = settings.get(b'server_port', self._server_port)
        except KeyError:
            raise SensorUpdateException(b'Key not in settings')

        if callable(self.on_config):
            try:
                self.on_config(settings)
            except:
                self.exception(b'Failed to update remote config')
                raise SensorUpdateException(b'Remote config failed')

    def person_update(self, people):
        """
        Update the status of people

        :param people: All people of this sensor
        :type people: list[paps.person.Person]
        :rtype: None
        :raises SensorUpdateException: Failed to update
        """
        packet = APPUpdateMessage(device_id=Id.NOT_SET, people=people)
        self._send_packet(self._server_ip, self._server_port, packet, acknowledge_packet=False)

    def _packet_loop(self):
        """
        Packet processing loop

        :rtype: None
        """
        while self._is_running:
            if self.inbox.empty() and not self.new_packet.wait(self._packet_timeout):
                continue
            ip, port, packet = self.inbox.get()
            if self.inbox.empty():
                self.new_packet.clear()
            self.debug((b'{}').format(packet))
            if packet.header.message_type == MsgType.CONFIG:
                self._do_config_packet(packet, ip, port)

    def _do_config_packet(self, packet, ip, port):
        """
        Apply config to this instance

        :param packet: Packet with config
        :type packet: paps.si.app.message.APPMessage
        :param ip: Ip of server
        :type ip: str
        :param port: Port of server
        :type port: int
        :rtype: None
        """
        self.debug(b'()')
        if packet.header.device_id != Id.SERVER:
            self.warning(b'Config packets only allowed from server')
            return
        try:
            config = packet.payload
            self.debug((b'{}').format(config))
            if not isinstance(config, dict):
                self.error(b'Wrong payload type')
                raise RuntimeError(b'Wrong type')
            config.setdefault(b'server_ip', ip)
            config.setdefault(b'server_port', port)
            self.config(config)
            self._joined.set()
        except:
            self.exception(b'Failed to configure')
            self.error((b'Faulty packet {}').format(format_data(packet.payload)))
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
        super(SensorClient, self).start(blocking=False)
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

    def stop(self):
        """
        Stop the interface

        :rtype: None
        """
        self.debug(b'()')
        try:
            self.unjoin()
            time.sleep(2)
        except:
            self.exception(b'Failed to leave audience')

        super(SensorClient, self).stop()