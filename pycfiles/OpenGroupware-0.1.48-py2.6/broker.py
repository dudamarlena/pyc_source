# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/coils/core/broker.py
# Compiled at: 2012-10-12 07:02:39
import yaml, logging, os
from coils.foundation.api.amq.transport import Timeout as AMQTimeOut
import coils.foundation.api.amq as amqp
from coils.foundation import Backend, ServerDefaultsManager
from packet import Packet
from exception import CoilsException, NotImplementedException
EXCHANGE_NAME = 'OpenGroupware_Coils'
EXCHANGE_TYPE = 'direct'

class Broker(object):
    __slots__ = ('_log', '_connection', '_channel', '_tag', '_callbacks', '_subscriptions')
    __AMQDebugOn__ = None
    __AMQConfig__ = None

    def __init__(self):
        sd = ServerDefaultsManager()
        self._log = logging.getLogger(('coils.broker[{0}]').format(os.getpid()))
        if Broker.__AMQDebugOn__ is None or Broker.__AMQConfig__ is None:
            Broker.__AMQDebugOn__ = sd.bool_for_default('BusDebugEnabled')
            Broker.__AMQConfig__ = sd.default_as_dict('AMQConfigDictionary')
        self._callbacks = {}
        self._subscriptions = {}
        self._connect()
        self._log.info(('Bus Debug Enabled: {0}').format(Broker.__AMQDebugOn__))
        return

    def _connect(self):
        self._connection = amqp.Connection(host=('{0}:{1}').format(Broker.__AMQConfig__.get('hostname', '127.0.0.1'), Broker.__AMQConfig__.get('port', 5672)), userid=Broker.__AMQConfig__.get('username', 'guest'), password=Broker.__AMQConfig__.get('password', 'guest'), ssl=False, virtual_host=Broker.__AMQConfig__.get('vhost', '/'))
        self._channel = self._connection.channel()
        if self.debug:
            self._log.debug('connected')
        for (name, data) in self.subscriptions.iteritems():
            self.subscribe(name, data[0], durable=data[1], auto_delete=data[2], exclusive=data[3], arguements=data[4])

    @staticmethod
    def Create():
        return Broker()

    @property
    def subscriptions(self):
        return self._subscriptions

    @property
    def debug(self):
        return Broker.__AMQDebugOn__

    def subscribe(self, name, callback, durable=False, auto_delete=False, exclusive=False, arguements={}, expiration=None):
        routing_key = name.lower()
        self._channel.exchange_declare(exchange=EXCHANGE_NAME, type=EXCHANGE_TYPE, durable=True, auto_delete=False)
        if expiration:
            expiration = int(expiration)
            if self.debug:
                self._log.debug(('Queue {0} will be created to expire after {1}ms of inactivity.').format(name, expiration))
            arguements['x-expires'] = expiration
        self._channel.queue_declare(queue=name, durable=durable, exclusive=exclusive, auto_delete=auto_delete, arguments=arguements)
        self._channel.queue_bind(queue=name, exchange=EXCHANGE_NAME, routing_key=routing_key)
        if not callback:
            callback = self.receive_message
        self._tag = self._channel.basic_consume(queue=name, no_ack=False, callback=callback)
        if self.debug:
            self._log.debug(('subscribed to {0}').format(routing_key))
        self._subscriptions[routing_key] = (
         callback, durable, auto_delete, exclusive, arguements)

    def unsubscribe(self, name):
        raise NotImplementedException('Not Implemented; patches welcome.')

    @property
    def default_source(self):
        if len(self._subscriptions) > 0:
            default_source = self.subscriptions.keys()[0]
            if self.debug:
                self._log.debug(('defaulting packet source to {0}').format(default_source))
            return default_source
        else:
            return 'null'

    def send(self, packet, callback=None):
        if packet.source is None:
            packet.source = ('{0}/__null').format(self.default_source)
        if self.debug:
            self._log.debug(('sending packet {0} with source of {1} to {2}').format(packet.uuid, packet.source, packet.target))
        message = amqp.Message(yaml.dump(packet))
        message.properties['delivery_mode'] = 2
        routing_key = Packet.Service(packet.target).lower()
        self._channel.basic_publish(message, exchange=EXCHANGE_NAME, routing_key=routing_key)
        if callback is not None:
            if self.debug:
                self._log.debug(('enqueued callback {0}').format(packet.reply_to))
            self._callbacks[packet.uuid] = callback
        return

    def packet_from_message(self, message):
        packet = yaml.load(message.body)
        if self.debug:
            self._log.debug(('Sending AMQ acknowledgement of message {0}').format(message.delivery_tag))
        if packet.source is None:
            raise CoilsException('Broker received a packet with no source address')
        if packet.target is None:
            raise CoilsException('Broker received a packet with no target address')
        self._channel.basic_ack(message.delivery_tag)
        if packet.reply_to in self._callbacks:
            if self._callbacks[packet.reply_to](packet.reply_to, packet.source, packet.target, packet.data):
                del self._callbacks[packet.reply_to]
                if self.debug:
                    self._log.debug(('dequeued callback {0}').format(packet.reply_to))
            return
        else:
            return packet

    def receive_message(self, message):
        return self.packet_from_message(message)

    def close(self):
        try:
            self._channel.close()
            self._connection.close()
        except Exception, e:
            self._log.warn('Exception occurred in closing AMQ connection.')
            self._log.exception(e)

    def wait(self, timeout=None):
        if not timeout:
            timeout = 1
        try:
            self._channel.wait(timeout=timeout)
        except AMQTimeOut:
            return
        except Exception, e:
            self._log.warn('Exception occurred in Broker.wait()')
            self._log.exception(e)
            raise e

        return