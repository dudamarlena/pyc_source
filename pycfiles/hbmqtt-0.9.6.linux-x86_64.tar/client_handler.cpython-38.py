# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/lib/python3.8/site-packages/hbmqtt/mqtt/protocol/client_handler.py
# Compiled at: 2020-01-25 09:04:28
# Size of source mod 2**32: 6447 bytes
import asyncio
from asyncio import futures
import sys
from hbmqtt.mqtt.protocol.handler import ProtocolHandler, EVENT_MQTT_PACKET_RECEIVED
from hbmqtt.mqtt.disconnect import DisconnectPacket
from hbmqtt.mqtt.pingreq import PingReqPacket
from hbmqtt.mqtt.pingresp import PingRespPacket
from hbmqtt.mqtt.subscribe import SubscribePacket
from hbmqtt.mqtt.suback import SubackPacket
from hbmqtt.mqtt.unsubscribe import UnsubscribePacket
from hbmqtt.mqtt.unsuback import UnsubackPacket
from hbmqtt.mqtt.connect import ConnectVariableHeader, ConnectPayload, ConnectPacket
from hbmqtt.mqtt.connack import ConnackPacket
from hbmqtt.session import Session
from hbmqtt.plugins.manager import PluginManager

class ClientProtocolHandler(ProtocolHandler):

    def __init__(self, plugins_manager, session=None, loop=None):
        super().__init__(plugins_manager, session, loop=loop)
        self._ping_task = None
        self._pingresp_queue = asyncio.Queue(loop=(self._loop))
        self._subscriptions_waiter = dict()
        self._unsubscriptions_waiter = dict()
        self._disconnect_waiter = None

    @asyncio.coroutine
    def start(self):
        yield from super().start()
        if self._disconnect_waiter is None:
            self._disconnect_waiter = futures.Future(loop=(self._loop))
        if False:
            yield None

    @asyncio.coroutine
    def stop(self):
        yield from super().stop()
        if self._ping_task:
            try:
                self.logger.debug('Cancel ping task')
                self._ping_task.cancel()
            except BaseException:
                pass

        if not self._disconnect_waiter.done():
            self._disconnect_waiter.cancel()
        self._disconnect_waiter = None
        if False:
            yield None

    def _build_connect_packet(self):
        vh = ConnectVariableHeader()
        payload = ConnectPayload()
        vh.keep_alive = self.session.keep_alive
        vh.clean_session_flag = self.session.clean_session
        vh.will_retain_flag = self.session.will_retain
        payload.client_id = self.session.client_id
        if self.session.username:
            vh.username_flag = True
            payload.username = self.session.username
        else:
            vh.username_flag = False
        if self.session.password:
            vh.password_flag = True
            payload.password = self.session.password
        else:
            vh.password_flag = False
        if self.session.will_flag:
            vh.will_flag = True
            vh.will_qos = self.session.will_qos
            payload.will_message = self.session.will_message
            payload.will_topic = self.session.will_topic
        else:
            vh.will_flag = False
        packet = ConnectPacket(vh=vh, payload=payload)
        return packet

    @asyncio.coroutine
    def mqtt_connect(self):
        connect_packet = self._build_connect_packet()
        (yield from self._send_packet(connect_packet))
        connack = yield from ConnackPacket.from_stream(self.reader)
        (yield from self.plugins_manager.fire_event(EVENT_MQTT_PACKET_RECEIVED, packet=connack, session=(self.session)))
        return connack.return_code
        if False:
            yield None

    def handle_write_timeout(self):
        try:
            if not self._ping_task:
                self.logger.debug('Scheduling Ping')
                self._ping_task = asyncio.ensure_future(self.mqtt_ping())
        except BaseException as be:
            try:
                self.logger.debug('Exception ignored in ping task: %r' % be)
            finally:
                be = None
                del be

    def handle_read_timeout(self):
        pass

    @asyncio.coroutine
    def mqtt_subscribe(self, topics, packet_id):
        """
        :param topics: array of topics [{'filter':'/a/b', 'qos': 0x00}, ...]
        :return:
        """
        subscribe = SubscribePacket.build(topics, packet_id)
        (yield from self._send_packet(subscribe))
        waiter = futures.Future(loop=(self._loop))
        self._subscriptions_waiter[subscribe.variable_header.packet_id] = waiter
        return_codes = yield from waiter
        del self._subscriptions_waiter[subscribe.variable_header.packet_id]
        return return_codes
        if False:
            yield None

    @asyncio.coroutine
    def handle_suback(self, suback: SubackPacket):
        packet_id = suback.variable_header.packet_id
        try:
            waiter = self._subscriptions_waiter.get(packet_id)
            waiter.set_result(suback.payload.return_codes)
        except KeyError as ke:
            try:
                self.logger.warning('Received SUBACK for unknown pending subscription with Id: %s' % packet_id)
            finally:
                ke = None
                del ke

    @asyncio.coroutine
    def mqtt_unsubscribe(self, topics, packet_id):
        """

        :param topics: array of topics ['/a/b', ...]
        :return:
        """
        unsubscribe = UnsubscribePacket.build(topics, packet_id)
        (yield from self._send_packet(unsubscribe))
        waiter = futures.Future(loop=(self._loop))
        self._unsubscriptions_waiter[unsubscribe.variable_header.packet_id] = waiter
        (yield from waiter)
        del self._unsubscriptions_waiter[unsubscribe.variable_header.packet_id]
        if False:
            yield None

    @asyncio.coroutine
    def handle_unsuback(self, unsuback: UnsubackPacket):
        packet_id = unsuback.variable_header.packet_id
        try:
            waiter = self._unsubscriptions_waiter.get(packet_id)
            waiter.set_result(None)
        except KeyError as ke:
            try:
                self.logger.warning('Received UNSUBACK for unknown pending subscription with Id: %s' % packet_id)
            finally:
                ke = None
                del ke

    @asyncio.coroutine
    def mqtt_disconnect(self):
        disconnect_packet = DisconnectPacket()
        (yield from self._send_packet(disconnect_packet))
        if False:
            yield None

    @asyncio.coroutine
    def mqtt_ping(self):
        ping_packet = PingReqPacket()
        (yield from self._send_packet(ping_packet))
        resp = yield from self._pingresp_queue.get()
        if self._ping_task:
            self._ping_task = None
        return resp
        if False:
            yield None

    @asyncio.coroutine
    def handle_pingresp(self, pingresp: PingRespPacket):
        (yield from self._pingresp_queue.put(pingresp))
        if False:
            yield None

    @asyncio.coroutine
    def handle_connection_closed(self):
        self.logger.debug('Broker closed connection')
        if not self._disconnect_waiter.done():
            self._disconnect_waiter.set_result(None)

    @asyncio.coroutine
    def wait_disconnect(self):
        (yield from self._disconnect_waiter)
        if False:
            yield None