# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/lib/python3.8/site-packages/hbmqtt/mqtt/protocol/broker_handler.py
# Compiled at: 2020-01-25 09:04:28
# Size of source mod 2**32: 8820 bytes
import asyncio
from asyncio import futures, Queue
from hbmqtt.mqtt.protocol.handler import ProtocolHandler
from hbmqtt.mqtt.connack import CONNECTION_ACCEPTED, UNACCEPTABLE_PROTOCOL_VERSION, IDENTIFIER_REJECTED, BAD_USERNAME_PASSWORD, NOT_AUTHORIZED, ConnackPacket
from hbmqtt.mqtt.connect import ConnectPacket
from hbmqtt.mqtt.pingreq import PingReqPacket
from hbmqtt.mqtt.pingresp import PingRespPacket
from hbmqtt.mqtt.subscribe import SubscribePacket
from hbmqtt.mqtt.suback import SubackPacket
from hbmqtt.mqtt.unsubscribe import UnsubscribePacket
from hbmqtt.mqtt.unsuback import UnsubackPacket
from hbmqtt.utils import format_client_message
from hbmqtt.session import Session
from hbmqtt.plugins.manager import PluginManager
from hbmqtt.adapters import ReaderAdapter, WriterAdapter
from hbmqtt.errors import MQTTException
from .handler import EVENT_MQTT_PACKET_RECEIVED, EVENT_MQTT_PACKET_SENT

class BrokerProtocolHandler(ProtocolHandler):

    def __init__(self, plugins_manager, session=None, loop=None):
        super().__init__(plugins_manager, session, loop)
        self._disconnect_waiter = None
        self._pending_subscriptions = Queue(loop=(self._loop))
        self._pending_unsubscriptions = Queue(loop=(self._loop))

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
        if self._disconnect_waiter is not None:
            if not self._disconnect_waiter.done():
                self._disconnect_waiter.set_result(None)
        if False:
            yield None

    @asyncio.coroutine
    def wait_disconnect(self):
        return (yield from self._disconnect_waiter)
        if False:
            yield None

    def handle_write_timeout(self):
        pass

    def handle_read_timeout(self):
        if self._disconnect_waiter is not None:
            if not self._disconnect_waiter.done():
                self._disconnect_waiter.set_result(None)

    @asyncio.coroutine
    def handle_disconnect(self, disconnect):
        self.logger.debug('Client disconnecting')
        if self._disconnect_waiter:
            if not self._disconnect_waiter.done():
                self.logger.debug('Setting waiter result to %r' % disconnect)
                self._disconnect_waiter.set_result(disconnect)

    @asyncio.coroutine
    def handle_connection_closed(self):
        (yield from self.handle_disconnect(None))
        if False:
            yield None

    @asyncio.coroutine
    def handle_connect(self, connect: ConnectPacket):
        self.logger.error('%s [MQTT-3.1.0-2] %s : CONNECT message received during messages handling' % (
         self.session.client_id, format_client_message(self.session)))
        if self._disconnect_waiter is not None:
            if not self._disconnect_waiter.done():
                self._disconnect_waiter.set_result(None)

    @asyncio.coroutine
    def handle_pingreq(self, pingreq: PingReqPacket):
        (yield from self._send_packet(PingRespPacket.build()))
        if False:
            yield None

    @asyncio.coroutine
    def handle_subscribe(self, subscribe: SubscribePacket):
        subscription = {'packet_id':subscribe.variable_header.packet_id,  'topics':subscribe.payload.topics}
        (yield from self._pending_subscriptions.put(subscription))
        if False:
            yield None

    @asyncio.coroutine
    def handle_unsubscribe(self, unsubscribe: UnsubscribePacket):
        unsubscription = {'packet_id':unsubscribe.variable_header.packet_id,  'topics':unsubscribe.payload.topics}
        (yield from self._pending_unsubscriptions.put(unsubscription))
        if False:
            yield None

    @asyncio.coroutine
    def get_next_pending_subscription(self):
        subscription = yield from self._pending_subscriptions.get()
        return subscription
        if False:
            yield None

    @asyncio.coroutine
    def get_next_pending_unsubscription(self):
        unsubscription = yield from self._pending_unsubscriptions.get()
        return unsubscription
        if False:
            yield None

    @asyncio.coroutine
    def mqtt_acknowledge_subscription(self, packet_id, return_codes):
        suback = SubackPacket.build(packet_id, return_codes)
        (yield from self._send_packet(suback))
        if False:
            yield None

    @asyncio.coroutine
    def mqtt_acknowledge_unsubscription(self, packet_id):
        unsuback = UnsubackPacket.build(packet_id)
        (yield from self._send_packet(unsuback))
        if False:
            yield None

    @asyncio.coroutine
    def mqtt_connack_authorize(self, authorize: bool):
        if authorize:
            connack = ConnackPacket.build(self.session.parent, CONNECTION_ACCEPTED)
        else:
            connack = ConnackPacket.build(self.session.parent, NOT_AUTHORIZED)
        (yield from self._send_packet(connack))
        if False:
            yield None

    @classmethod
    @asyncio.coroutine
    def init_from_connect(cls, reader: ReaderAdapter, writer: WriterAdapter, plugins_manager, loop=None):
        """

        :param reader:
        :param writer:
        :param plugins_manager:
        :param loop:
        :return:
        """
        remote_address, remote_port = writer.get_peer_info()
        connect = yield from ConnectPacket.from_stream(reader)
        (yield from plugins_manager.fire_event(EVENT_MQTT_PACKET_RECEIVED, packet=connect))
        if connect.payload.client_id is None:
            raise MQTTException('[[MQTT-3.1.3-3]] : Client identifier must be present')
        if connect.variable_header.will_flag:
            if connect.payload.will_topic is None or connect.payload.will_message is None:
                raise MQTTException('will flag set, but will topic/message not present in payload')
        if connect.variable_header.reserved_flag:
            raise MQTTException('[MQTT-3.1.2-3] CONNECT reserved flag must be set to 0')
        if connect.proto_name != 'MQTT':
            raise MQTTException('[MQTT-3.1.2-1] Incorrect protocol name: "%s"' % connect.proto_name)
        connack = None
        error_msg = None
        if connect.proto_level != 4:
            error_msg = 'Invalid protocol from %s: %d' % (
             format_client_message(address=remote_address, port=remote_port), connect.proto_level)
            connack = ConnackPacket.build(0, UNACCEPTABLE_PROTOCOL_VERSION)
        else:
            if (connect.username_flag or connect).password_flag:
                connack = ConnackPacket.build(0, BAD_USERNAME_PASSWORD)
            else:
                if connect.username_flag:
                    connack = connect.password_flag or ConnackPacket.build(0, BAD_USERNAME_PASSWORD)
                else:
                    if connect.username_flag and connect.username is None:
                        error_msg = 'Invalid username from %s' % format_client_message(address=remote_address, port=remote_port)
                        connack = ConnackPacket.build(0, BAD_USERNAME_PASSWORD)
                    else:
                        if connect.password_flag and connect.password is None:
                            error_msg = 'Invalid password %s' % format_client_message(address=remote_address, port=remote_port)
                            connack = ConnackPacket.build(0, BAD_USERNAME_PASSWORD)
                        else:
                            if connect.clean_session_flag is False:
                                if connect.payload.client_id_is_random:
                                    error_msg = '[MQTT-3.1.3-8] [MQTT-3.1.3-9] %s: No client Id provided (cleansession=0)' % format_client_message(address=remote_address, port=remote_port)
                                    connack = ConnackPacket.build(0, IDENTIFIER_REJECTED)
                            else:
                                if connack is not None:
                                    (yield from plugins_manager.fire_event(EVENT_MQTT_PACKET_SENT, packet=connack))
                                    (yield from connack.to_stream(writer))
                                    (yield from writer.close())
                                    raise MQTTException(error_msg)
                                incoming_session = Session(loop)
                                incoming_session.client_id = connect.client_id
                                incoming_session.clean_session = connect.clean_session_flag
                                incoming_session.will_flag = connect.will_flag
                                incoming_session.will_retain = connect.will_retain_flag
                                incoming_session.will_qos = connect.will_qos
                                incoming_session.will_topic = connect.will_topic
                                incoming_session.will_message = connect.will_message
                                incoming_session.username = connect.username
                                incoming_session.password = connect.password
                                if connect.keep_alive > 0:
                                    incoming_session.keep_alive = connect.keep_alive
                                else:
                                    incoming_session.keep_alive = 0
                            handler = cls(plugins_manager, loop=loop)
                            return (handler, incoming_session)
        if False:
            yield None