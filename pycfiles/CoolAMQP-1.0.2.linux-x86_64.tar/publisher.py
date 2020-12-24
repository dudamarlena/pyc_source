# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/travis/virtualenv/python2.7.15/lib/python2.7/site-packages/coolamqp/attaches/publisher.py
# Compiled at: 2020-04-03 16:00:47
"""
Module used to publish messages.

Expect wild NameErrors if you build this without RabbitMQ extensions (enabled by default),
and try to use MODE_CNPUB.

If you use a broker that doesn't support these, just don't use MODE_CNPUB. CoolAMQP is smart enough
to check with the broker beforehand.
"""
from __future__ import absolute_import, division, print_function
import collections, logging, warnings, six
from coolamqp.framing.definitions import ChannelOpenOk, BasicPublish, Basic, BasicAck
from coolamqp.framing.frames import AMQPMethodFrame, AMQPBodyFrame, AMQPHeaderFrame
try:
    from coolamqp.framing.definitions import ConfirmSelect, ConfirmSelectOk, BasicNack, ChannelFlow, ChannelFlowOk, ConnectionBlocked, ConnectionUnblocked
except ImportError:
    pass

from coolamqp.attaches.channeler import Channeler, ST_ONLINE, ST_OFFLINE
from coolamqp.uplink import PUBLISHER_CONFIRMS, MethodWatch, FailWatch
from coolamqp.attaches.utils import AtomicTagger, FutureConfirmableRejectable, Synchronized
from concurrent.futures import Future
from coolamqp.objects import Exchange
logger = logging.getLogger(__name__)
CnpubMessageSendOrder = collections.namedtuple('CnpubMessageSendOrder', ('message',
                                                                         'exchange_name',
                                                                         'routing_key',
                                                                         'future'))

class Publisher(Channeler, Synchronized):
    """
    An object that is capable of sucking into a Connection and sending messages.
    Depending on it's characteristic, it may process messages in:

        - non-ack mode (default) - messages will be dropped on the floor if there is no active uplink
        - Consumer Publish mode - requires broker support, each message will be ACK/NACKed by the broker
                                  messages will survive broker reconnections.

                                  If you support this, it is your job to ensure that broker supports
                                  publisher_confirms. If it doesn't, this publisher will enter ST_OFFLINE
                                  and emit a warning.

        Other modes may be added in the future.

    Since this may be called by other threads than ListenerThread, this has locking.

    _pub and on_fail are synchronized so that _pub doesn't see a partially destroyed class.

    :param mode: Publishing mode to use. One of:
         MODE_NOACK - use non-ack mode
         MODE_CNPUB - use consumer publishing mode. A switch to MODE_TXPUB will be made
                      if broker does not support these.
    :raise ValueError: mode invalid
    """
    MODE_NOACK = 0
    MODE_CNPUB = 1

    class UnusablePublisher(Exception):
        """This publisher will never work (eg. MODE_CNPUB on a broker not supporting publisher confirms)"""
        pass

    def __init__(self, mode):
        Channeler.__init__(self)
        Synchronized.__init__(self)
        if mode not in (Publisher.MODE_NOACK, Publisher.MODE_CNPUB):
            raise ValueError('Invalid publisher mode')
        self.mode = mode
        self.messages = collections.deque()
        self.tagger = None
        self.critically_failed = False
        self.content_flow = True
        self.blocked = False
        self.frames_to_send = []
        return

    @Synchronized.synchronized
    def attach(self, connection):
        Channeler.attach(self, connection)
        connection.watch(FailWatch(self.on_fail))

    def on_connection_blocked(self, payload):
        if isinstance(payload, ConnectionBlocked):
            self.blocked = True
        elif isinstance(payload, ConnectionUnblocked):
            self.blocked = False
            if self.content_flow:
                self.connection.send(self.frames_to_send)
                self.frames_to_send = []

    def on_flow_control(self, payload):
        """Called on ChannelFlow"""
        assert isinstance(ChannelFlow, payload)
        self.content_flow = payload.active
        self.connection.send([
         AMQPMethodFrame(self.channel_id, ChannelFlowOk(payload.active))])
        if payload.active and not self.blocked:
            self.connection.send(self.frames_to_send)
            self.frames_to_send = []

    @Synchronized.synchronized
    def on_fail(self):
        self.state = ST_OFFLINE

    def _pub(self, message, exchange_name, routing_key):
        """
        Just send the message. Sends BasicDeliver + header + body.

        BECAUSE OF publish THIS CAN GET CALLED BY FOREIGN THREAD.

        :param message: Message instance
        :param exchange_name: exchange to use
        :param routing_key: routing key to use
        :type exchange_name: bytes
        :param routing_key: bytes
        """
        bodies = []
        body = memoryview(message.body)
        max_body_size = self.connection.frame_max - AMQPBodyFrame.FRAME_SIZE_WITHOUT_PAYLOAD - 16
        while len(body) > 0:
            bodies.append(body[:max_body_size])
            body = body[max_body_size:]

        frames_to_send = [
         AMQPMethodFrame(self.channel_id, BasicPublish(exchange_name, routing_key, False, False)),
         AMQPHeaderFrame(self.channel_id, Basic.INDEX, 0, len(message.body), message.properties)]
        if len(bodies) == 1:
            frames_to_send.append(AMQPBodyFrame(self.channel_id, bodies[0]))
        if self.content_flow and not self.blocked:
            self.connection.send(frames_to_send)
            if len(bodies) > 1:
                while self.content_flow and not self.blocked and len(bodies) > 0:
                    self.connection.send([AMQPBodyFrame(self.channel_id, bodies[0])])
                    del bodies[0]

                if not self.content_flow and not self.blocked and len(bodies) > 0:
                    for body in bodies:
                        self.frames_to_send.append(AMQPBodyFrame(self.channel_id, body))

        else:
            self.frames_to_send.extend(frames_to_send)
            if len(bodies) > 1:
                for body in bodies:
                    self.frames_to_send.append(AMQPBodyFrame(self.channel_id, body))

    def _mode_cnpub_process_deliveries(self):
        """
        Dispatch all frames that are waiting to be sent

        To be used when  mode is MODE_CNPUB and we just got ST_ONLINE
        """
        assert self.state == ST_ONLINE
        assert self.mode == Publisher.MODE_CNPUB
        assert self.tagger is not None
        while len(self.messages) > 0:
            try:
                msg, xchg, rk, fut = self.messages.popleft()
            except IndexError:
                break

            if not fut.set_running_or_notify_cancel():
                continue
            self.tagger.deposit(self.tagger.get_key(), FutureConfirmableRejectable(fut))
            assert isinstance(xchg, (six.binary_type, six.text_type))
            self._pub(msg, xchg, rk)

        return

    def _on_cnpub_delivery(self, payload):
        """
        This gets called on BasicAck and BasicNack, if mode is MODE_CNPUB
        """
        assert self.mode == Publisher.MODE_CNPUB
        if isinstance(payload, BasicAck):
            self.tagger.ack(payload.delivery_tag, payload.multiple)
        elif isinstance(payload, BasicNack):
            self.tagger.nack(payload.delivery_tag, payload.multiple)

    @Synchronized.synchronized
    def publish(self, message, exchange='', routing_key=''):
        """
        Schedule to have a message published.

        If mode is MODE_CNPUB:
            this function will return a Future. Future can end either with success (result will be None),
            or exception (a plain Exception instance). Exception will happen when broker NACKs the message:
            that, according to RabbitMQ, means an internal error in Erlang process.

            Returned Future can be cancelled - this will prevent from sending the message, if it hasn't commenced yet.

        If mode is MODE_NOACK:
            this function returns None. Messages are dropped on the floor if there's no connection.

        :param message: Message object to send
        :param exchange: exchange name to use. Default direct exchange by default. Can also be an Exchange object.
        :type exchange: bytes, str or Exchange instance
        :param routing_key: routing key to use
        :return: a Future instance, or None
        :raise Publisher.UnusablePublisher: this publisher will never work (eg. MODE_CNPUB on Non-RabbitMQ)
        """
        if isinstance(exchange, Exchange):
            exchange = exchange.name.encode('utf8')
        elif isinstance(exchange, six.text_type):
            exchange = exchange.encode('utf8')
        assert isinstance(exchange, six.binary_type)
        if self.mode == Publisher.MODE_NOACK:
            if self.state != ST_ONLINE:
                logger.debug('Publish request, but not connected - dropping the message')
            else:
                self._pub(message, exchange, routing_key)
        else:
            if self.mode == Publisher.MODE_CNPUB:
                fut = Future()
                cnpo = CnpubMessageSendOrder(message, exchange, routing_key, fut)
                self.messages.append(cnpo)
                if self.state == ST_ONLINE:
                    self._mode_cnpub_process_deliveries()
                return fut
            raise Exception('Invalid mode')

    def on_operational(self, operational):
        state = {True: 'up', False: 'down'}[operational]
        mode = {Publisher.MODE_NOACK: 'noack', Publisher.MODE_CNPUB: 'cnpub'}[self.mode]
        logger.info('Publisher %s is %s', mode, state)

    def on_setup(self, payload):
        if self.mode == Publisher.MODE_CNPUB:
            if PUBLISHER_CONFIRMS not in self.connection.extensions:
                warnings.warn('Broker does not support publisher_confirms, refusing to start publisher', RuntimeWarning)
                self.state = ST_OFFLINE
                self.critically_failed = True
                return
        logger.debug('Publisher on_setup, payload=%s', payload)
        if isinstance(payload, ChannelOpenOk):
            mw = self.watch_for_method(ChannelFlow, self.on_flow_control)
            mw.oneshot = False
            mw = self.connection.watch_for_method(0, (ConnectionBlocked, ConnectionUnblocked), self.on_connection_blocked)
            mw.oneshot = False
            if self.mode == Publisher.MODE_CNPUB:
                self.method_and_watch(ConfirmSelect(False), ConfirmSelectOk, self.on_setup)
            elif self.mode == Publisher.MODE_NOACK:
                self.state = ST_ONLINE
                self.on_operational(True)
        elif self.mode == Publisher.MODE_CNPUB and isinstance(payload, ConfirmSelectOk):
            self.tagger = AtomicTagger()
            self.state = ST_ONLINE
            self.on_operational(True)
            mw = MethodWatch(self.channel_id, (BasicAck, BasicNack), self._on_cnpub_delivery)
            mw.oneshot = False
            self.connection.watch(mw)
            self._mode_cnpub_process_deliveries()