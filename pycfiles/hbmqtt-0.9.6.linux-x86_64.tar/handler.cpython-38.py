# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/lib/python3.8/site-packages/hbmqtt/mqtt/protocol/handler.py
# Compiled at: 2020-01-25 09:04:28
# Size of source mod 2**32: 27045 bytes
import logging, collections, itertools, asyncio
from asyncio import InvalidStateError
from hbmqtt.mqtt import packet_class
from hbmqtt.mqtt.connack import ConnackPacket
from hbmqtt.mqtt.connect import ConnectPacket
from hbmqtt.mqtt.packet import RESERVED_0, CONNECT, CONNACK, PUBLISH, PUBACK, PUBREC, PUBREL, PUBCOMP, SUBSCRIBE, SUBACK, UNSUBSCRIBE, UNSUBACK, PINGREQ, PINGRESP, DISCONNECT, RESERVED_15, MQTTFixedHeader
from hbmqtt.mqtt.pingresp import PingRespPacket
from hbmqtt.mqtt.pingreq import PingReqPacket
from hbmqtt.mqtt.publish import PublishPacket
from hbmqtt.mqtt.pubrel import PubrelPacket
from hbmqtt.mqtt.puback import PubackPacket
from hbmqtt.mqtt.pubrec import PubrecPacket
from hbmqtt.mqtt.pubcomp import PubcompPacket
from hbmqtt.mqtt.suback import SubackPacket
from hbmqtt.mqtt.subscribe import SubscribePacket
from hbmqtt.mqtt.unsubscribe import UnsubscribePacket
from hbmqtt.mqtt.unsuback import UnsubackPacket
from hbmqtt.mqtt.disconnect import DisconnectPacket
from hbmqtt.adapters import ReaderAdapter, WriterAdapter
from hbmqtt.session import Session, OutgoingApplicationMessage, IncomingApplicationMessage, INCOMING, OUTGOING
from hbmqtt.mqtt.constants import QOS_0, QOS_1, QOS_2
from hbmqtt.plugins.manager import PluginManager
from hbmqtt.errors import HBMQTTException, MQTTException, NoDataException
EVENT_MQTT_PACKET_SENT = 'mqtt_packet_sent'
EVENT_MQTT_PACKET_RECEIVED = 'mqtt_packet_received'

class ProtocolHandlerException(BaseException):
    pass


class ProtocolHandler:
    __doc__ = '\n    Class implementing the MQTT communication protocol using asyncio features\n    '

    def __init__(self, plugins_manager: PluginManager, session: Session=None, loop=None):
        self.logger = logging.getLogger(__name__)
        if session:
            self._init_session(session)
        else:
            self.session = None
        self.reader = None
        self.writer = None
        self.plugins_manager = plugins_manager
        if loop is None:
            self._loop = asyncio.get_event_loop()
        else:
            self._loop = loop
        self._reader_task = None
        self._keepalive_task = None
        self._reader_ready = None
        self._reader_stopped = asyncio.Event(loop=(self._loop))
        self._puback_waiters = dict()
        self._pubrec_waiters = dict()
        self._pubrel_waiters = dict()
        self._pubcomp_waiters = dict()
        self._write_lock = asyncio.Lock(loop=(self._loop))

    def _init_session(self, session: Session):
        assert session
        log = logging.getLogger(__name__)
        self.session = session
        self.logger = logging.LoggerAdapter(log, {'client_id': self.session.client_id})
        self.keepalive_timeout = self.session.keep_alive
        if self.keepalive_timeout <= 0:
            self.keepalive_timeout = None

    def attach(self, session, reader: ReaderAdapter, writer: WriterAdapter):
        if self.session:
            raise ProtocolHandlerException('Handler is already attached to a session')
        self._init_session(session)
        self.reader = reader
        self.writer = writer

    def detach(self):
        self.session = None
        self.reader = None
        self.writer = None

    def _is_attached(self):
        if self.session:
            return True
        return False

    @asyncio.coroutine
    def start(self):
        if not self._is_attached():
            raise ProtocolHandlerException('Handler is not attached to a stream')
        self._reader_ready = asyncio.Event(loop=(self._loop))
        self._reader_task = asyncio.Task((self._reader_loop()), loop=(self._loop))
        (yield from asyncio.wait([self._reader_ready.wait()], loop=(self._loop)))
        if self.keepalive_timeout:
            self._keepalive_task = self._loop.call_later(self.keepalive_timeout, self.handle_write_timeout)
        self.logger.debug('Handler tasks started')
        (yield from self._retry_deliveries())
        self.logger.debug('Handler ready')
        if False:
            yield None

    @asyncio.coroutine
    def stop(self):
        self._stop_waiters()
        if self._keepalive_task:
            self._keepalive_task.cancel()
        self.logger.debug('waiting for tasks to be stopped')
        if not self._reader_task.done():
            self._reader_task.cancel()
            (yield from asyncio.wait([
             self._reader_stopped.wait()],
              loop=(self._loop)))
        self.logger.debug('closing writer')
        try:
            (yield from self.writer.close())
        except Exception as e:
            try:
                self.logger.debug('Handler writer close failed: %s' % e)
            finally:
                e = None
                del e

        if False:
            yield None

    def _stop_waiters(self):
        self.logger.debug('Stopping %d puback waiters' % len(self._puback_waiters))
        self.logger.debug('Stopping %d pucomp waiters' % len(self._pubcomp_waiters))
        self.logger.debug('Stopping %d purec waiters' % len(self._pubrec_waiters))
        self.logger.debug('Stopping %d purel waiters' % len(self._pubrel_waiters))
        for waiter in itertools.chain(self._puback_waiters.values(), self._pubcomp_waiters.values(), self._pubrec_waiters.values(), self._pubrel_waiters.values()):
            waiter.cancel()

    @asyncio.coroutine
    def _retry_deliveries(self):
        """
        Handle [MQTT-4.4.0-1] by resending PUBLISH and PUBREL messages for pending out messages
        :return:
        """
        self.logger.debug('Begin messages delivery retries')
        tasks = []
        for message in itertools.chain(self.session.inflight_in.values(), self.session.inflight_out.values()):
            tasks.append(asyncio.wait_for((self._handle_message_flow(message)), 10, loop=(self._loop)))
        else:
            if tasks:
                done, pending = yield from asyncio.wait(tasks, loop=(self._loop))
                self.logger.debug('%d messages redelivered' % len(done))
                self.logger.debug('%d messages not redelivered due to timeout' % len(pending))
            self.logger.debug('End messages delivery retries')

        if False:
            yield None

    @asyncio.coroutine
    def mqtt_publish(self, topic, data, qos, retain, ack_timeout=None):
        """
        Sends a MQTT publish message and manages messages flows.
        This methods doesn't return until the message has been acknowledged by receiver or timeout occur
        :param topic: MQTT topic to publish
        :param data:  data to send on topic
        :param qos: quality of service to use for message flow. Can be QOS_0, QOS_1 or QOS_2
        :param retain: retain message flag
        :param ack_timeout: acknowledge timeout. If set, this method will return a TimeOut error if the acknowledgment
        is not completed before ack_timeout second
        :return: ApplicationMessage used during inflight operations
        """
        if qos in (QOS_1, QOS_2):
            packet_id = self.session.next_packet_id
            if packet_id in self.session.inflight_out:
                raise HBMQTTException("A message with the same packet ID '%d' is already in flight" % packet_id)
        else:
            packet_id = None
        message = OutgoingApplicationMessage(packet_id, topic, qos, data, retain)
        if ack_timeout is not None and ack_timeout > 0:
            (yield from asyncio.wait_for((self._handle_message_flow(message)), ack_timeout, loop=(self._loop)))
        else:
            (yield from self._handle_message_flow(message))
        return message
        if False:
            yield None

    @asyncio.coroutine
    def _handle_message_flow(self, app_message):
        """
        Handle protocol flow for incoming and outgoing messages, depending on service level and according to MQTT
        spec. paragraph 4.3-Quality of Service levels and protocol flows
        :param app_message: PublishMessage to handle
        :return: nothing.
        """
        if app_message.qos == QOS_0:
            (yield from self._handle_qos0_message_flow(app_message))
        else:
            if app_message.qos == QOS_1:
                (yield from self._handle_qos1_message_flow(app_message))
            else:
                if app_message.qos == QOS_2:
                    (yield from self._handle_qos2_message_flow(app_message))
                else:
                    raise HBMQTTException("Unexcepted QOS value '%d" % str(app_message.qos))
        if False:
            yield None

    @asyncio.coroutine
    def _handle_qos0_message_flow(self, app_message):
        """
        Handle QOS_0 application message acknowledgment
        For incoming messages, this method stores the message
        For outgoing messages, this methods sends PUBLISH
        :param app_message:
        :return:
        """
        if not app_message.qos == QOS_0:
            raise AssertionError
        elif app_message.direction == OUTGOING:
            packet = app_message.build_publish_packet()
            (yield from self._send_packet(packet))
            app_message.publish_packet = packet
        else:
            if app_message.direction == INCOMING:
                if app_message.publish_packet.dup_flag:
                    self.logger.warning('[MQTT-3.3.1-2] DUP flag must set to 0 for QOS 0 message. Message ignored: %s' % repr(app_message.publish_packet))
                else:
                    try:
                        self.session.delivered_message_queue.put_nowait(app_message)
                    except:
                        self.logger.warning('delivered messages queue full. QOS_0 message discarded')

        if False:
            yield None

    @asyncio.coroutine
    def _handle_qos1_message_flow(self, app_message):
        """
        Handle QOS_1 application message acknowledgment
        For incoming messages, this method stores the message and reply with PUBACK
        For outgoing messages, this methods sends PUBLISH and waits for the corresponding PUBACK
        :param app_message:
        :return:
        """
        if not app_message.qos == QOS_1:
            raise AssertionError
        else:
            if app_message.puback_packet:
                raise HBMQTTException("Message '%d' has already been acknowledged" % app_message.packet_id)
            if app_message.direction == OUTGOING:
                if app_message.packet_id not in self.session.inflight_out:
                    self.session.inflight_out[app_message.packet_id] = app_message
                elif app_message.publish_packet is not None:
                    publish_packet = app_message.build_publish_packet(dup=True)
                else:
                    publish_packet = app_message.build_publish_packet()
                (yield from self._send_packet(publish_packet))
                app_message.publish_packet = publish_packet
                waiter = asyncio.Future(loop=(self._loop))
                self._puback_waiters[app_message.packet_id] = waiter
                (yield from waiter)
                del self._puback_waiters[app_message.packet_id]
                app_message.puback_packet = waiter.result()
                del self.session.inflight_out[app_message.packet_id]
            else:
                if app_message.direction == INCOMING:
                    self.logger.debug('Add message to delivery')
                    (yield from self.session.delivered_message_queue.put(app_message))
                    puback = PubackPacket.build(app_message.packet_id)
                    (yield from self._send_packet(puback))
                    app_message.puback_packet = puback
        if False:
            yield None

    @asyncio.coroutine
    def _handle_qos2_message_flow(self, app_message):
        """
        Handle QOS_2 application message acknowledgment
        For incoming messages, this method stores the message, sends PUBREC, waits for PUBREL, initiate delivery
        and send PUBCOMP
        For outgoing messages, this methods sends PUBLISH, waits for PUBREC, discards messages and wait for PUBCOMP
        :param app_message:
        :return:
        """
        if not app_message.qos == QOS_2:
            raise AssertionError
        else:
            if app_message.direction == OUTGOING:
                if app_message.pubrel_packet:
                    if app_message.pubcomp_packet:
                        raise HBMQTTException("Message '%d' has already been acknowledged" % app_message.packet_id)
                    else:
                        if (app_message.pubrel_packet or app_message.publish_packet) is not None:
                            if app_message.packet_id not in self.session.inflight_out:
                                raise HBMQTTException("Unknown inflight message '%d' in session" % app_message.packet_id)
                            publish_packet = app_message.build_publish_packet(dup=True)
                        else:
                            self.session.inflight_out[app_message.packet_id] = app_message
                            publish_packet = app_message.build_publish_packet()
                        (yield from self._send_packet(publish_packet))
                        app_message.publish_packet = publish_packet
                        if app_message.packet_id in self._pubrec_waiters:
                            message = "Can't add PUBREC waiter, a waiter already exists for message Id '%s'" % app_message.packet_id
                            self.logger.warning(message)
                            raise HBMQTTException(message)
                        waiter = asyncio.Future(loop=(self._loop))
                        self._pubrec_waiters[app_message.packet_id] = waiter
                        (yield from waiter)
                        del self._pubrec_waiters[app_message.packet_id]
                        app_message.pubrec_packet = waiter.result()
                    if not app_message.pubcomp_packet:
                        app_message.pubrel_packet = PubrelPacket.build(app_message.packet_id)
                        (yield from self._send_packet(app_message.pubrel_packet))
                        waiter = asyncio.Future(loop=(self._loop))
                        self._pubcomp_waiters[app_message.packet_id] = waiter
                        (yield from waiter)
                        del self._pubcomp_waiters[app_message.packet_id]
                        app_message.pubcomp_packet = waiter.result()
                    del self.session.inflight_out[app_message.packet_id]
                else:
                    pass
            if app_message.direction == INCOMING:
                self.session.inflight_in[app_message.packet_id] = app_message
                pubrec_packet = PubrecPacket.build(app_message.packet_id)
                (yield from self._send_packet(pubrec_packet))
                app_message.pubrec_packet = pubrec_packet
                if app_message.packet_id in self._pubrel_waiters:
                    if not self._pubrel_waiters[app_message.packet_id].done():
                        message = "A waiter already exists for message Id '%s', canceling it" % app_message.packet_id
                        self.logger.warning(message)
                        self._pubrel_waiters[app_message.packet_id].cancel()
                try:
                    waiter = asyncio.Future(loop=(self._loop))
                    self._pubrel_waiters[app_message.packet_id] = waiter
                    (yield from waiter)
                    del self._pubrel_waiters[app_message.packet_id]
                    app_message.pubrel_packet = waiter.result()
                    (yield from self.session.delivered_message_queue.put(app_message))
                    del self.session.inflight_in[app_message.packet_id]
                    pubcomp_packet = PubcompPacket.build(app_message.packet_id)
                    (yield from self._send_packet(pubcomp_packet))
                    app_message.pubcomp_packet = pubcomp_packet
                except asyncio.CancelledError:
                    self.logger.debug('Message flow cancelled')

        if False:
            yield None

    @asyncio.coroutine
    def _reader_loop--- This code section failed: ---

 L. 359         0  LOAD_FAST                'self'
                2  LOAD_ATTR                logger
                4  LOAD_METHOD              debug
                6  LOAD_STR                 '%s Starting reader coro'
                8  LOAD_FAST                'self'
               10  LOAD_ATTR                session
               12  LOAD_ATTR                client_id
               14  BINARY_MODULO    
               16  CALL_METHOD_1         1  ''
               18  POP_TOP          

 L. 360        20  LOAD_GLOBAL              collections
               22  LOAD_METHOD              deque
               24  CALL_METHOD_0         0  ''
               26  STORE_FAST               'running_tasks'

 L. 361        28  LOAD_FAST                'self'
               30  LOAD_ATTR                session
               32  LOAD_ATTR                keep_alive
               34  STORE_FAST               'keepalive_timeout'

 L. 362        36  LOAD_FAST                'keepalive_timeout'
               38  LOAD_CONST               0
               40  COMPARE_OP               <=
               42  POP_JUMP_IF_FALSE    48  'to 48'

 L. 363        44  LOAD_CONST               None
               46  STORE_FAST               'keepalive_timeout'
             48_0  COME_FROM            42  '42'

 L. 365     48_50  SETUP_FINALLY       886  'to 886'

 L. 366        52  LOAD_FAST                'self'
               54  LOAD_ATTR                _reader_ready
               56  LOAD_METHOD              set
               58  CALL_METHOD_0         0  ''
               60  POP_TOP          

 L. 367        62  LOAD_FAST                'running_tasks'
               64  POP_JUMP_IF_FALSE    88  'to 88'
               66  LOAD_FAST                'running_tasks'
               68  LOAD_CONST               0
               70  BINARY_SUBSCR    
               72  LOAD_METHOD              done
               74  CALL_METHOD_0         0  ''
               76  POP_JUMP_IF_FALSE    88  'to 88'

 L. 368        78  LOAD_FAST                'running_tasks'
               80  LOAD_METHOD              popleft
               82  CALL_METHOD_0         0  ''
               84  POP_TOP          
               86  JUMP_BACK            62  'to 62'
             88_0  COME_FROM            76  '76'
             88_1  COME_FROM            64  '64'

 L. 369        88  LOAD_GLOBAL              len
               90  LOAD_FAST                'running_tasks'
               92  CALL_FUNCTION_1       1  ''
               94  LOAD_CONST               1
               96  COMPARE_OP               >
               98  POP_JUMP_IF_FALSE   120  'to 120'

 L. 370       100  LOAD_FAST                'self'
              102  LOAD_ATTR                logger
              104  LOAD_METHOD              debug
              106  LOAD_STR                 'handler running tasks: %d'
              108  LOAD_GLOBAL              len
              110  LOAD_FAST                'running_tasks'
              112  CALL_FUNCTION_1       1  ''
              114  BINARY_MODULO    
              116  CALL_METHOD_1         1  ''
              118  POP_TOP          
            120_0  COME_FROM            98  '98'

 L. 372       120  LOAD_GLOBAL              asyncio
              122  LOAD_ATTR                wait_for

 L. 373       124  LOAD_GLOBAL              MQTTFixedHeader
              126  LOAD_METHOD              from_stream
              128  LOAD_FAST                'self'
              130  LOAD_ATTR                reader
              132  CALL_METHOD_1         1  ''

 L. 374       134  LOAD_FAST                'keepalive_timeout'

 L. 374       136  LOAD_FAST                'self'
              138  LOAD_ATTR                _loop

 L. 372       140  LOAD_CONST               ('loop',)
              142  CALL_FUNCTION_KW_3     3  '3 total positional and keyword args'
              144  GET_YIELD_FROM_ITER
              146  LOAD_CONST               None
              148  YIELD_FROM       
              150  STORE_FAST               'fixed_header'

 L. 375       152  LOAD_FAST                'fixed_header'
          154_156  POP_JUMP_IF_FALSE   856  'to 856'

 L. 376       158  LOAD_FAST                'fixed_header'
              160  LOAD_ATTR                packet_type
              162  LOAD_GLOBAL              RESERVED_0
              164  COMPARE_OP               ==
              166  POP_JUMP_IF_TRUE    178  'to 178'
              168  LOAD_FAST                'fixed_header'
              170  LOAD_ATTR                packet_type
              172  LOAD_GLOBAL              RESERVED_15
              174  COMPARE_OP               ==
              176  POP_JUMP_IF_FALSE   216  'to 216'
            178_0  COME_FROM           166  '166'

 L. 377       178  LOAD_FAST                'self'
              180  LOAD_ATTR                logger
              182  LOAD_METHOD              warning
              184  LOAD_STR                 '%s Received reserved packet, which is forbidden: closing connection'

 L. 378       186  LOAD_FAST                'self'
              188  LOAD_ATTR                session
              190  LOAD_ATTR                client_id

 L. 377       192  BINARY_MODULO    
              194  CALL_METHOD_1         1  ''
              196  POP_TOP          

 L. 379       198  LOAD_FAST                'self'
              200  LOAD_METHOD              handle_connection_closed
              202  CALL_METHOD_0         0  ''
              204  GET_YIELD_FROM_ITER
              206  LOAD_CONST               None
              208  YIELD_FROM       
              210  POP_TOP          
          212_214  JUMP_ABSOLUTE       882  'to 882'
            216_0  COME_FROM           176  '176'

 L. 381       216  LOAD_GLOBAL              packet_class
              218  LOAD_FAST                'fixed_header'
              220  CALL_FUNCTION_1       1  ''
              222  STORE_FAST               'cls'

 L. 382       224  LOAD_FAST                'cls'
              226  LOAD_ATTR                from_stream
              228  LOAD_FAST                'self'
              230  LOAD_ATTR                reader
              232  LOAD_FAST                'fixed_header'
              234  LOAD_CONST               ('fixed_header',)
              236  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              238  GET_YIELD_FROM_ITER
              240  LOAD_CONST               None
              242  YIELD_FROM       
              244  STORE_FAST               'packet'

 L. 383       246  LOAD_FAST                'self'
              248  LOAD_ATTR                plugins_manager
              250  LOAD_ATTR                fire_event

 L. 384       252  LOAD_GLOBAL              EVENT_MQTT_PACKET_RECEIVED

 L. 384       254  LOAD_FAST                'packet'

 L. 384       256  LOAD_FAST                'self'
              258  LOAD_ATTR                session

 L. 383       260  LOAD_CONST               ('packet', 'session')
              262  CALL_FUNCTION_KW_3     3  '3 total positional and keyword args'
              264  GET_YIELD_FROM_ITER
              266  LOAD_CONST               None
              268  YIELD_FROM       
              270  POP_TOP          

 L. 385       272  LOAD_CONST               None
              274  STORE_FAST               'task'

 L. 386       276  LOAD_FAST                'packet'
              278  LOAD_ATTR                fixed_header
              280  LOAD_ATTR                packet_type
              282  LOAD_GLOBAL              CONNACK
              284  COMPARE_OP               ==
          286_288  POP_JUMP_IF_FALSE   316  'to 316'

 L. 387       290  LOAD_GLOBAL              asyncio
              292  LOAD_ATTR                ensure_future
              294  LOAD_FAST                'self'
              296  LOAD_METHOD              handle_connack
              298  LOAD_FAST                'packet'
              300  CALL_METHOD_1         1  ''
              302  LOAD_FAST                'self'
              304  LOAD_ATTR                _loop
              306  LOAD_CONST               ('loop',)
              308  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              310  STORE_FAST               'task'
          312_314  JUMP_FORWARD        838  'to 838'
            316_0  COME_FROM           286  '286'

 L. 388       316  LOAD_FAST                'packet'
              318  LOAD_ATTR                fixed_header
              320  LOAD_ATTR                packet_type
              322  LOAD_GLOBAL              SUBSCRIBE
              324  COMPARE_OP               ==
          326_328  POP_JUMP_IF_FALSE   356  'to 356'

 L. 389       330  LOAD_GLOBAL              asyncio
              332  LOAD_ATTR                ensure_future
              334  LOAD_FAST                'self'
              336  LOAD_METHOD              handle_subscribe
              338  LOAD_FAST                'packet'
              340  CALL_METHOD_1         1  ''
              342  LOAD_FAST                'self'
              344  LOAD_ATTR                _loop
              346  LOAD_CONST               ('loop',)
              348  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              350  STORE_FAST               'task'
          352_354  JUMP_FORWARD        838  'to 838'
            356_0  COME_FROM           326  '326'

 L. 390       356  LOAD_FAST                'packet'
              358  LOAD_ATTR                fixed_header
              360  LOAD_ATTR                packet_type
              362  LOAD_GLOBAL              UNSUBSCRIBE
              364  COMPARE_OP               ==
          366_368  POP_JUMP_IF_FALSE   396  'to 396'

 L. 391       370  LOAD_GLOBAL              asyncio
              372  LOAD_ATTR                ensure_future
              374  LOAD_FAST                'self'
              376  LOAD_METHOD              handle_unsubscribe
              378  LOAD_FAST                'packet'
              380  CALL_METHOD_1         1  ''
              382  LOAD_FAST                'self'
              384  LOAD_ATTR                _loop
              386  LOAD_CONST               ('loop',)
              388  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              390  STORE_FAST               'task'
          392_394  JUMP_FORWARD        838  'to 838'
            396_0  COME_FROM           366  '366'

 L. 392       396  LOAD_FAST                'packet'
              398  LOAD_ATTR                fixed_header
              400  LOAD_ATTR                packet_type
              402  LOAD_GLOBAL              SUBACK
              404  COMPARE_OP               ==
          406_408  POP_JUMP_IF_FALSE   436  'to 436'

 L. 393       410  LOAD_GLOBAL              asyncio
              412  LOAD_ATTR                ensure_future
              414  LOAD_FAST                'self'
              416  LOAD_METHOD              handle_suback
              418  LOAD_FAST                'packet'
              420  CALL_METHOD_1         1  ''
              422  LOAD_FAST                'self'
              424  LOAD_ATTR                _loop
              426  LOAD_CONST               ('loop',)
              428  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              430  STORE_FAST               'task'
          432_434  JUMP_FORWARD        838  'to 838'
            436_0  COME_FROM           406  '406'

 L. 394       436  LOAD_FAST                'packet'
              438  LOAD_ATTR                fixed_header
              440  LOAD_ATTR                packet_type
              442  LOAD_GLOBAL              UNSUBACK
              444  COMPARE_OP               ==
          446_448  POP_JUMP_IF_FALSE   476  'to 476'

 L. 395       450  LOAD_GLOBAL              asyncio
              452  LOAD_ATTR                ensure_future
              454  LOAD_FAST                'self'
              456  LOAD_METHOD              handle_unsuback
              458  LOAD_FAST                'packet'
              460  CALL_METHOD_1         1  ''
              462  LOAD_FAST                'self'
              464  LOAD_ATTR                _loop
              466  LOAD_CONST               ('loop',)
              468  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              470  STORE_FAST               'task'
          472_474  JUMP_FORWARD        838  'to 838'
            476_0  COME_FROM           446  '446'

 L. 396       476  LOAD_FAST                'packet'
              478  LOAD_ATTR                fixed_header
              480  LOAD_ATTR                packet_type
              482  LOAD_GLOBAL              PUBACK
              484  COMPARE_OP               ==
          486_488  POP_JUMP_IF_FALSE   516  'to 516'

 L. 397       490  LOAD_GLOBAL              asyncio
              492  LOAD_ATTR                ensure_future
              494  LOAD_FAST                'self'
              496  LOAD_METHOD              handle_puback
              498  LOAD_FAST                'packet'
              500  CALL_METHOD_1         1  ''
              502  LOAD_FAST                'self'
              504  LOAD_ATTR                _loop
              506  LOAD_CONST               ('loop',)
              508  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              510  STORE_FAST               'task'
          512_514  JUMP_FORWARD        838  'to 838'
            516_0  COME_FROM           486  '486'

 L. 398       516  LOAD_FAST                'packet'
              518  LOAD_ATTR                fixed_header
              520  LOAD_ATTR                packet_type
              522  LOAD_GLOBAL              PUBREC
              524  COMPARE_OP               ==
          526_528  POP_JUMP_IF_FALSE   556  'to 556'

 L. 399       530  LOAD_GLOBAL              asyncio
              532  LOAD_ATTR                ensure_future
              534  LOAD_FAST                'self'
              536  LOAD_METHOD              handle_pubrec
              538  LOAD_FAST                'packet'
              540  CALL_METHOD_1         1  ''
              542  LOAD_FAST                'self'
              544  LOAD_ATTR                _loop
              546  LOAD_CONST               ('loop',)
              548  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              550  STORE_FAST               'task'
          552_554  JUMP_FORWARD        838  'to 838'
            556_0  COME_FROM           526  '526'

 L. 400       556  LOAD_FAST                'packet'
              558  LOAD_ATTR                fixed_header
              560  LOAD_ATTR                packet_type
              562  LOAD_GLOBAL              PUBREL
              564  COMPARE_OP               ==
          566_568  POP_JUMP_IF_FALSE   594  'to 594'

 L. 401       570  LOAD_GLOBAL              asyncio
              572  LOAD_ATTR                ensure_future
              574  LOAD_FAST                'self'
              576  LOAD_METHOD              handle_pubrel
              578  LOAD_FAST                'packet'
              580  CALL_METHOD_1         1  ''
              582  LOAD_FAST                'self'
              584  LOAD_ATTR                _loop
              586  LOAD_CONST               ('loop',)
              588  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              590  STORE_FAST               'task'
              592  JUMP_FORWARD        838  'to 838'
            594_0  COME_FROM           566  '566'

 L. 402       594  LOAD_FAST                'packet'
              596  LOAD_ATTR                fixed_header
              598  LOAD_ATTR                packet_type
              600  LOAD_GLOBAL              PUBCOMP
              602  COMPARE_OP               ==
          604_606  POP_JUMP_IF_FALSE   632  'to 632'

 L. 403       608  LOAD_GLOBAL              asyncio
              610  LOAD_ATTR                ensure_future
              612  LOAD_FAST                'self'
              614  LOAD_METHOD              handle_pubcomp
              616  LOAD_FAST                'packet'
              618  CALL_METHOD_1         1  ''
              620  LOAD_FAST                'self'
              622  LOAD_ATTR                _loop
              624  LOAD_CONST               ('loop',)
              626  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              628  STORE_FAST               'task'
              630  JUMP_FORWARD        838  'to 838'
            632_0  COME_FROM           604  '604'

 L. 404       632  LOAD_FAST                'packet'
              634  LOAD_ATTR                fixed_header
              636  LOAD_ATTR                packet_type
              638  LOAD_GLOBAL              PINGREQ
              640  COMPARE_OP               ==
          642_644  POP_JUMP_IF_FALSE   670  'to 670'

 L. 405       646  LOAD_GLOBAL              asyncio
              648  LOAD_ATTR                ensure_future
              650  LOAD_FAST                'self'
              652  LOAD_METHOD              handle_pingreq
              654  LOAD_FAST                'packet'
              656  CALL_METHOD_1         1  ''
              658  LOAD_FAST                'self'
              660  LOAD_ATTR                _loop
              662  LOAD_CONST               ('loop',)
              664  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              666  STORE_FAST               'task'
              668  JUMP_FORWARD        838  'to 838'
            670_0  COME_FROM           642  '642'

 L. 406       670  LOAD_FAST                'packet'
              672  LOAD_ATTR                fixed_header
              674  LOAD_ATTR                packet_type
              676  LOAD_GLOBAL              PINGRESP
              678  COMPARE_OP               ==
          680_682  POP_JUMP_IF_FALSE   708  'to 708'

 L. 407       684  LOAD_GLOBAL              asyncio
              686  LOAD_ATTR                ensure_future
              688  LOAD_FAST                'self'
              690  LOAD_METHOD              handle_pingresp
              692  LOAD_FAST                'packet'
              694  CALL_METHOD_1         1  ''
              696  LOAD_FAST                'self'
              698  LOAD_ATTR                _loop
              700  LOAD_CONST               ('loop',)
              702  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              704  STORE_FAST               'task'
              706  JUMP_FORWARD        838  'to 838'
            708_0  COME_FROM           680  '680'

 L. 408       708  LOAD_FAST                'packet'
              710  LOAD_ATTR                fixed_header
              712  LOAD_ATTR                packet_type
              714  LOAD_GLOBAL              PUBLISH
              716  COMPARE_OP               ==
          718_720  POP_JUMP_IF_FALSE   746  'to 746'

 L. 409       722  LOAD_GLOBAL              asyncio
              724  LOAD_ATTR                ensure_future
              726  LOAD_FAST                'self'
              728  LOAD_METHOD              handle_publish
              730  LOAD_FAST                'packet'
              732  CALL_METHOD_1         1  ''
              734  LOAD_FAST                'self'
              736  LOAD_ATTR                _loop
              738  LOAD_CONST               ('loop',)
              740  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              742  STORE_FAST               'task'
              744  JUMP_FORWARD        838  'to 838'
            746_0  COME_FROM           718  '718'

 L. 410       746  LOAD_FAST                'packet'
              748  LOAD_ATTR                fixed_header
              750  LOAD_ATTR                packet_type
              752  LOAD_GLOBAL              DISCONNECT
              754  COMPARE_OP               ==
          756_758  POP_JUMP_IF_FALSE   784  'to 784'

 L. 411       760  LOAD_GLOBAL              asyncio
              762  LOAD_ATTR                ensure_future
              764  LOAD_FAST                'self'
              766  LOAD_METHOD              handle_disconnect
              768  LOAD_FAST                'packet'
              770  CALL_METHOD_1         1  ''
              772  LOAD_FAST                'self'
              774  LOAD_ATTR                _loop
              776  LOAD_CONST               ('loop',)
              778  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              780  STORE_FAST               'task'
              782  JUMP_FORWARD        838  'to 838'
            784_0  COME_FROM           756  '756'

 L. 412       784  LOAD_FAST                'packet'
              786  LOAD_ATTR                fixed_header
              788  LOAD_ATTR                packet_type
              790  LOAD_GLOBAL              CONNECT
              792  COMPARE_OP               ==
          794_796  POP_JUMP_IF_FALSE   810  'to 810'

 L. 413       798  LOAD_FAST                'self'
              800  LOAD_METHOD              handle_connect
              802  LOAD_FAST                'packet'
              804  CALL_METHOD_1         1  ''
              806  POP_TOP          
              808  JUMP_FORWARD        838  'to 838'
            810_0  COME_FROM           794  '794'

 L. 415       810  LOAD_FAST                'self'
              812  LOAD_ATTR                logger
              814  LOAD_METHOD              warning
              816  LOAD_STR                 '%s Unhandled packet type: %s'

 L. 416       818  LOAD_FAST                'self'
              820  LOAD_ATTR                session
              822  LOAD_ATTR                client_id
              824  LOAD_FAST                'packet'
              826  LOAD_ATTR                fixed_header
              828  LOAD_ATTR                packet_type
              830  BUILD_TUPLE_2         2 

 L. 415       832  BINARY_MODULO    
              834  CALL_METHOD_1         1  ''
              836  POP_TOP          
            838_0  COME_FROM           808  '808'
            838_1  COME_FROM           782  '782'
            838_2  COME_FROM           744  '744'
            838_3  COME_FROM           706  '706'
            838_4  COME_FROM           668  '668'
            838_5  COME_FROM           630  '630'
            838_6  COME_FROM           592  '592'
            838_7  COME_FROM           552  '552'
            838_8  COME_FROM           512  '512'
            838_9  COME_FROM           472  '472'
           838_10  COME_FROM           432  '432'
           838_11  COME_FROM           392  '392'
           838_12  COME_FROM           352  '352'
           838_13  COME_FROM           312  '312'

 L. 417       838  LOAD_FAST                'task'
          840_842  POP_JUMP_IF_FALSE   882  'to 882'

 L. 418       844  LOAD_FAST                'running_tasks'
              846  LOAD_METHOD              append
              848  LOAD_FAST                'task'
              850  CALL_METHOD_1         1  ''
              852  POP_TOP          
              854  JUMP_FORWARD        882  'to 882'
            856_0  COME_FROM           154  '154'

 L. 420       856  LOAD_FAST                'self'
              858  LOAD_ATTR                logger
              860  LOAD_METHOD              debug
              862  LOAD_STR                 '%s No more data (EOF received), stopping reader coro'
              864  LOAD_FAST                'self'
              866  LOAD_ATTR                session
              868  LOAD_ATTR                client_id
              870  BINARY_MODULO    
              872  CALL_METHOD_1         1  ''
              874  POP_TOP          

 L. 421       876  POP_BLOCK        
          878_880  JUMP_ABSOLUTE      1122  'to 1122'
            882_0  COME_FROM           854  '854'
            882_1  COME_FROM           840  '840'
              882  POP_BLOCK        
              884  JUMP_BACK            48  'to 48'
            886_0  COME_FROM_FINALLY    48  '48'

 L. 422       886  DUP_TOP          
              888  LOAD_GLOBAL              MQTTException
              890  COMPARE_OP               exception-match
          892_894  POP_JUMP_IF_FALSE   918  'to 918'
              896  POP_TOP          
              898  POP_TOP          
              900  POP_TOP          

 L. 423       902  LOAD_FAST                'self'
              904  LOAD_ATTR                logger
              906  LOAD_METHOD              debug
              908  LOAD_STR                 'Message discarded'
              910  CALL_METHOD_1         1  ''
              912  POP_TOP          
              914  POP_EXCEPT       
              916  JUMP_BACK            48  'to 48'
            918_0  COME_FROM           892  '892'

 L. 424       918  DUP_TOP          
              920  LOAD_GLOBAL              asyncio
              922  LOAD_ATTR                CancelledError
              924  COMPARE_OP               exception-match
          926_928  POP_JUMP_IF_FALSE   958  'to 958'
              930  POP_TOP          
              932  POP_TOP          
              934  POP_TOP          

 L. 425       936  LOAD_FAST                'self'
              938  LOAD_ATTR                logger
              940  LOAD_METHOD              debug
              942  LOAD_STR                 'Task cancelled, reader loop ending'
              944  CALL_METHOD_1         1  ''
              946  POP_TOP          

 L. 426       948  POP_EXCEPT       
          950_952  JUMP_ABSOLUTE      1122  'to 1122'
              954  POP_EXCEPT       
              956  JUMP_BACK            48  'to 48'
            958_0  COME_FROM           926  '926'

 L. 427       958  DUP_TOP          
              960  LOAD_GLOBAL              asyncio
              962  LOAD_ATTR                TimeoutError
              964  COMPARE_OP               exception-match
          966_968  POP_JUMP_IF_FALSE  1008  'to 1008'
              970  POP_TOP          
              972  POP_TOP          
              974  POP_TOP          

 L. 428       976  LOAD_FAST                'self'
              978  LOAD_ATTR                logger
              980  LOAD_METHOD              debug
              982  LOAD_STR                 '%s Input stream read timeout'
              984  LOAD_FAST                'self'
              986  LOAD_ATTR                session
              988  LOAD_ATTR                client_id
              990  BINARY_MODULO    
              992  CALL_METHOD_1         1  ''
              994  POP_TOP          

 L. 429       996  LOAD_FAST                'self'
              998  LOAD_METHOD              handle_read_timeout
             1000  CALL_METHOD_0         0  ''
             1002  POP_TOP          
             1004  POP_EXCEPT       
             1006  JUMP_BACK            48  'to 48'
           1008_0  COME_FROM           966  '966'

 L. 430      1008  DUP_TOP          
             1010  LOAD_GLOBAL              NoDataException
             1012  COMPARE_OP               exception-match
         1014_1016  POP_JUMP_IF_FALSE  1048  'to 1048'
             1018  POP_TOP          
             1020  POP_TOP          
             1022  POP_TOP          

 L. 431      1024  LOAD_FAST                'self'
             1026  LOAD_ATTR                logger
             1028  LOAD_METHOD              debug
             1030  LOAD_STR                 '%s No data available'
             1032  LOAD_FAST                'self'
             1034  LOAD_ATTR                session
             1036  LOAD_ATTR                client_id
             1038  BINARY_MODULO    
             1040  CALL_METHOD_1         1  ''
             1042  POP_TOP          
             1044  POP_EXCEPT       
             1046  JUMP_BACK            48  'to 48'
           1048_0  COME_FROM          1014  '1014'

 L. 432      1048  DUP_TOP          
             1050  LOAD_GLOBAL              BaseException
             1052  COMPARE_OP               exception-match
         1054_1056  POP_JUMP_IF_FALSE  1118  'to 1118'
             1058  POP_TOP          
             1060  STORE_FAST               'e'
             1062  POP_TOP          
             1064  SETUP_FINALLY      1106  'to 1106'

 L. 433      1066  LOAD_FAST                'self'
             1068  LOAD_ATTR                logger
             1070  LOAD_METHOD              warning
             1072  LOAD_STR                 '%s Unhandled exception in reader coro: %r'
             1074  LOAD_GLOBAL              type
             1076  LOAD_FAST                'self'
             1078  CALL_FUNCTION_1       1  ''
             1080  LOAD_ATTR                __name__
             1082  LOAD_FAST                'e'
             1084  BUILD_TUPLE_2         2 
             1086  BINARY_MODULO    
             1088  CALL_METHOD_1         1  ''
             1090  POP_TOP          

 L. 434      1092  POP_BLOCK        
             1094  POP_EXCEPT       
             1096  CALL_FINALLY       1106  'to 1106'
         1098_1100  JUMP_ABSOLUTE      1122  'to 1122'
             1102  POP_BLOCK        
             1104  BEGIN_FINALLY    
           1106_0  COME_FROM          1096  '1096'
           1106_1  COME_FROM_FINALLY  1064  '1064'
             1106  LOAD_CONST               None
             1108  STORE_FAST               'e'
             1110  DELETE_FAST              'e'
             1112  END_FINALLY      
             1114  POP_EXCEPT       
             1116  JUMP_BACK            48  'to 48'
           1118_0  COME_FROM          1054  '1054'
             1118  END_FINALLY      
             1120  JUMP_BACK            48  'to 48'

 L. 435      1122  LOAD_FAST                'running_tasks'
         1124_1126  POP_JUMP_IF_FALSE  1144  'to 1144'

 L. 436      1128  LOAD_FAST                'running_tasks'
             1130  LOAD_METHOD              popleft
             1132  CALL_METHOD_0         0  ''
             1134  LOAD_METHOD              cancel
             1136  CALL_METHOD_0         0  ''
             1138  POP_TOP          
         1140_1142  JUMP_BACK          1122  'to 1122'
           1144_0  COME_FROM          1124  '1124'

 L. 437      1144  LOAD_FAST                'self'
             1146  LOAD_METHOD              handle_connection_closed
             1148  CALL_METHOD_0         0  ''
             1150  GET_YIELD_FROM_ITER
             1152  LOAD_CONST               None
             1154  YIELD_FROM       
             1156  POP_TOP          

 L. 438      1158  LOAD_FAST                'self'
             1160  LOAD_ATTR                _reader_stopped
             1162  LOAD_METHOD              set
             1164  CALL_METHOD_0         0  ''
             1166  POP_TOP          

 L. 439      1168  LOAD_FAST                'self'
             1170  LOAD_ATTR                logger
             1172  LOAD_METHOD              debug
             1174  LOAD_STR                 '%s Reader coro stopped'
             1176  LOAD_FAST                'self'
             1178  LOAD_ATTR                session
             1180  LOAD_ATTR                client_id
             1182  BINARY_MODULO    
             1184  CALL_METHOD_1         1  ''
             1186  POP_TOP          

 L. 440      1188  LOAD_FAST                'self'
             1190  LOAD_METHOD              stop
             1192  CALL_METHOD_0         0  ''
             1194  GET_YIELD_FROM_ITER
             1196  LOAD_CONST               None
             1198  YIELD_FROM       
             1200  POP_TOP          

Parse error at or near `COME_FROM' instruction at offset 882_0

    @asyncio.coroutine
    def _send_packet(self, packet):
        try:
            with (yield from self._write_lock):
                (yield from packet.to_stream(self.writer))
            if self._keepalive_task:
                self._keepalive_task.cancel()
                self._keepalive_task = self._loop.call_later(self.keepalive_timeout, self.handle_write_timeout)
            (yield from self.plugins_manager.fire_event(EVENT_MQTT_PACKET_SENT, packet=packet, session=(self.session)))
        except ConnectionResetError as cre:
            try:
                (yield from self.handle_connection_closed())
                raise
            finally:
                cre = None
                del cre

        except BaseException as e:
            try:
                self.logger.warning('Unhandled exception: %s' % e)
                raise
            finally:
                e = None
                del e

        if False:
            yield None

    @asyncio.coroutine
    def mqtt_deliver_next_message(self):
        if self.logger.isEnabledFor(logging.DEBUG):
            self.logger.debug('%d message(s) available for delivery' % self.session.delivered_message_queue.qsize())
        try:
            message = yield from self.session.delivered_message_queue.get()
        except asyncio.CancelledError:
            message = None
        else:
            if self.logger.isEnabledFor(logging.DEBUG):
                self.logger.debug('Delivering message %s' % message)
            return message
        if False:
            yield None

    def handle_write_timeout(self):
        self.logger.debug('%s write timeout unhandled' % self.session.client_id)

    def handle_read_timeout(self):
        self.logger.debug('%s read timeout unhandled' % self.session.client_id)

    @asyncio.coroutine
    def handle_connack(self, connack: ConnackPacket):
        self.logger.debug('%s CONNACK unhandled' % self.session.client_id)

    @asyncio.coroutine
    def handle_connect(self, connect: ConnectPacket):
        self.logger.debug('%s CONNECT unhandled' % self.session.client_id)

    @asyncio.coroutine
    def handle_subscribe(self, subscribe: SubscribePacket):
        self.logger.debug('%s SUBSCRIBE unhandled' % self.session.client_id)

    @asyncio.coroutine
    def handle_unsubscribe(self, subscribe: UnsubscribePacket):
        self.logger.debug('%s UNSUBSCRIBE unhandled' % self.session.client_id)

    @asyncio.coroutine
    def handle_suback(self, suback: SubackPacket):
        self.logger.debug('%s SUBACK unhandled' % self.session.client_id)

    @asyncio.coroutine
    def handle_unsuback(self, unsuback: UnsubackPacket):
        self.logger.debug('%s UNSUBACK unhandled' % self.session.client_id)

    @asyncio.coroutine
    def handle_pingresp(self, pingresp: PingRespPacket):
        self.logger.debug('%s PINGRESP unhandled' % self.session.client_id)

    @asyncio.coroutine
    def handle_pingreq(self, pingreq: PingReqPacket):
        self.logger.debug('%s PINGREQ unhandled' % self.session.client_id)

    @asyncio.coroutine
    def handle_disconnect(self, disconnect: DisconnectPacket):
        self.logger.debug('%s DISCONNECT unhandled' % self.session.client_id)

    @asyncio.coroutine
    def handle_connection_closed(self):
        self.logger.debug('%s Connection closed unhandled' % self.session.client_id)

    @asyncio.coroutine
    def handle_puback(self, puback: PubackPacket):
        packet_id = puback.variable_header.packet_id
        try:
            waiter = self._puback_waiters[packet_id]
            waiter.set_result(puback)
        except KeyError:
            self.logger.warning("Received PUBACK for unknown pending message Id: '%d'" % packet_id)
        except InvalidStateError:
            self.logger.warning("PUBACK waiter with Id '%d' already done" % packet_id)

    @asyncio.coroutine
    def handle_pubrec(self, pubrec: PubrecPacket):
        packet_id = pubrec.packet_id
        try:
            waiter = self._pubrec_waiters[packet_id]
            waiter.set_result(pubrec)
        except KeyError:
            self.logger.warning('Received PUBREC for unknown pending message with Id: %d' % packet_id)
        except InvalidStateError:
            self.logger.warning("PUBREC waiter with Id '%d' already done" % packet_id)

    @asyncio.coroutine
    def handle_pubcomp(self, pubcomp: PubcompPacket):
        packet_id = pubcomp.packet_id
        try:
            waiter = self._pubcomp_waiters[packet_id]
            waiter.set_result(pubcomp)
        except KeyError:
            self.logger.warning('Received PUBCOMP for unknown pending message with Id: %d' % packet_id)
        except InvalidStateError:
            self.logger.warning("PUBCOMP waiter with Id '%d' already done" % packet_id)

    @asyncio.coroutine
    def handle_pubrel(self, pubrel: PubrelPacket):
        packet_id = pubrel.packet_id
        try:
            waiter = self._pubrel_waiters[packet_id]
            waiter.set_result(pubrel)
        except KeyError:
            self.logger.warning('Received PUBREL for unknown pending message with Id: %d' % packet_id)
        except InvalidStateError:
            self.logger.warning("PUBREL waiter with Id '%d' already done" % packet_id)

    @asyncio.coroutine
    def handle_publish(self, publish_packet: PublishPacket):
        packet_id = publish_packet.variable_header.packet_id
        qos = publish_packet.qos
        incoming_message = IncomingApplicationMessage(packet_id, publish_packet.topic_name, qos, publish_packet.data, publish_packet.retain_flag)
        incoming_message.publish_packet = publish_packet
        (yield from self._handle_message_flow(incoming_message))
        self.logger.debug('Message queue size: %d' % self.session.delivered_message_queue.qsize())
        if False:
            yield None