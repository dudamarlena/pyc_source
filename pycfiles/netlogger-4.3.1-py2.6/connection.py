# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-x86_64/egg/netlogger/amqp/connection.py
# Compiled at: 2010-09-14 08:48:37
"""
Classes and defaults to provide Connect, Produce and Consume objects
for sending and processing amqp messages from a amqp broker like 
RabbitMQ.

Both the Produce and Consume object will automatically create a connection
using the outlined default values (contacting a rabbit broker running on
the localhost).  If a different connection is needed, then a Connect 
object must be explicitly created and passed to Produce or Consume
as an argument:

c = Connect(host='rabbit.example.com')
p = Produce(connection=c)

All of the standard arguments (host, queue and exchange names, etc) can
be changed by passing arguments to the various constructors.

If this module is imported in code that may or may not be using amqp
functionality (like nl_load) then one will need to do an import test.
Warnings should be issued at command-line parsing time if a user
tries to turn on amqp support and code will need to be wrapped to
avoid compile time errors.

An example of usage of the producer with the appropriate tests:

---
from netlogger.amqp.connection import Produce, ConnectionException

if Produce:
    try:
        p = Produce()
    except ConnectionException:
        sys.exit(-1)
    p.send('foo')
    p.send('bar')
    p.send_disconnect()
    p.close()
else:
    print 'py-amqplib support not enabled'
---

Of note in this example is the p.send_disconnect() call.  Py-amqplib
supports sending a sentinel message to the consumers when the stack
of messages has been sent that will cause all the consumers listening
to that exchange to disconnect.  This is also a preferrable way of 
breaking out of the wait() processing loop.  That method will send
that message if desired.

The Produce object can also be used as a log handler with the addition
of an argument:

p = Produce(loghandler=True)
log.addHandler(p)

Writing a consumer is slightly more involved as one must register
a processing callback and it is a good practice to register a
signal handler to cleanly exit the event loop in case a sentinel 
message is not being used to close down the processing loop.

Consumer example:

---
from netlogger.amqp.connection import Consume, ConnectionException
from netlogger import util
import sys, time

c = None

def on_kill(signo, frame):
    global c
    if c:
        c.close()
    time.sleep(.5)
    sys.exit(0)

def callback(msg):
    print msg.body
    msg.channel.basic_ack(msg.delivery_tag)
    
def main():
    util.handleSignals((on_kill, ('SIGTERM', 'SIGINT', 'SIGUSR2')))
    if Consume:
        global c
        try:
            c = Consume()
        except ConnectionException:
            sys.exit(-1)
        c.register(callback)
        c.wait()
        c.close()
    else:
        print 'py-amqplib support not enabled'

if __name__ == '__main__':
    main()
---

Processing of each recieved message will happen in the registered
callback.  That is where the logic to process the messages is written.

The loop will exit cleanly if sent a sentinel disconnect
message by a client or if the approprite signal is sent (Ctrl-C, etc).

"""
from netlogger.nllog import DoesLogging
from netlogger.nlapi import Level, Log
import logging, socket, sys, uuid
__rcsid__ = '$Id$'
__author__ = 'Monte Goode'
_D = {'host': '127.0.0.1', 
   'port': 5672, 
   'user': 'guest', 
   'pass': 'guest', 
   'vhost': '/', 
   'insist': False, 
   'exchange': 'default_nl_ex', 
   'exchange_type': 'direct', 
   'route': 'default_nl_route', 
   'queue': 'uuid', 
   'auto_delete': True, 
   'durable': False, 
   'no_ack': False, 
   'disconnect_message': 'disconnect_consumers_now', 
   'loghandler': False}

class ConnectionException(Exception):

    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)


class AmqpConnectBase(DoesLogging):

    def __init__(self):
        DoesLogging.__init__(self)


try:
    from amqplib import client_0_8 as amqp

    class Connect(AmqpConnectBase):

        def __init__(self, host=_D['host'], port=_D['port'], user=_D['user'], pw=_D['pass'], vhost=_D['vhost'], insist=_D['insist'], **kw):
            """
            Constructor for the Connect class.  Recieves and
            sets various connection options defined by keyword
            parameters.  All parameters have sane default values
            set for connecting to a amqp broker on the localhost.
            
            @type       host: string
            @keyword    host: Host to connect to (default: 127.0.0.1).
            @type       port: integer
            @keyword    port: Port to conenct to (default: 5672).
            @type       user: string
            @keyword    user: User to authenticate as (default: guest).
            @type       pw: string
            @keyword    pw: Password to authenticate with (default: guest).
            @type       vhost: string
            @keyword    vhost: RabbitMQ virtual host to connect to (default: /).
            @type       insist: boolean
            @keyword    insist: Set insist parameter to send to server (default: False).
            @rtype:     None
            @return:    No return value.
            """
            AmqpConnectBase.__init__(self)
            self.host = '%s:%s' % (host, port)
            self.log.info('init.start', msg='Connecting to %s' % self.host)
            self.user = user
            self.pw = pw
            self.vhost = vhost
            self.insist = insist
            vals = {'host': self.host, 
               'user': self.user, 
               'pw': self.pw, 
               'vhost': self.vhost, 
               'insist': self.insist}
            self.log.debug('init.args', **vals)
            self.connection = None
            self.connected = False
            try:
                self.connect()
                self.connected = True
            except socket.error, (val, msg):
                err = 'Unable to open connection to: %s - %s' % (self.host, msg)
                self.log.critical('init', msg=err)
                raise ConnectionException, err

            self.log.debug('init.end')
            return

        def connect(self):
            """
            Connect using the values specified in __init__().
            Called in __init__().
            
            @rtype:     None
            @return:    No return value.
            """
            try:
                self.connection = amqp.Connection(host=self.host, userid=self.user, password=self.pw, virtual_host=self.vhost, insist=self.insist)
            except IOError, err:
                raise ConnectionException('Connecting to host=%s;vhost=%s as user=%s: %s' % (
                 self.host, self.vhost, self.user, err))

        def channel(self):
            """
            Returns the connection channel for the Produce or
            Consume objects to interact with.
            
            @rtype:     amqplib Channel object
            @return:    Returns the channel to a client class.
            """
            return self.connection.channel()

        def close(self):
            """
            Closes current connection down.
            
            @rtype:     None
            @return:    No return value.
            """
            self.connection.close()
            self.log.info('close.end')


    class Consume(AmqpConnectBase):

        def __init__(self, connection=None, exchange=_D['exchange'], exchange_type=_D['exchange_type'], route=_D['route'], queue=_D['queue'], auto_delete=_D['auto_delete'], durable=_D['durable'], no_ack=_D['no_ack'], disconnect=_D['disconnect_message'], **kw):
            """
            Constructor for the Consume class.  Use this to write code
            that listens to an exchange and process the messages.  When called
            with no arguments, a sane built-in Connect class will connect
            to a localhost server.
            
            @type       connection: netlogger.amqp.Connect instance.
            @keyword    connection: Connect object to use to contact server.
            @type       exchange: string
            @keyword    exchange: Exchange to use (default: default_ex)
            @type       exchange_type: string
            @keyword    exchange_type: They type of exchange to create ie: topic, 
                        fanout or direct (default: direct).
            @type       route: string
            @keyword    route: the routing_key to use (default: default_route).
            @type       queue: string
            @keyword    queue: Queue to use (default: uuid - will generate a 
                        unique queue name).
            @type       auto_delete: boolean
            @keyword    auto_delete: Set auto_delete for queues and exchanges 
                        (default: True).
            @type       durable: boolean
            @keyword    durable: Set durable bit for queues and exchanges 
                        (default: False).
            @type       disconnect: string
            @keyword    disconnect: The sentinel message that will cause consumers
                        to disconnect from server (default: disconnect_consumers_now).
            @rtype:     None
            @return:    No return value.
            """
            AmqpConnectBase.__init__(self)
            self.log.info('init.start')
            self.connection = connection or Connect()
            self.channel = self.connection.channel()
            self.exchange = exchange
            self.exchange_type = exchange_type
            self.route = route
            self.queue = queue
            self.auto_delete = auto_delete
            self.durable = durable
            self.no_ack = no_ack
            self.disconnect = disconnect
            vals = {'exchange': self.exchange, 
               'exchange_type': self.exchange_type, 
               'route': self.route, 
               'queue': self.queue, 
               'auto_delete': self.auto_delete, 
               'durable': self.durable, 
               'disconnect': self.disconnect}
            self.log.debug('init.args', **vals)
            if self.queue == 'uuid':
                self.queue = str(uuid.uuid4())
            self.callback = None
            self.waiting = True
            self.tag = None
            self.cancelled = False
            self.channel.queue_declare(queue=self.queue, durable=self.durable, auto_delete=self.auto_delete)
            self.channel.exchange_declare(exchange=self.exchange, type=self.exchange_type, durable=self.durable, auto_delete=self.auto_delete)
            self.channel.queue_bind(queue=self.queue, exchange=self.exchange, routing_key=self.route)
            self.tag = self.channel.basic_consume(queue=self.queue, callback=self.dispatch, no_ack=self.no_ack)
            return

        def register(self, callback, *args):
            """
            Registers the external callback that the messages
            will be forwarded to for processing.
            
            @type   callback: Reference to a function or method
            @param  callback: The external callback to forward messages to.
            @type  args: List
            @param args: Additional arguments to pass to the callback
            @rtype:     None
            @return:    No return value.
            """
            self.callback = callback
            self.callback_args = args

        def dispatch(self, msg):
            """
            Internal dispatch method.  Handles the sentinel hangup
            message if it is received or shuttles the message to the
            processing callback otherwise.
            
            @type   msg: a py-amqplib Message object
            @param  msg: The current message that has been recieved from
                        the server.
            @rtype:     None
            @return:    No return value.
            """
            if self.callback:
                if msg.body == self.disconnect:
                    self.log.info('dispatch', msg='Recieved disconnect message')
                    self.channel.basic_cancel(self.tag)
                    self.waiting = False
                    self.cancelled = True
                    return
                self.log.debug('dispatch', msg='Dispatching message: %s' % msg.body)
                self.callback(msg, *self.callback_args)
            else:
                self.log.warn('dispatch', msg='No callback registered')

        def wait(self):
            """
            Starts the amqp event loop.  Must be called to begin
            receiving messages.
            
            @rtype:     None
            @return:    No return value.
            """
            while self.waiting:
                self.channel.wait()

        def close(self):
            """
            Closes down all the moving parts.  Should be called even
            if shutdown via sentinel message is triggered.
            
            @rtype:     None
            @return:    No return value.
            """
            if not self.cancelled:
                self.channel.basic_cancel(self.tag)
            self.waiting = False
            self.channel.close()
            self.connection.close()
            self.log.info('close.end')


    class Produce(logging.Handler, AmqpConnectBase):

        def __init__(self, connection=None, exchange=_D['exchange'], route=_D['route'], disconnect=_D['disconnect_message'], exchange_type=_D['exchange_type'], auto_delete=_D['auto_delete'], durable=_D['durable'], loghandler=_D['loghandler'], **kw):
            """
            Constructor of the Producer class to send messages to
            the amqp server.  When called with no arguments, a sane 
            built-in Connect class will connect to a localhost server.
            
            @type       connection: netlogger.amqp.Connect instance.
            @keyword    connection: Connect object to use to contact server.
            @type       exchange: string
            @keyword    exchange: Exchange to use (default: default_ex)
            @type       exchange_type: string
            @keyword    exchange_type: They type of exchange to create ie: topic,
            @type       auto_delete: boolean
            @keyword    auto_delete: Set auto_delete for queues and exchanges 
                        (default: True).
            @type       durable: boolean
            @keyword    durable: Set durable bit for queues and exchanges 
                        (default: False).
 
            @type       route: string
            @keyword    route: the routing_key to use (default: default_route).
                        If it starts with '@' then make it dynamic based on the
                        field name after the '@'.
            @type       disconnect: string
            @keyword    disconnect: The sentinel message that will cause consumers
                        to disconnect from server (default: disconnect_consumers_now).
            @type       loghandler: boolean
            @keyword    loghandler: Toggles on the ability to be passed to a logging
                        object to be used as a logging handler (default: False).
            @rtype:     None
            @return:    No return value.
            """
            AmqpConnectBase.__init__(self)
            if loghandler:
                logging.Handler.__init__(self)
            self.log.info('init.start')
            self.connection = connection or Connect()
            self.channel = self.connection.channel()
            self.exchange = exchange
            self.channel.exchange_declare(exchange=self.exchange, type=exchange_type, durable=durable, auto_delete=auto_delete)
            self.route = route
            self.disconnect = disconnect
            self.log.info('init.end')
            vals = {'exchange': self.exchange, 
               'route': self.route, 
               'disconnect': self.disconnect, 
               'loghandler': loghandler}
            self.log.debug('init.args', **vals)

        def send(self, s):
            """
            The external method called to send a message to the server.
            
            @type   s: string
            @param  s: The string to send as a message to the server.
            @rtype:     None
            @return:    No return value.
            """
            msg = amqp.Message(s, content_type='text/plain')
            if self._dbg:
                self.log.debug('send', msg='Sending: %s' % s)
            self.channel.basic_publish(msg, exchange=self.exchange, routing_key=self.route)

        def send_disconnect(self):
            """
            Send a sentinel disconnnect signal to the exchange currently
            connected to.  This can be sent when the stack of messages 
            is complete to signal that all the consumers can exit.
            
            @rtype:     None
            @return:    No return value.
            """
            self.log.debug('send_disconnect', msg='Sending disconnect string: %s' % self.disconnect)
            self.send(self.disconnect)

        def emit(self, data):
            """
            Exposes an emit method for use as a logging handler.  Calls
            .getMessage() on the incoming object and passes the result
            to self.send().
            
            @type   data: Log object
            @param  data: Incoming log object when using this as a logging
            handler.
            @rtype:     None
            @return:    No return value.
            """
            self.send(data.getMessage())

        def close(self):
            """
            Shuts down the current channel and connection.
            
            @rtype:     None
            @return:    No return value.
            """
            try:
                self.channel.close()
            except amqp.exceptions.AMQPChannelException, e:
                self.log.warn('close', msg='Error closing channel: %s' % e[1])

            self.connection.close()
            self.log.info('close.end')


    class NlProduce(Produce):
        """
        Simple wrapper subclass allow a producer to be able to be dropped
        in where a nlapi.Log would be used to write to (eg: nl_parse, etc).
        """

        def __init__(self, connection=None, exchange=_D['exchange'], route=_D['route'], disconnect=_D['disconnect_message'], loghandler=_D['loghandler'], **kw):
            """
            Same init() args as superclass:
            
            @type       connection: netlogger.amqp.Connect instance.
            @keyword    connection: Connect object to use to contact server.
            @type       exchange: string
            @keyword    exchange: Exchange to use (default: default_ex)
            @type       route: string
            @keyword    route: the routing_key to use (default: default_route).
            @type       disconnect: string
            @keyword    disconnect: The sentinel message that will cause consumers
                        to disconnect from server (default: disconnect_consumers_now).
            @type       loghandler: boolean
            @keyword    loghandler: Toggles on the ability to be passed to a logging
                        object to be used as a logging handler (default: False).
            @rtype:     None
            @return:    No return value.
            """
            Produce.__init__(self, connection=connection, exchange=exchange, route=route, disconnect=disconnect, loghandler=loghandler, **kw)
            self.event_route = route.lower() == '@event'
            self.formatter = Log(float_time=True)

        def write(self, event='event', ts=None, level=Level.INFO, **kw):
            """
            Format the incoming dict into a nl string and feed to send()
            """
            if not ts:
                ts = time.time()
            buf = self.formatter.format(event, ts, level, kw)
            if self.event_route:
                self.route = event
            self.send(buf)

        def flush(self):
            """
            Noop method - just here to satisfy calling code.
            """
            pass


except ImportError:
    Connect = None
    Consume = None
    Produce = None
    NlProduce = None