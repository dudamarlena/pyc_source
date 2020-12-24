# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/lib/python3.8/site-packages/hbmqtt/broker.py
# Compiled at: 2020-01-25 09:04:28
# Size of source mod 2**32: 37755 bytes
import logging, ssl, websockets, asyncio, sys, re
from asyncio import CancelledError
from collections import deque
from functools import partial
from transitions import Machine, MachineError
from hbmqtt.session import Session
from hbmqtt.mqtt.protocol.broker_handler import BrokerProtocolHandler
from hbmqtt.errors import HBMQTTException, MQTTException
from hbmqtt.utils import format_client_message, gen_client_id
from hbmqtt.adapters import StreamReaderAdapter, StreamWriterAdapter, ReaderAdapter, WriterAdapter, WebSocketsReader, WebSocketsWriter
from plugins.manager import PluginManager, BaseContext
_defaults = {'timeout-disconnect-delay':2, 
 'auth':{'allow-anonymous':True, 
  'password-file':None}}
EVENT_BROKER_PRE_START = 'broker_pre_start'
EVENT_BROKER_POST_START = 'broker_post_start'
EVENT_BROKER_PRE_SHUTDOWN = 'broker_pre_shutdown'
EVENT_BROKER_POST_SHUTDOWN = 'broker_post_shutdown'
EVENT_BROKER_CLIENT_CONNECTED = 'broker_client_connected'
EVENT_BROKER_CLIENT_DISCONNECTED = 'broker_client_disconnected'
EVENT_BROKER_CLIENT_SUBSCRIBED = 'broker_client_subscribed'
EVENT_BROKER_CLIENT_UNSUBSCRIBED = 'broker_client_unsubscribed'
EVENT_BROKER_MESSAGE_RECEIVED = 'broker_message_received'

class BrokerException(BaseException):
    pass


class RetainedApplicationMessage:
    __slots__ = ('source_session', 'topic', 'data', 'qos')

    def __init__(self, source_session, topic, data, qos=None):
        self.source_session = source_session
        self.topic = topic
        self.data = data
        self.qos = qos


class Server:

    def __init__(self, listener_name, server_instance, max_connections=-1, loop=None):
        self.logger = logging.getLogger(__name__)
        self.instance = server_instance
        self.conn_count = 0
        self.listener_name = listener_name
        if loop is not None:
            self._loop = loop
        else:
            self._loop = asyncio.get_event_loop()
        self.max_connections = max_connections
        if self.max_connections > 0:
            self.semaphore = asyncio.Semaphore((self.max_connections), loop=(self._loop))
        else:
            self.semaphore = None

    @asyncio.coroutine
    def acquire_connection(self):
        if self.semaphore:
            yield from self.semaphore.acquire()
        else:
            self.conn_count += 1
            if self.max_connections > 0:
                self.logger.info("Listener '%s': %d/%d connections acquired" % (
                 self.listener_name, self.conn_count, self.max_connections))
            else:
                self.logger.info("Listener '%s': %d connections acquired" % (
                 self.listener_name, self.conn_count))
        if False:
            yield None

    def release_connection(self):
        if self.semaphore:
            self.semaphore.release()
        else:
            self.conn_count -= 1
            if self.max_connections > 0:
                self.logger.info("Listener '%s': %d/%d connections acquired" % (
                 self.listener_name, self.conn_count, self.max_connections))
            else:
                self.logger.info("Listener '%s': %d connections acquired" % (
                 self.listener_name, self.conn_count))

    @asyncio.coroutine
    def close_instance(self):
        if self.instance:
            self.instance.close()
            yield from self.instance.wait_closed()
        if False:
            yield None


class BrokerContext(BaseContext):
    __doc__ = '\n    BrokerContext is used as the context passed to plugins interacting with the broker.\n    It act as an adapter to broker services from plugins developed for HBMQTT broker\n    '

    def __init__(self, broker):
        super().__init__()
        self.config = None
        self._broker_instance = broker

    @asyncio.coroutine
    def broadcast_message(self, topic, data, qos=None):
        yield from self._broker_instance.internal_message_broadcast(topic, data, qos)
        if False:
            yield None

    def retain_message(self, topic_name, data, qos=None):
        self._broker_instance.retain_message(None, topic_name, data, qos)

    @property
    def sessions(self):
        for k, session in self._broker_instance._sessions.items():
            yield session[0]

    @property
    def retained_messages(self):
        return self._broker_instance._retained_messages

    @property
    def subscriptions(self):
        return self._broker_instance._subscriptions


class Broker:
    __doc__ = '\n    MQTT 3.1.1 compliant broker implementation\n\n    :param config: Example Yaml config\n    :param loop: asyncio loop to use. Defaults to ``asyncio.get_event_loop()`` if none is given\n    :param plugin_namespace: Plugin namespace to use when loading plugin entry_points. Defaults to ``hbmqtt.broker.plugins``\n\n    '
    states = [
     'new', 'starting', 'started', 'not_started', 'stopping', 'stopped', 'not_stopped', 'stopped']

    def __init__(self, config=None, loop=None, plugin_namespace=None):
        self.logger = logging.getLogger(__name__)
        self.config = _defaults
        if config is not None:
            self.config.update(config)
        else:
            self._build_listeners_config(self.config)
            if loop is not None:
                self._loop = loop
            else:
                self._loop = asyncio.get_event_loop()
            self._servers = dict()
            self._init_states()
            self._sessions = dict()
            self._subscriptions = dict()
            self._retained_messages = dict()
            self._broadcast_queue = asyncio.Queue(loop=(self._loop))
            self._broadcast_task = None
            context = BrokerContext(self)
            context.config = self.config
            if plugin_namespace:
                namespace = plugin_namespace
            else:
                namespace = 'hbmqtt.broker.plugins'
        self.plugins_manager = PluginManager(namespace, context, self._loop)

    def _build_listeners_config(self, broker_config):
        self.listeners_config = dict()
        try:
            listeners_config = broker_config['listeners']
            defaults = listeners_config['default']
            for listener in listeners_config:
                config = dict(defaults)
                config.update(listeners_config[listener])
                self.listeners_config[listener] = config

        except KeyError as ke:
            try:
                raise BrokerException('Listener config not found invalid: %s' % ke)
            finally:
                ke = None
                del ke

    def _init_states(self):
        self.transitions = Machine(states=(Broker.states), initial='new')
        self.transitions.add_transition(trigger='start', source='new', dest='starting')
        self.transitions.add_transition(trigger='starting_fail', source='starting', dest='not_started')
        self.transitions.add_transition(trigger='starting_success', source='starting', dest='started')
        self.transitions.add_transition(trigger='shutdown', source='started', dest='stopping')
        self.transitions.add_transition(trigger='stopping_success', source='stopping', dest='stopped')
        self.transitions.add_transition(trigger='stopping_failure', source='stopping', dest='not_stopped')
        self.transitions.add_transition(trigger='start', source='stopped', dest='starting')

    @asyncio.coroutine
    def start(self):
        """
            Start the broker to serve with the given configuration

            Start method opens network sockets and will start listening for incoming connections.

            This method is a *coroutine*.
        """
        try:
            self._sessions = dict()
            self._subscriptions = dict()
            self._retained_messages = dict()
            self.transitions.start()
            self.logger.debug('Broker starting')
        except (MachineError, ValueError) as exc:
            try:
                self.logger.warning('[WARN-0001] Invalid method call at this moment: %s' % exc)
                raise BrokerException("Broker instance can't be started: %s" % exc)
            finally:
                exc = None
                del exc

        else:
            (yield from self.plugins_manager.fire_event(EVENT_BROKER_PRE_START))
        try:
            for listener_name in self.listeners_config:
                listener = self.listeners_config[listener_name]
                if 'bind' not in listener:
                    self.logger.debug("Listener configuration '%s' is not bound" % listener_name)
                else:
                    try:
                        max_connections = listener['max_connections']
                    except KeyError:
                        max_connections = -1
                    else:
                        sc = None
                        ssl_active = listener.get('ssl', False)
                        if isinstance(ssl_active, str):
                            ssl_active = ssl_active.upper() == 'ON'
                        if ssl_active:
                            try:
                                sc = ssl.create_default_context((ssl.Purpose.CLIENT_AUTH),
                                  cafile=(listener.get('cafile')),
                                  capath=(listener.get('capath')),
                                  cadata=(listener.get('cadata')))
                                sc.load_cert_chain(listener['certfile'], listener['keyfile'])
                                sc.verify_mode = ssl.CERT_OPTIONAL
                            except KeyError as ke:
                                try:
                                    raise BrokerException("'certfile' or 'keyfile' configuration parameter missing: %s" % ke)
                                finally:
                                    ke = None
                                    del ke

                            except FileNotFoundError as fnfe:
                                try:
                                    raise BrokerException("Can't read cert files '%s' or '%s' : %s" % (
                                     listener['certfile'], listener['keyfile'], fnfe))
                                finally:
                                    fnfe = None
                                    del fnfe

                        address, s_port = listener['bind'].split(':')
                        port = 0
                        try:
                            port = int(s_port)
                        except ValueError as ve:
                            try:
                                raise BrokerException('Invalid port value in bind value: %s' % listener['bind'])
                            finally:
                                ve = None
                                del ve

                        else:
                            if listener['type'] == 'tcp':
                                cb_partial = partial((self.stream_connected), listener_name=listener_name)
                                instance = yield from asyncio.start_server(cb_partial, address,
                                  port,
                                  reuse_address=True,
                                  ssl=sc,
                                  loop=(self._loop))
                                self._servers[listener_name] = Server(listener_name, instance, max_connections, self._loop)
                            else:
                                if listener['type'] == 'ws':
                                    cb_partial = partial((self.ws_connected), listener_name=listener_name)
                                    instance = yield from websockets.serve(cb_partial, address, port, ssl=sc, loop=(self._loop), subprotocols=[
                                     'mqtt'])
                                    self._servers[listener_name] = Server(listener_name, instance, max_connections, self._loop)
                                self.logger.info("Listener '%s' bind to %s (max_connections=%d)" % (
                                 listener_name, listener['bind'], max_connections))
            else:
                self.transitions.starting_success()
                (yield from self.plugins_manager.fire_event(EVENT_BROKER_POST_START))
                self._broadcast_task = asyncio.ensure_future((self._broadcast_loop()), loop=(self._loop))
                self.logger.debug('Broker started')

        except Exception as e:
            try:
                self.logger.error('Broker startup failed: %s' % e)
                self.transitions.starting_fail()
                raise BrokerException("Broker instance can't be started: %s" % e)
            finally:
                e = None
                del e

        if False:
            yield None

    @asyncio.coroutine
    def shutdown(self):
        """
            Stop broker instance.

            Closes all connected session, stop listening on network socket and free resources.
        """
        try:
            self._sessions = dict()
            self._subscriptions = dict()
            self._retained_messages = dict()
            self.transitions.shutdown()
        except (MachineError, ValueError) as exc:
            try:
                self.logger.debug('Invalid method call at this moment: %s' % exc)
                raise BrokerException("Broker instance can't be stopped: %s" % exc)
            finally:
                exc = None
                del exc

        else:
            (yield from self.plugins_manager.fire_event(EVENT_BROKER_PRE_SHUTDOWN))
            if self._broadcast_task:
                self._broadcast_task.cancel()
            if self._broadcast_queue.qsize() > 0:
                self.logger.warning('%d messages not broadcasted' % self._broadcast_queue.qsize())
            for listener_name in self._servers:
                server = self._servers[listener_name]
                (yield from server.close_instance())
            else:
                self.logger.debug('Broker closing')
                self.logger.info('Broker closed')
                (yield from self.plugins_manager.fire_event(EVENT_BROKER_POST_SHUTDOWN))
                self.transitions.stopping_success()

        if False:
            yield None

    @asyncio.coroutine
    def internal_message_broadcast(self, topic, data, qos=None):
        return (yield from self._broadcast_message(None, topic, data))
        if False:
            yield None

    @asyncio.coroutine
    def ws_connected(self, websocket, uri, listener_name):
        (yield from self.client_connected(listener_name, WebSocketsReader(websocket), WebSocketsWriter(websocket)))
        if False:
            yield None

    @asyncio.coroutine
    def stream_connected(self, reader, writer, listener_name):
        (yield from self.client_connected(listener_name, StreamReaderAdapter(reader), StreamWriterAdapter(writer)))
        if False:
            yield None

    @asyncio.coroutine
    def client_connected--- This code section failed: ---

 L. 349         0  LOAD_FAST                'self'
                2  LOAD_ATTR                _servers
                4  LOAD_METHOD              get
                6  LOAD_FAST                'listener_name'
                8  LOAD_CONST               None
               10  CALL_METHOD_2         2  ''
               12  STORE_FAST               'server'

 L. 350        14  LOAD_FAST                'server'
               16  POP_JUMP_IF_TRUE     30  'to 30'

 L. 351        18  LOAD_GLOBAL              BrokerException
               20  LOAD_STR                 "Invalid listener name '%s'"
               22  LOAD_FAST                'listener_name'
               24  BINARY_MODULO    
               26  CALL_FUNCTION_1       1  ''
               28  RAISE_VARARGS_1       1  'exception instance'
             30_0  COME_FROM            16  '16'

 L. 352        30  LOAD_FAST                'server'
               32  LOAD_METHOD              acquire_connection
               34  CALL_METHOD_0         0  ''
               36  GET_YIELD_FROM_ITER
               38  LOAD_CONST               None
               40  YIELD_FROM       
               42  POP_TOP          

 L. 354        44  LOAD_FAST                'writer'
               46  LOAD_METHOD              get_peer_info
               48  CALL_METHOD_0         0  ''
               50  UNPACK_SEQUENCE_2     2 
               52  STORE_FAST               'remote_address'
               54  STORE_FAST               'remote_port'

 L. 355        56  LOAD_FAST                'self'
               58  LOAD_ATTR                logger
               60  LOAD_METHOD              info
               62  LOAD_STR                 "Connection from %s:%d on listener '%s'"
               64  LOAD_FAST                'remote_address'
               66  LOAD_FAST                'remote_port'
               68  LOAD_FAST                'listener_name'
               70  BUILD_TUPLE_3         3 
               72  BINARY_MODULO    
               74  CALL_METHOD_1         1  ''
               76  POP_TOP          

 L. 358        78  SETUP_FINALLY       116  'to 116'

 L. 359        80  LOAD_GLOBAL              BrokerProtocolHandler
               82  LOAD_ATTR                init_from_connect
               84  LOAD_FAST                'reader'
               86  LOAD_FAST                'writer'
               88  LOAD_FAST                'self'
               90  LOAD_ATTR                plugins_manager
               92  LOAD_FAST                'self'
               94  LOAD_ATTR                _loop
               96  LOAD_CONST               ('loop',)
               98  CALL_FUNCTION_KW_4     4  '4 total positional and keyword args'
              100  GET_YIELD_FROM_ITER
              102  LOAD_CONST               None
              104  YIELD_FROM       
              106  UNPACK_SEQUENCE_2     2 
              108  STORE_FAST               'handler'
              110  STORE_FAST               'client_session'
              112  POP_BLOCK        
              114  JUMP_FORWARD        290  'to 290'
            116_0  COME_FROM_FINALLY    78  '78'

 L. 360       116  DUP_TOP          
              118  LOAD_GLOBAL              HBMQTTException
              120  COMPARE_OP               exception-match
              122  POP_JUMP_IF_FALSE   194  'to 194'
              124  POP_TOP          
              126  STORE_FAST               'exc'
              128  POP_TOP          
              130  SETUP_FINALLY       182  'to 182'

 L. 361       132  LOAD_FAST                'self'
              134  LOAD_ATTR                logger
              136  LOAD_METHOD              warning
              138  LOAD_STR                 "[MQTT-3.1.0-1] %s: Can't read first packet an CONNECT: %s"

 L. 362       140  LOAD_GLOBAL              format_client_message
              142  LOAD_FAST                'remote_address'
              144  LOAD_FAST                'remote_port'
              146  LOAD_CONST               ('address', 'port')
              148  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              150  LOAD_FAST                'exc'
              152  BUILD_TUPLE_2         2 

 L. 361       154  BINARY_MODULO    
              156  CALL_METHOD_1         1  ''
              158  POP_TOP          

 L. 364       160  LOAD_FAST                'self'
              162  LOAD_ATTR                logger
              164  LOAD_METHOD              debug
              166  LOAD_STR                 'Connection closed'
              168  CALL_METHOD_1         1  ''
              170  POP_TOP          

 L. 365       172  POP_BLOCK        
              174  POP_EXCEPT       
              176  CALL_FINALLY        182  'to 182'
              178  LOAD_CONST               None
              180  RETURN_VALUE     
            182_0  COME_FROM           176  '176'
            182_1  COME_FROM_FINALLY   130  '130'
              182  LOAD_CONST               None
              184  STORE_FAST               'exc'
              186  DELETE_FAST              'exc'
              188  END_FINALLY      
              190  POP_EXCEPT       
              192  JUMP_FORWARD        290  'to 290'
            194_0  COME_FROM           122  '122'

 L. 366       194  DUP_TOP          
              196  LOAD_GLOBAL              MQTTException
              198  COMPARE_OP               exception-match
          200_202  POP_JUMP_IF_FALSE   288  'to 288'
              204  POP_TOP          
              206  STORE_FAST               'me'
              208  POP_TOP          
              210  SETUP_FINALLY       276  'to 276'

 L. 367       212  LOAD_FAST                'self'
              214  LOAD_ATTR                logger
              216  LOAD_METHOD              error
              218  LOAD_STR                 'Invalid connection from %s : %s'

 L. 368       220  LOAD_GLOBAL              format_client_message
              222  LOAD_FAST                'remote_address'
              224  LOAD_FAST                'remote_port'
              226  LOAD_CONST               ('address', 'port')
              228  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              230  LOAD_FAST                'me'
              232  BUILD_TUPLE_2         2 

 L. 367       234  BINARY_MODULO    
              236  CALL_METHOD_1         1  ''
              238  POP_TOP          

 L. 369       240  LOAD_FAST                'writer'
              242  LOAD_METHOD              close
              244  CALL_METHOD_0         0  ''
              246  GET_YIELD_FROM_ITER
              248  LOAD_CONST               None
              250  YIELD_FROM       
              252  POP_TOP          

 L. 370       254  LOAD_FAST                'self'
              256  LOAD_ATTR                logger
              258  LOAD_METHOD              debug
              260  LOAD_STR                 'Connection closed'
              262  CALL_METHOD_1         1  ''
              264  POP_TOP          

 L. 371       266  POP_BLOCK        
              268  POP_EXCEPT       
              270  CALL_FINALLY        276  'to 276'
              272  LOAD_CONST               None
              274  RETURN_VALUE     
            276_0  COME_FROM           270  '270'
            276_1  COME_FROM_FINALLY   210  '210'
              276  LOAD_CONST               None
              278  STORE_FAST               'me'
              280  DELETE_FAST              'me'
              282  END_FINALLY      
              284  POP_EXCEPT       
              286  JUMP_FORWARD        290  'to 290'
            288_0  COME_FROM           200  '200'
              288  END_FINALLY      
            290_0  COME_FROM           286  '286'
            290_1  COME_FROM           192  '192'
            290_2  COME_FROM           114  '114'

 L. 373       290  LOAD_FAST                'client_session'
              292  LOAD_ATTR                clean_session
          294_296  POP_JUMP_IF_FALSE   352  'to 352'

 L. 375       298  LOAD_FAST                'client_session'
              300  LOAD_ATTR                client_id
              302  LOAD_CONST               None
              304  COMPARE_OP               is-not
          306_308  POP_JUMP_IF_FALSE   336  'to 336'
              310  LOAD_FAST                'client_session'
              312  LOAD_ATTR                client_id
              314  LOAD_STR                 ''
              316  COMPARE_OP               !=
          318_320  POP_JUMP_IF_FALSE   336  'to 336'

 L. 376       322  LOAD_FAST                'self'
              324  LOAD_METHOD              delete_session
              326  LOAD_FAST                'client_session'
              328  LOAD_ATTR                client_id
              330  CALL_METHOD_1         1  ''
              332  POP_TOP          
              334  JUMP_FORWARD        344  'to 344'
            336_0  COME_FROM           318  '318'
            336_1  COME_FROM           306  '306'

 L. 378       336  LOAD_GLOBAL              gen_client_id
              338  CALL_FUNCTION_0       0  ''
              340  LOAD_FAST                'client_session'
              342  STORE_ATTR               client_id
            344_0  COME_FROM           334  '334'

 L. 379       344  LOAD_CONST               0
              346  LOAD_FAST                'client_session'
              348  STORE_ATTR               parent
              350  JUMP_FORWARD        424  'to 424'
            352_0  COME_FROM           294  '294'

 L. 382       352  LOAD_FAST                'client_session'
              354  LOAD_ATTR                client_id
              356  LOAD_FAST                'self'
              358  LOAD_ATTR                _sessions
              360  COMPARE_OP               in
          362_364  POP_JUMP_IF_FALSE   418  'to 418'

 L. 383       366  LOAD_FAST                'self'
              368  LOAD_ATTR                logger
              370  LOAD_METHOD              debug
              372  LOAD_STR                 'Found old session %s'
              374  LOAD_GLOBAL              repr
              376  LOAD_FAST                'self'
              378  LOAD_ATTR                _sessions
              380  LOAD_FAST                'client_session'
              382  LOAD_ATTR                client_id
              384  BINARY_SUBSCR    
              386  CALL_FUNCTION_1       1  ''
              388  BINARY_MODULO    
              390  CALL_METHOD_1         1  ''
              392  POP_TOP          

 L. 384       394  LOAD_FAST                'self'
              396  LOAD_ATTR                _sessions
              398  LOAD_FAST                'client_session'
              400  LOAD_ATTR                client_id
              402  BINARY_SUBSCR    
              404  UNPACK_SEQUENCE_2     2 
              406  STORE_FAST               'client_session'
              408  STORE_FAST               'h'

 L. 385       410  LOAD_CONST               1
              412  LOAD_FAST                'client_session'
              414  STORE_ATTR               parent
              416  JUMP_FORWARD        424  'to 424'
            418_0  COME_FROM           362  '362'

 L. 387       418  LOAD_CONST               0
              420  LOAD_FAST                'client_session'
              422  STORE_ATTR               parent
            424_0  COME_FROM           416  '416'
            424_1  COME_FROM           350  '350'

 L. 388       424  LOAD_FAST                'client_session'
              426  LOAD_ATTR                keep_alive
              428  LOAD_CONST               0
              430  COMPARE_OP               >
          432_434  POP_JUMP_IF_FALSE   456  'to 456'

 L. 389       436  LOAD_FAST                'client_session'
              438  DUP_TOP          
              440  LOAD_ATTR                keep_alive
              442  LOAD_FAST                'self'
              444  LOAD_ATTR                config
              446  LOAD_STR                 'timeout-disconnect-delay'
              448  BINARY_SUBSCR    
              450  INPLACE_ADD      
              452  ROT_TWO          
              454  STORE_ATTR               keep_alive
            456_0  COME_FROM           432  '432'

 L. 390       456  LOAD_FAST                'self'
              458  LOAD_ATTR                logger
              460  LOAD_METHOD              debug
              462  LOAD_STR                 'Keep-alive timeout=%d'
              464  LOAD_FAST                'client_session'
              466  LOAD_ATTR                keep_alive
              468  BINARY_MODULO    
              470  CALL_METHOD_1         1  ''
              472  POP_TOP          

 L. 392       474  LOAD_FAST                'handler'
              476  LOAD_METHOD              attach
              478  LOAD_FAST                'client_session'
              480  LOAD_FAST                'reader'
              482  LOAD_FAST                'writer'
              484  CALL_METHOD_3         3  ''
              486  POP_TOP          

 L. 393       488  LOAD_FAST                'client_session'
              490  LOAD_FAST                'handler'
              492  BUILD_TUPLE_2         2 
              494  LOAD_FAST                'self'
              496  LOAD_ATTR                _sessions
              498  LOAD_FAST                'client_session'
              500  LOAD_ATTR                client_id
              502  STORE_SUBSCR     

 L. 395       504  LOAD_FAST                'self'
              506  LOAD_METHOD              authenticate
              508  LOAD_FAST                'client_session'
              510  LOAD_FAST                'self'
              512  LOAD_ATTR                listeners_config
              514  LOAD_FAST                'listener_name'
              516  BINARY_SUBSCR    
              518  CALL_METHOD_2         2  ''
              520  GET_YIELD_FROM_ITER
              522  LOAD_CONST               None
              524  YIELD_FROM       
              526  STORE_FAST               'authenticated'

 L. 396       528  LOAD_FAST                'authenticated'
          530_532  POP_JUMP_IF_TRUE    560  'to 560'

 L. 397       534  LOAD_FAST                'writer'
              536  LOAD_METHOD              close
              538  CALL_METHOD_0         0  ''
              540  GET_YIELD_FROM_ITER
              542  LOAD_CONST               None
              544  YIELD_FROM       
              546  POP_TOP          

 L. 398       548  LOAD_FAST                'server'
              550  LOAD_METHOD              release_connection
              552  CALL_METHOD_0         0  ''
              554  POP_TOP          

 L. 399       556  LOAD_CONST               None
              558  RETURN_VALUE     
            560_0  COME_FROM           530  '530'

 L. 402       560  SETUP_FINALLY       582  'to 582'

 L. 403       562  LOAD_FAST                'client_session'
              564  LOAD_ATTR                transitions
              566  LOAD_METHOD              connect
              568  CALL_METHOD_0         0  ''
              570  POP_TOP          

 L. 404       572  POP_BLOCK        
          574_576  BREAK_LOOP          652  'to 652'
              578  POP_BLOCK        
              580  JUMP_BACK           560  'to 560'
            582_0  COME_FROM_FINALLY   560  '560'

 L. 405       582  DUP_TOP          
              584  LOAD_GLOBAL              MachineError
              586  LOAD_GLOBAL              ValueError
              588  BUILD_TUPLE_2         2 
              590  COMPARE_OP               exception-match
          592_594  POP_JUMP_IF_FALSE   646  'to 646'
              596  POP_TOP          
              598  POP_TOP          
              600  POP_TOP          

 L. 407       602  LOAD_FAST                'self'
              604  LOAD_ATTR                logger
              606  LOAD_METHOD              warning
              608  LOAD_STR                 'Client %s is reconnecting too quickly, make it wait'
              610  LOAD_FAST                'client_session'
              612  LOAD_ATTR                client_id
              614  BINARY_MODULO    
              616  CALL_METHOD_1         1  ''
              618  POP_TOP          

 L. 409       620  LOAD_GLOBAL              asyncio
              622  LOAD_ATTR                sleep
              624  LOAD_CONST               1
              626  LOAD_FAST                'self'
              628  LOAD_ATTR                _loop
              630  LOAD_CONST               ('loop',)
              632  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              634  GET_YIELD_FROM_ITER
              636  LOAD_CONST               None
              638  YIELD_FROM       
              640  POP_TOP          
              642  POP_EXCEPT       
              644  JUMP_BACK           560  'to 560'
            646_0  COME_FROM           592  '592'
              646  END_FINALLY      
          648_650  JUMP_BACK           560  'to 560'

 L. 410       652  LOAD_FAST                'handler'
              654  LOAD_METHOD              mqtt_connack_authorize
              656  LOAD_FAST                'authenticated'
              658  CALL_METHOD_1         1  ''
              660  GET_YIELD_FROM_ITER
              662  LOAD_CONST               None
              664  YIELD_FROM       
              666  POP_TOP          

 L. 412       668  LOAD_FAST                'self'
              670  LOAD_ATTR                plugins_manager
              672  LOAD_ATTR                fire_event
              674  LOAD_GLOBAL              EVENT_BROKER_CLIENT_CONNECTED
              676  LOAD_FAST                'client_session'
              678  LOAD_ATTR                client_id
              680  LOAD_CONST               ('client_id',)
              682  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              684  GET_YIELD_FROM_ITER
              686  LOAD_CONST               None
              688  YIELD_FROM       
              690  POP_TOP          

 L. 414       692  LOAD_FAST                'self'
              694  LOAD_ATTR                logger
              696  LOAD_METHOD              debug
              698  LOAD_STR                 '%s Start messages handling'
              700  LOAD_FAST                'client_session'
              702  LOAD_ATTR                client_id
              704  BINARY_MODULO    
              706  CALL_METHOD_1         1  ''
              708  POP_TOP          

 L. 415       710  LOAD_FAST                'handler'
              712  LOAD_METHOD              start
              714  CALL_METHOD_0         0  ''
              716  GET_YIELD_FROM_ITER
              718  LOAD_CONST               None
              720  YIELD_FROM       
              722  POP_TOP          

 L. 416       724  LOAD_FAST                'self'
              726  LOAD_ATTR                logger
              728  LOAD_METHOD              debug
              730  LOAD_STR                 'Retained messages queue size: %d'
              732  LOAD_FAST                'client_session'
              734  LOAD_ATTR                retained_messages
              736  LOAD_METHOD              qsize
              738  CALL_METHOD_0         0  ''
              740  BINARY_MODULO    
              742  CALL_METHOD_1         1  ''
              744  POP_TOP          

 L. 417       746  LOAD_FAST                'self'
              748  LOAD_METHOD              publish_session_retained_messages
              750  LOAD_FAST                'client_session'
              752  CALL_METHOD_1         1  ''
              754  GET_YIELD_FROM_ITER
              756  LOAD_CONST               None
              758  YIELD_FROM       
              760  POP_TOP          

 L. 420       762  LOAD_GLOBAL              asyncio
              764  LOAD_ATTR                ensure_future
              766  LOAD_FAST                'handler'
              768  LOAD_METHOD              wait_disconnect
              770  CALL_METHOD_0         0  ''
              772  LOAD_FAST                'self'
              774  LOAD_ATTR                _loop
              776  LOAD_CONST               ('loop',)
              778  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              780  STORE_FAST               'disconnect_waiter'

 L. 421       782  LOAD_GLOBAL              asyncio
              784  LOAD_ATTR                ensure_future
              786  LOAD_FAST                'handler'
              788  LOAD_METHOD              get_next_pending_subscription
              790  CALL_METHOD_0         0  ''
              792  LOAD_FAST                'self'
              794  LOAD_ATTR                _loop
              796  LOAD_CONST               ('loop',)
              798  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              800  STORE_FAST               'subscribe_waiter'

 L. 422       802  LOAD_GLOBAL              asyncio
              804  LOAD_ATTR                ensure_future
              806  LOAD_FAST                'handler'
              808  LOAD_METHOD              get_next_pending_unsubscription
              810  CALL_METHOD_0         0  ''
              812  LOAD_FAST                'self'
              814  LOAD_ATTR                _loop
              816  LOAD_CONST               ('loop',)
              818  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              820  STORE_FAST               'unsubscribe_waiter'

 L. 423       822  LOAD_GLOBAL              asyncio
              824  LOAD_ATTR                ensure_future
              826  LOAD_FAST                'handler'
              828  LOAD_METHOD              mqtt_deliver_next_message
              830  CALL_METHOD_0         0  ''
              832  LOAD_FAST                'self'
              834  LOAD_ATTR                _loop
              836  LOAD_CONST               ('loop',)
              838  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              840  STORE_FAST               'wait_deliver'

 L. 424       842  LOAD_CONST               True
              844  STORE_FAST               'connected'

 L. 425       846  LOAD_FAST                'connected'
          848_850  POP_JUMP_IF_FALSE  1770  'to 1770'

 L. 426   852_854  SETUP_FINALLY      1724  'to 1724'

 L. 427       856  LOAD_GLOBAL              asyncio
              858  LOAD_ATTR                wait

 L. 428       860  LOAD_FAST                'disconnect_waiter'
              862  LOAD_FAST                'subscribe_waiter'
              864  LOAD_FAST                'unsubscribe_waiter'
              866  LOAD_FAST                'wait_deliver'
              868  BUILD_LIST_4          4 

 L. 429       870  LOAD_GLOBAL              asyncio
              872  LOAD_ATTR                FIRST_COMPLETED

 L. 429       874  LOAD_FAST                'self'
              876  LOAD_ATTR                _loop

 L. 427       878  LOAD_CONST               ('return_when', 'loop')
              880  CALL_FUNCTION_KW_3     3  '3 total positional and keyword args'
              882  GET_YIELD_FROM_ITER
              884  LOAD_CONST               None
              886  YIELD_FROM       
              888  UNPACK_SEQUENCE_2     2 
              890  STORE_FAST               'done'
              892  STORE_FAST               'pending'

 L. 430       894  LOAD_FAST                'disconnect_waiter'
              896  LOAD_FAST                'done'
              898  COMPARE_OP               in
          900_902  POP_JUMP_IF_FALSE  1120  'to 1120'

 L. 431       904  LOAD_FAST                'disconnect_waiter'
              906  LOAD_METHOD              result
              908  CALL_METHOD_0         0  ''
              910  STORE_FAST               'result'

 L. 432       912  LOAD_FAST                'self'
              914  LOAD_ATTR                logger
              916  LOAD_METHOD              debug
              918  LOAD_STR                 '%s Result from wait_diconnect: %s'
              920  LOAD_FAST                'client_session'
              922  LOAD_ATTR                client_id
              924  LOAD_FAST                'result'
              926  BUILD_TUPLE_2         2 
              928  BINARY_MODULO    
              930  CALL_METHOD_1         1  ''
              932  POP_TOP          

 L. 433       934  LOAD_FAST                'result'
              936  LOAD_CONST               None
              938  COMPARE_OP               is
          940_942  POP_JUMP_IF_FALSE  1048  'to 1048'

 L. 434       944  LOAD_FAST                'self'
              946  LOAD_ATTR                logger
              948  LOAD_METHOD              debug
              950  LOAD_STR                 'Will flag: %s'
              952  LOAD_FAST                'client_session'
              954  LOAD_ATTR                will_flag
              956  BINARY_MODULO    
              958  CALL_METHOD_1         1  ''
              960  POP_TOP          

 L. 436       962  LOAD_FAST                'client_session'
              964  LOAD_ATTR                will_flag
          966_968  POP_JUMP_IF_FALSE  1048  'to 1048'

 L. 437       970  LOAD_FAST                'self'
              972  LOAD_ATTR                logger
              974  LOAD_METHOD              debug
              976  LOAD_STR                 'Client %s disconnected abnormally, sending will message'

 L. 438       978  LOAD_GLOBAL              format_client_message
              980  LOAD_FAST                'client_session'
              982  CALL_FUNCTION_1       1  ''

 L. 437       984  BINARY_MODULO    
              986  CALL_METHOD_1         1  ''
              988  POP_TOP          

 L. 439       990  LOAD_FAST                'self'
              992  LOAD_METHOD              _broadcast_message

 L. 440       994  LOAD_FAST                'client_session'

 L. 441       996  LOAD_FAST                'client_session'
              998  LOAD_ATTR                will_topic

 L. 442      1000  LOAD_FAST                'client_session'
             1002  LOAD_ATTR                will_message

 L. 443      1004  LOAD_FAST                'client_session'
             1006  LOAD_ATTR                will_qos

 L. 439      1008  CALL_METHOD_4         4  ''
             1010  GET_YIELD_FROM_ITER
             1012  LOAD_CONST               None
             1014  YIELD_FROM       
             1016  POP_TOP          

 L. 444      1018  LOAD_FAST                'client_session'
             1020  LOAD_ATTR                will_retain
         1022_1024  POP_JUMP_IF_FALSE  1048  'to 1048'

 L. 445      1026  LOAD_FAST                'self'
             1028  LOAD_METHOD              retain_message
             1030  LOAD_FAST                'client_session'

 L. 446      1032  LOAD_FAST                'client_session'
             1034  LOAD_ATTR                will_topic

 L. 447      1036  LOAD_FAST                'client_session'
             1038  LOAD_ATTR                will_message

 L. 448      1040  LOAD_FAST                'client_session'
             1042  LOAD_ATTR                will_qos

 L. 445      1044  CALL_METHOD_4         4  ''
             1046  POP_TOP          
           1048_0  COME_FROM          1022  '1022'
           1048_1  COME_FROM           966  '966'
           1048_2  COME_FROM           940  '940'

 L. 449      1048  LOAD_FAST                'self'
             1050  LOAD_ATTR                logger
             1052  LOAD_METHOD              debug
             1054  LOAD_STR                 '%s Disconnecting session'
             1056  LOAD_FAST                'client_session'
             1058  LOAD_ATTR                client_id
             1060  BINARY_MODULO    
             1062  CALL_METHOD_1         1  ''
             1064  POP_TOP          

 L. 450      1066  LOAD_FAST                'self'
             1068  LOAD_METHOD              _stop_handler
             1070  LOAD_FAST                'handler'
             1072  CALL_METHOD_1         1  ''
             1074  GET_YIELD_FROM_ITER
             1076  LOAD_CONST               None
             1078  YIELD_FROM       
             1080  POP_TOP          

 L. 451      1082  LOAD_FAST                'client_session'
             1084  LOAD_ATTR                transitions
             1086  LOAD_METHOD              disconnect
             1088  CALL_METHOD_0         0  ''
             1090  POP_TOP          

 L. 452      1092  LOAD_FAST                'self'
             1094  LOAD_ATTR                plugins_manager
             1096  LOAD_ATTR                fire_event
             1098  LOAD_GLOBAL              EVENT_BROKER_CLIENT_DISCONNECTED
             1100  LOAD_FAST                'client_session'
             1102  LOAD_ATTR                client_id
             1104  LOAD_CONST               ('client_id',)
             1106  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
             1108  GET_YIELD_FROM_ITER
             1110  LOAD_CONST               None
             1112  YIELD_FROM       
             1114  POP_TOP          

 L. 453      1116  LOAD_CONST               False
             1118  STORE_FAST               'connected'
           1120_0  COME_FROM           900  '900'

 L. 454      1120  LOAD_FAST                'unsubscribe_waiter'
             1122  LOAD_FAST                'done'
             1124  COMPARE_OP               in
         1126_1128  POP_JUMP_IF_FALSE  1250  'to 1250'

 L. 455      1130  LOAD_FAST                'self'
             1132  LOAD_ATTR                logger
             1134  LOAD_METHOD              debug
             1136  LOAD_STR                 '%s handling unsubscription'
             1138  LOAD_FAST                'client_session'
             1140  LOAD_ATTR                client_id
             1142  BINARY_MODULO    
             1144  CALL_METHOD_1         1  ''
             1146  POP_TOP          

 L. 456      1148  LOAD_FAST                'unsubscribe_waiter'
             1150  LOAD_METHOD              result
             1152  CALL_METHOD_0         0  ''
             1154  STORE_FAST               'unsubscription'

 L. 457      1156  LOAD_FAST                'unsubscription'
             1158  LOAD_STR                 'topics'
             1160  BINARY_SUBSCR    
             1162  GET_ITER         
             1164  FOR_ITER           1210  'to 1210'
             1166  STORE_FAST               'topic'

 L. 458      1168  LOAD_FAST                'self'
             1170  LOAD_METHOD              _del_subscription
             1172  LOAD_FAST                'topic'
             1174  LOAD_FAST                'client_session'
             1176  CALL_METHOD_2         2  ''
             1178  POP_TOP          

 L. 459      1180  LOAD_FAST                'self'
             1182  LOAD_ATTR                plugins_manager
             1184  LOAD_ATTR                fire_event

 L. 460      1186  LOAD_GLOBAL              EVENT_BROKER_CLIENT_UNSUBSCRIBED

 L. 461      1188  LOAD_FAST                'client_session'
             1190  LOAD_ATTR                client_id

 L. 462      1192  LOAD_FAST                'topic'

 L. 459      1194  LOAD_CONST               ('client_id', 'topic')
             1196  CALL_FUNCTION_KW_3     3  '3 total positional and keyword args'
             1198  GET_YIELD_FROM_ITER
             1200  LOAD_CONST               None
             1202  YIELD_FROM       
             1204  POP_TOP          
         1206_1208  JUMP_BACK          1164  'to 1164'

 L. 463      1210  LOAD_FAST                'handler'
             1212  LOAD_METHOD              mqtt_acknowledge_unsubscription
             1214  LOAD_FAST                'unsubscription'
             1216  LOAD_STR                 'packet_id'
             1218  BINARY_SUBSCR    
             1220  CALL_METHOD_1         1  ''
             1222  GET_YIELD_FROM_ITER
             1224  LOAD_CONST               None
             1226  YIELD_FROM       
             1228  POP_TOP          

 L. 464      1230  LOAD_GLOBAL              asyncio
             1232  LOAD_ATTR                Task
             1234  LOAD_FAST                'handler'
             1236  LOAD_METHOD              get_next_pending_unsubscription
             1238  CALL_METHOD_0         0  ''
             1240  LOAD_FAST                'self'
             1242  LOAD_ATTR                _loop
             1244  LOAD_CONST               ('loop',)
             1246  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
             1248  STORE_FAST               'unsubscribe_waiter'
           1250_0  COME_FROM          1126  '1126'

 L. 465      1250  LOAD_FAST                'subscribe_waiter'
             1252  LOAD_FAST                'done'
             1254  COMPARE_OP               in
         1256_1258  POP_JUMP_IF_FALSE  1486  'to 1486'

 L. 466      1260  LOAD_FAST                'self'
             1262  LOAD_ATTR                logger
             1264  LOAD_METHOD              debug
             1266  LOAD_STR                 '%s handling subscription'
             1268  LOAD_FAST                'client_session'
             1270  LOAD_ATTR                client_id
             1272  BINARY_MODULO    
             1274  CALL_METHOD_1         1  ''
             1276  POP_TOP          

 L. 467      1278  LOAD_FAST                'subscribe_waiter'
             1280  LOAD_METHOD              result
             1282  CALL_METHOD_0         0  ''
             1284  STORE_FAST               'subscriptions'

 L. 468      1286  BUILD_LIST_0          0 
             1288  STORE_FAST               'return_codes'

 L. 469      1290  LOAD_FAST                'subscriptions'
             1292  LOAD_STR                 'topics'
             1294  BINARY_SUBSCR    
             1296  GET_ITER         
             1298  FOR_ITER           1334  'to 1334'
             1300  STORE_FAST               'subscription'

 L. 470      1302  LOAD_FAST                'self'
             1304  LOAD_METHOD              add_subscription
             1306  LOAD_FAST                'subscription'
             1308  LOAD_FAST                'client_session'
             1310  CALL_METHOD_2         2  ''
             1312  GET_YIELD_FROM_ITER
             1314  LOAD_CONST               None
             1316  YIELD_FROM       
             1318  STORE_FAST               'result'

 L. 471      1320  LOAD_FAST                'return_codes'
             1322  LOAD_METHOD              append
             1324  LOAD_FAST                'result'
             1326  CALL_METHOD_1         1  ''
             1328  POP_TOP          
         1330_1332  JUMP_BACK          1298  'to 1298'

 L. 472      1334  LOAD_FAST                'handler'
             1336  LOAD_METHOD              mqtt_acknowledge_subscription
             1338  LOAD_FAST                'subscriptions'
             1340  LOAD_STR                 'packet_id'
             1342  BINARY_SUBSCR    
             1344  LOAD_FAST                'return_codes'
             1346  CALL_METHOD_2         2  ''
             1348  GET_YIELD_FROM_ITER
             1350  LOAD_CONST               None
             1352  YIELD_FROM       
             1354  POP_TOP          

 L. 473      1356  LOAD_GLOBAL              enumerate
             1358  LOAD_FAST                'subscriptions'
             1360  LOAD_STR                 'topics'
             1362  BINARY_SUBSCR    
             1364  CALL_FUNCTION_1       1  ''
             1366  GET_ITER         
           1368_0  COME_FROM          1386  '1386'
             1368  FOR_ITER           1448  'to 1448'
             1370  UNPACK_SEQUENCE_2     2 
             1372  STORE_FAST               'index'
             1374  STORE_FAST               'subscription'

 L. 474      1376  LOAD_FAST                'return_codes'
             1378  LOAD_FAST                'index'
             1380  BINARY_SUBSCR    
             1382  LOAD_CONST               128
             1384  COMPARE_OP               !=
         1386_1388  POP_JUMP_IF_FALSE  1368  'to 1368'

 L. 475      1390  LOAD_FAST                'self'
             1392  LOAD_ATTR                plugins_manager
             1394  LOAD_ATTR                fire_event

 L. 476      1396  LOAD_GLOBAL              EVENT_BROKER_CLIENT_SUBSCRIBED

 L. 477      1398  LOAD_FAST                'client_session'
             1400  LOAD_ATTR                client_id

 L. 478      1402  LOAD_FAST                'subscription'
             1404  LOAD_CONST               0
             1406  BINARY_SUBSCR    

 L. 479      1408  LOAD_FAST                'subscription'
             1410  LOAD_CONST               1
             1412  BINARY_SUBSCR    

 L. 475      1414  LOAD_CONST               ('client_id', 'topic', 'qos')
             1416  CALL_FUNCTION_KW_4     4  '4 total positional and keyword args'
             1418  GET_YIELD_FROM_ITER
             1420  LOAD_CONST               None
             1422  YIELD_FROM       
             1424  POP_TOP          

 L. 480      1426  LOAD_FAST                'self'
             1428  LOAD_METHOD              publish_retained_messages_for_subscription
             1430  LOAD_FAST                'subscription'
             1432  LOAD_FAST                'client_session'
             1434  CALL_METHOD_2         2  ''
             1436  GET_YIELD_FROM_ITER
             1438  LOAD_CONST               None
             1440  YIELD_FROM       
             1442  POP_TOP          
         1444_1446  JUMP_BACK          1368  'to 1368'

 L. 481      1448  LOAD_GLOBAL              asyncio
             1450  LOAD_ATTR                Task
             1452  LOAD_FAST                'handler'
             1454  LOAD_METHOD              get_next_pending_subscription
             1456  CALL_METHOD_0         0  ''
             1458  LOAD_FAST                'self'
             1460  LOAD_ATTR                _loop
             1462  LOAD_CONST               ('loop',)
             1464  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
             1466  STORE_FAST               'subscribe_waiter'

 L. 482      1468  LOAD_FAST                'self'
             1470  LOAD_ATTR                logger
             1472  LOAD_METHOD              debug
             1474  LOAD_GLOBAL              repr
             1476  LOAD_FAST                'self'
             1478  LOAD_ATTR                _subscriptions
             1480  CALL_FUNCTION_1       1  ''
             1482  CALL_METHOD_1         1  ''
             1484  POP_TOP          
           1486_0  COME_FROM          1256  '1256'

 L. 483      1486  LOAD_FAST                'wait_deliver'
             1488  LOAD_FAST                'done'
             1490  COMPARE_OP               in
         1492_1494  POP_JUMP_IF_FALSE  1720  'to 1720'

 L. 484      1496  LOAD_FAST                'self'
             1498  LOAD_ATTR                logger
             1500  LOAD_METHOD              isEnabledFor
             1502  LOAD_GLOBAL              logging
             1504  LOAD_ATTR                DEBUG
             1506  CALL_METHOD_1         1  ''
         1508_1510  POP_JUMP_IF_FALSE  1530  'to 1530'

 L. 485      1512  LOAD_FAST                'self'
             1514  LOAD_ATTR                logger
             1516  LOAD_METHOD              debug
             1518  LOAD_STR                 '%s handling message delivery'
             1520  LOAD_FAST                'client_session'
             1522  LOAD_ATTR                client_id
             1524  BINARY_MODULO    
             1526  CALL_METHOD_1         1  ''
             1528  POP_TOP          
           1530_0  COME_FROM          1508  '1508'

 L. 486      1530  LOAD_FAST                'wait_deliver'
             1532  LOAD_METHOD              result
             1534  CALL_METHOD_0         0  ''
             1536  STORE_FAST               'app_message'

 L. 487      1538  LOAD_FAST                'app_message'
             1540  LOAD_ATTR                topic
         1542_1544  POP_JUMP_IF_TRUE   1570  'to 1570'

 L. 488      1546  LOAD_FAST                'self'
             1548  LOAD_ATTR                logger
             1550  LOAD_METHOD              warning
             1552  LOAD_STR                 '[MQTT-4.7.3-1] - %s invalid TOPIC sent in PUBLISH message, closing connection'
             1554  LOAD_FAST                'client_session'
             1556  LOAD_ATTR                client_id
             1558  BINARY_MODULO    
             1560  CALL_METHOD_1         1  ''
             1562  POP_TOP          

 L. 489      1564  POP_BLOCK        
         1566_1568  JUMP_ABSOLUTE      1770  'to 1770'
           1570_0  COME_FROM          1542  '1542'

 L. 490      1570  LOAD_STR                 '#'
             1572  LOAD_FAST                'app_message'
             1574  LOAD_ATTR                topic
             1576  COMPARE_OP               in
         1578_1580  POP_JUMP_IF_TRUE   1594  'to 1594'
             1582  LOAD_STR                 '+'
             1584  LOAD_FAST                'app_message'
             1586  LOAD_ATTR                topic
             1588  COMPARE_OP               in
         1590_1592  POP_JUMP_IF_FALSE  1618  'to 1618'
           1594_0  COME_FROM          1578  '1578'

 L. 491      1594  LOAD_FAST                'self'
             1596  LOAD_ATTR                logger
             1598  LOAD_METHOD              warning
             1600  LOAD_STR                 '[MQTT-3.3.2-2] - %s invalid TOPIC sent in PUBLISH message, closing connection'
             1602  LOAD_FAST                'client_session'
             1604  LOAD_ATTR                client_id
             1606  BINARY_MODULO    
             1608  CALL_METHOD_1         1  ''
             1610  POP_TOP          

 L. 492      1612  POP_BLOCK        
         1614_1616  JUMP_ABSOLUTE      1770  'to 1770'
           1618_0  COME_FROM          1590  '1590'

 L. 493      1618  LOAD_FAST                'self'
             1620  LOAD_ATTR                plugins_manager
             1622  LOAD_ATTR                fire_event
             1624  LOAD_GLOBAL              EVENT_BROKER_MESSAGE_RECEIVED

 L. 494      1626  LOAD_FAST                'client_session'
             1628  LOAD_ATTR                client_id

 L. 495      1630  LOAD_FAST                'app_message'

 L. 493      1632  LOAD_CONST               ('client_id', 'message')
             1634  CALL_FUNCTION_KW_3     3  '3 total positional and keyword args'
             1636  GET_YIELD_FROM_ITER
             1638  LOAD_CONST               None
             1640  YIELD_FROM       
             1642  POP_TOP          

 L. 496      1644  LOAD_FAST                'self'
             1646  LOAD_METHOD              _broadcast_message
             1648  LOAD_FAST                'client_session'
             1650  LOAD_FAST                'app_message'
             1652  LOAD_ATTR                topic
             1654  LOAD_FAST                'app_message'
             1656  LOAD_ATTR                data
             1658  CALL_METHOD_3         3  ''
             1660  GET_YIELD_FROM_ITER
             1662  LOAD_CONST               None
             1664  YIELD_FROM       
             1666  POP_TOP          

 L. 497      1668  LOAD_FAST                'app_message'
             1670  LOAD_ATTR                publish_packet
             1672  LOAD_ATTR                retain_flag
         1674_1676  POP_JUMP_IF_FALSE  1700  'to 1700'

 L. 498      1678  LOAD_FAST                'self'
             1680  LOAD_METHOD              retain_message
             1682  LOAD_FAST                'client_session'
             1684  LOAD_FAST                'app_message'
             1686  LOAD_ATTR                topic
             1688  LOAD_FAST                'app_message'
             1690  LOAD_ATTR                data
             1692  LOAD_FAST                'app_message'
             1694  LOAD_ATTR                qos
             1696  CALL_METHOD_4         4  ''
             1698  POP_TOP          
           1700_0  COME_FROM          1674  '1674'

 L. 499      1700  LOAD_GLOBAL              asyncio
             1702  LOAD_ATTR                Task
             1704  LOAD_FAST                'handler'
             1706  LOAD_METHOD              mqtt_deliver_next_message
             1708  CALL_METHOD_0         0  ''
             1710  LOAD_FAST                'self'
             1712  LOAD_ATTR                _loop
             1714  LOAD_CONST               ('loop',)
             1716  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
             1718  STORE_FAST               'wait_deliver'
           1720_0  COME_FROM          1492  '1492'
             1720  POP_BLOCK        
             1722  JUMP_BACK           846  'to 846'
           1724_0  COME_FROM_FINALLY   852  '852'

 L. 500      1724  DUP_TOP          
             1726  LOAD_GLOBAL              asyncio
             1728  LOAD_ATTR                CancelledError
             1730  COMPARE_OP               exception-match
         1732_1734  POP_JUMP_IF_FALSE  1764  'to 1764'
             1736  POP_TOP          
             1738  POP_TOP          
             1740  POP_TOP          

 L. 501      1742  LOAD_FAST                'self'
             1744  LOAD_ATTR                logger
             1746  LOAD_METHOD              debug
             1748  LOAD_STR                 'Client loop cancelled'
             1750  CALL_METHOD_1         1  ''
             1752  POP_TOP          

 L. 502      1754  POP_EXCEPT       
         1756_1758  JUMP_ABSOLUTE      1770  'to 1770'
             1760  POP_EXCEPT       
             1762  JUMP_BACK           846  'to 846'
           1764_0  COME_FROM          1732  '1732'
             1764  END_FINALLY      
         1766_1768  JUMP_BACK           846  'to 846'
           1770_0  COME_FROM           848  '848'

 L. 503      1770  LOAD_FAST                'disconnect_waiter'
             1772  LOAD_METHOD              cancel
             1774  CALL_METHOD_0         0  ''
             1776  POP_TOP          

 L. 504      1778  LOAD_FAST                'subscribe_waiter'
             1780  LOAD_METHOD              cancel
             1782  CALL_METHOD_0         0  ''
             1784  POP_TOP          

 L. 505      1786  LOAD_FAST                'unsubscribe_waiter'
             1788  LOAD_METHOD              cancel
             1790  CALL_METHOD_0         0  ''
             1792  POP_TOP          

 L. 506      1794  LOAD_FAST                'wait_deliver'
             1796  LOAD_METHOD              cancel
             1798  CALL_METHOD_0         0  ''
             1800  POP_TOP          

 L. 508      1802  LOAD_FAST                'self'
             1804  LOAD_ATTR                logger
             1806  LOAD_METHOD              debug
             1808  LOAD_STR                 '%s Client disconnected'
             1810  LOAD_FAST                'client_session'
             1812  LOAD_ATTR                client_id
             1814  BINARY_MODULO    
             1816  CALL_METHOD_1         1  ''
             1818  POP_TOP          

 L. 509      1820  LOAD_FAST                'server'
             1822  LOAD_METHOD              release_connection
             1824  CALL_METHOD_0         0  ''
             1826  POP_TOP          

Parse error at or near `CALL_FINALLY' instruction at offset 176

    def _init_handler(self, session, reader, writer):
        """
        Create a BrokerProtocolHandler and attach to a session
        :return:
        """
        handler = BrokerProtocolHandler(self.plugins_manager, self._loop)
        handler.attach(session, reader, writer)
        return handler

    @asyncio.coroutine
    def _stop_handler(self, handler):
        """
        Stop a running handler and detach if from the session
        :param handler:
        :return:
        """
        try:
            (yield from handler.stop())
        except Exception as e:
            try:
                self.logger.error(e)
            finally:
                e = None
                del e

        if False:
            yield None

    @asyncio.coroutine
    def authenticate(self, session: Session, listener):
        """
        This method call the authenticate method on registered plugins to test user authentication.
        User is considered authenticated if all plugins called returns True.
        Plugins authenticate() method are supposed to return :
         - True if user is authentication succeed
         - False if user authentication fails
         - None if authentication can't be achieved (then plugin result is then ignored)
        :param session:
        :param listener:
        :return:
        """
        auth_plugins = None
        auth_config = self.config.get('auth', None)
        if auth_config:
            auth_plugins = auth_config.get('plugins', None)
        returns = yield from self.plugins_manager.map_plugin_coro('authenticate',
          session=session,
          filter_plugins=auth_plugins)
        auth_result = True
        if returns:
            for plugin in returns:
                res = returns[plugin]
                if res is False:
                    auth_result = False
                    self.logger.debug("Authentication failed due to '%s' plugin result: %s" % (plugin.name, res))
                else:
                    self.logger.debug("'%s' plugin result: %s" % (plugin.name, res))

        return auth_result
        if False:
            yield None

    @asyncio.coroutine
    def topic_filtering(self, session: Session, topic):
        """
        This method call the topic_filtering method on registered plugins to check that the subscription is allowed.
        User is considered allowed if all plugins called return True.
        Plugins topic_filtering() method are supposed to return :
         - True if MQTT client can be subscribed to the topic
         - False if MQTT client is not allowed to subscribe to the topic
         - None if topic filtering can't be achieved (then plugin result is then ignored)
        :param session:
        :param listener:
        :param topic: Topic in which the client wants to subscribe
        :return:
        """
        topic_plugins = None
        topic_config = self.config.get('topic-check', None)
        if topic_config:
            if topic_config.get('enabled', False):
                topic_plugins = topic_config.get('plugins', None)
        returns = yield from self.plugins_manager.map_plugin_coro('topic_filtering',
          session=session,
          topic=topic,
          filter_plugins=topic_plugins)
        topic_result = True
        if returns:
            for plugin in returns:
                res = returns[plugin]
                if res is False:
                    topic_result = False
                    self.logger.debug("Topic filtering failed due to '%s' plugin result: %s" % (plugin.name, res))
                else:
                    self.logger.debug("'%s' plugin result: %s" % (plugin.name, res))

        return topic_result
        if False:
            yield None

    def retain_message(self, source_session, topic_name, data, qos=None):
        if data is not None and data != b'':
            self.logger.debug('Retaining message on topic %s' % topic_name)
            retained_message = RetainedApplicationMessage(source_session, topic_name, data, qos)
            self._retained_messages[topic_name] = retained_message
        else:
            if topic_name in self._retained_messages:
                self.logger.debug("Clear retained messages for topic '%s'" % topic_name)
                del self._retained_messages[topic_name]

    @asyncio.coroutine
    def add_subscription--- This code section failed: ---

 L. 614         0  SETUP_FINALLY       252  'to 252'

 L. 615         2  LOAD_FAST                'subscription'
                4  LOAD_CONST               0
                6  BINARY_SUBSCR    
                8  STORE_FAST               'a_filter'

 L. 616        10  LOAD_STR                 '#'
               12  LOAD_FAST                'a_filter'
               14  COMPARE_OP               in
               16  POP_JUMP_IF_FALSE    34  'to 34'
               18  LOAD_FAST                'a_filter'
               20  LOAD_METHOD              endswith
               22  LOAD_STR                 '#'
               24  CALL_METHOD_1         1  ''
               26  POP_JUMP_IF_TRUE     34  'to 34'

 L. 618        28  POP_BLOCK        
               30  LOAD_CONST               128
               32  RETURN_VALUE     
             34_0  COME_FROM            26  '26'
             34_1  COME_FROM            16  '16'

 L. 619        34  LOAD_FAST                'a_filter'
               36  LOAD_STR                 '+'
               38  COMPARE_OP               !=
               40  POP_JUMP_IF_FALSE    72  'to 72'

 L. 620        42  LOAD_STR                 '+'
               44  LOAD_FAST                'a_filter'
               46  COMPARE_OP               in
               48  POP_JUMP_IF_FALSE    72  'to 72'

 L. 621        50  LOAD_STR                 '/+'
               52  LOAD_FAST                'a_filter'
               54  COMPARE_OP               not-in
               56  POP_JUMP_IF_FALSE    72  'to 72'
               58  LOAD_STR                 '+/'
               60  LOAD_FAST                'a_filter'
               62  COMPARE_OP               not-in
               64  POP_JUMP_IF_FALSE    72  'to 72'

 L. 623        66  POP_BLOCK        
               68  LOAD_CONST               128
               70  RETURN_VALUE     
             72_0  COME_FROM            64  '64'
             72_1  COME_FROM            56  '56'
             72_2  COME_FROM            48  '48'
             72_3  COME_FROM            40  '40'

 L. 625        72  LOAD_FAST                'self'
               74  LOAD_ATTR                topic_filtering
               76  LOAD_DEREF               'session'
               78  LOAD_FAST                'a_filter'
               80  LOAD_CONST               ('topic',)
               82  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
               84  GET_YIELD_FROM_ITER
               86  LOAD_CONST               None
               88  YIELD_FROM       
               90  STORE_FAST               'permitted'

 L. 626        92  LOAD_FAST                'permitted'
               94  POP_JUMP_IF_TRUE    102  'to 102'

 L. 627        96  POP_BLOCK        
               98  LOAD_CONST               128
              100  RETURN_VALUE     
            102_0  COME_FROM            94  '94'

 L. 628       102  LOAD_FAST                'subscription'
              104  LOAD_CONST               1
              106  BINARY_SUBSCR    
              108  STORE_FAST               'qos'

 L. 629       110  LOAD_STR                 'max-qos'
              112  LOAD_FAST                'self'
              114  LOAD_ATTR                config
              116  COMPARE_OP               in
              118  POP_JUMP_IF_FALSE   144  'to 144'
              120  LOAD_FAST                'qos'
              122  LOAD_FAST                'self'
              124  LOAD_ATTR                config
              126  LOAD_STR                 'max-qos'
              128  BINARY_SUBSCR    
              130  COMPARE_OP               >
              132  POP_JUMP_IF_FALSE   144  'to 144'

 L. 630       134  LOAD_FAST                'self'
              136  LOAD_ATTR                config
              138  LOAD_STR                 'max-qos'
              140  BINARY_SUBSCR    
              142  STORE_FAST               'qos'
            144_0  COME_FROM           132  '132'
            144_1  COME_FROM           118  '118'

 L. 631       144  LOAD_FAST                'a_filter'
              146  LOAD_FAST                'self'
              148  LOAD_ATTR                _subscriptions
              150  COMPARE_OP               not-in
              152  POP_JUMP_IF_FALSE   164  'to 164'

 L. 632       154  BUILD_LIST_0          0 
              156  LOAD_FAST                'self'
              158  LOAD_ATTR                _subscriptions
              160  LOAD_FAST                'a_filter'
              162  STORE_SUBSCR     
            164_0  COME_FROM           152  '152'

 L. 633       164  LOAD_GLOBAL              next

 L. 634       166  LOAD_CLOSURE             'session'
              168  BUILD_TUPLE_1         1 
              170  LOAD_GENEXPR             '<code_object <genexpr>>'
              172  LOAD_STR                 'Broker.add_subscription.<locals>.<genexpr>'
              174  MAKE_FUNCTION_8          'closure'
              176  LOAD_FAST                'self'
              178  LOAD_ATTR                _subscriptions
              180  LOAD_FAST                'a_filter'
              182  BINARY_SUBSCR    
              184  GET_ITER         
              186  CALL_FUNCTION_1       1  ''

 L. 634       188  LOAD_CONST               None

 L. 633       190  CALL_FUNCTION_2       2  ''
              192  STORE_FAST               'already_subscribed'

 L. 635       194  LOAD_FAST                'already_subscribed'
              196  POP_JUMP_IF_TRUE    220  'to 220'

 L. 636       198  LOAD_FAST                'self'
              200  LOAD_ATTR                _subscriptions
              202  LOAD_FAST                'a_filter'
              204  BINARY_SUBSCR    
              206  LOAD_METHOD              append
              208  LOAD_DEREF               'session'
              210  LOAD_FAST                'qos'
              212  BUILD_TUPLE_2         2 
              214  CALL_METHOD_1         1  ''
              216  POP_TOP          
              218  JUMP_FORWARD        246  'to 246'
            220_0  COME_FROM           196  '196'

 L. 638       220  LOAD_FAST                'self'
              222  LOAD_ATTR                logger
              224  LOAD_METHOD              debug
              226  LOAD_STR                 'Client %s has already subscribed to %s'
              228  LOAD_GLOBAL              format_client_message
              230  LOAD_DEREF               'session'
              232  LOAD_CONST               ('session',)
              234  CALL_FUNCTION_KW_1     1  '1 total positional and keyword args'
              236  LOAD_FAST                'a_filter'
              238  BUILD_TUPLE_2         2 
              240  BINARY_MODULO    
              242  CALL_METHOD_1         1  ''
              244  POP_TOP          
            246_0  COME_FROM           218  '218'

 L. 639       246  LOAD_FAST                'qos'
              248  POP_BLOCK        
              250  RETURN_VALUE     
            252_0  COME_FROM_FINALLY     0  '0'

 L. 640       252  DUP_TOP          
              254  LOAD_GLOBAL              KeyError
              256  COMPARE_OP               exception-match
          258_260  POP_JUMP_IF_FALSE   274  'to 274'
              262  POP_TOP          
              264  POP_TOP          
              266  POP_TOP          

 L. 641       268  POP_EXCEPT       
              270  LOAD_CONST               128
              272  RETURN_VALUE     
            274_0  COME_FROM           258  '258'
              274  END_FINALLY      

Parse error at or near `LOAD_CONST' instruction at offset 30

    def _del_subscription--- This code section failed: ---

 L. 650         0  LOAD_CONST               0
                2  STORE_FAST               'deleted'

 L. 651         4  LOAD_CONST               None
                6  SETUP_FINALLY       130  'to 130'
                8  SETUP_FINALLY       106  'to 106'

 L. 652        10  LOAD_FAST                'self'
               12  LOAD_ATTR                _subscriptions
               14  LOAD_FAST                'a_filter'
               16  BINARY_SUBSCR    
               18  STORE_FAST               'subscriptions'

 L. 653        20  LOAD_GLOBAL              enumerate
               22  LOAD_FAST                'subscriptions'
               24  CALL_FUNCTION_1       1  ''
               26  GET_ITER         
             28_0  COME_FROM            50  '50'
               28  FOR_ITER            102  'to 102'
               30  UNPACK_SEQUENCE_2     2 
               32  STORE_FAST               'index'
               34  UNPACK_SEQUENCE_2     2 
               36  STORE_FAST               'sub_session'
               38  STORE_FAST               'qos'

 L. 654        40  LOAD_FAST                'sub_session'
               42  LOAD_ATTR                client_id
               44  LOAD_FAST                'session'
               46  LOAD_ATTR                client_id
               48  COMPARE_OP               ==
               50  POP_JUMP_IF_FALSE    28  'to 28'

 L. 655        52  LOAD_FAST                'self'
               54  LOAD_ATTR                logger
               56  LOAD_METHOD              debug
               58  LOAD_STR                 "Removing subscription on topic '%s' for client %s"

 L. 656        60  LOAD_FAST                'a_filter'
               62  LOAD_GLOBAL              format_client_message
               64  LOAD_FAST                'session'
               66  LOAD_CONST               ('session',)
               68  CALL_FUNCTION_KW_1     1  '1 total positional and keyword args'
               70  BUILD_TUPLE_2         2 

 L. 655        72  BINARY_MODULO    
               74  CALL_METHOD_1         1  ''
               76  POP_TOP          

 L. 657        78  LOAD_FAST                'subscriptions'
               80  LOAD_METHOD              pop
               82  LOAD_FAST                'index'
               84  CALL_METHOD_1         1  ''
               86  POP_TOP          

 L. 658        88  LOAD_FAST                'deleted'
               90  LOAD_CONST               1
               92  INPLACE_ADD      
               94  STORE_FAST               'deleted'

 L. 659        96  POP_TOP          
               98  BREAK_LOOP          102  'to 102'
              100  JUMP_BACK            28  'to 28'
              102  POP_BLOCK        
              104  JUMP_FORWARD        126  'to 126'
            106_0  COME_FROM_FINALLY     8  '8'

 L. 660       106  DUP_TOP          
              108  LOAD_GLOBAL              KeyError
              110  COMPARE_OP               exception-match
              112  POP_JUMP_IF_FALSE   124  'to 124'
              114  POP_TOP          
              116  POP_TOP          
              118  POP_TOP          

 L. 662       120  POP_EXCEPT       
              122  JUMP_FORWARD        126  'to 126'
            124_0  COME_FROM           112  '112'
              124  END_FINALLY      
            126_0  COME_FROM           122  '122'
            126_1  COME_FROM           104  '104'
              126  POP_BLOCK        
              128  BEGIN_FINALLY    
            130_0  COME_FROM_FINALLY     6  '6'

 L. 664       130  LOAD_FAST                'deleted'
              132  POP_FINALLY           1  ''
              134  ROT_TWO          
              136  POP_TOP          
              138  RETURN_VALUE     
              140  END_FINALLY      
              142  POP_TOP          

Parse error at or near `LOAD_FAST' instruction at offset 130

    def _del_all_subscriptions(self, session):
        """
        Delete all topic subscriptions for a given session
        :param session:
        :return:
        """
        filter_queue = deque()
        for topic in self._subscriptions:
            if self._del_subscription(topic, session):
                filter_queue.append(topic)
        else:
            for topic in filter_queue:
                if not self._subscriptions[topic]:
                    del self._subscriptions[topic]

    def matches(self, topic, a_filter):
        if '#' not in a_filter:
            if '+' not in a_filter:
                return a_filter == topic
        match_pattern = re.compile(a_filter.replace('#', '.*').replace('$', '\\$').replace('+', '[/\\$\\s\\w\\d]+'))
        return match_pattern.match(topic)

    @asyncio.coroutine
    def _broadcast_loop(self):
        running_tasks = deque()
        try:
            while running_tasks:
                if running_tasks[0].done():
                    running_tasks.popleft()
                else:
                    broadcast = yield from self._broadcast_queue.get()
                    if self.logger.isEnabledFor(logging.DEBUG):
                        self.logger.debug('broadcasting %r' % broadcast)
                    for k_filter in self._subscriptions:
                        if not broadcast['topic'].startswith('$') or k_filter.startswith('+') or k_filter.startswith('#'):
                            self.logger.debug('[MQTT-4.7.2-1] - ignoring brodcasting $ topic to subscriptions starting with + or #')
                        elif self.matches(broadcast['topic'], k_filter):
                            subscriptions = self._subscriptions[k_filter]

                    for target_session, qos in subscriptions:
                        if 'qos' in broadcast:
                            qos = broadcast['qos']
                        if target_session.transitions.state == 'connected':
                            self.logger.debug("broadcasting application message from %s on topic '%s' to %s" % (
                             format_client_message(session=(broadcast['session'])),
                             broadcast['topic'], format_client_message(session=target_session)))
                            handler = self._get_handler(target_session)
                            task = asyncio.ensure_future(handler.mqtt_publish((broadcast['topic']), (broadcast['data']), qos, retain=False),
                              loop=(self._loop))
                            running_tasks.append(task)
                        else:
                            self.logger.debug("retaining application message from %s on topic '%s' to client '%s'" % (
                             format_client_message(session=(broadcast['session'])),
                             broadcast['topic'], format_client_message(session=target_session)))
                            retained_message = RetainedApplicationMessage(broadcast['session'], broadcast['topic'], broadcast['data'], qos)
                            (yield from target_session.retained_messages.put(retained_message))

        except CancelledError:
            if running_tasks:
                (yield from asyncio.wait(running_tasks, loop=(self._loop)))

        if False:
            yield None

    @asyncio.coroutine
    def _broadcast_message(self, session, topic, data, force_qos=None):
        broadcast = {'session':session, 
         'topic':topic, 
         'data':data}
        if force_qos:
            broadcast['qos'] = force_qos
        (yield from self._broadcast_queue.put(broadcast))
        if False:
            yield None

    @asyncio.coroutine
    def publish_session_retained_messages(self, session):
        self.logger.debug('Publishing %d messages retained for session %s' % (
         session.retained_messages.qsize(), format_client_message(session=session)))
        publish_tasks = []
        handler = self._get_handler(session)
        while not session.retained_messages.empty():
            retained = yield from session.retained_messages.get()
            publish_tasks.append(asyncio.ensure_future((handler.mqtt_publish(retained.topic, retained.data, retained.qos, True)),
              loop=(self._loop)))

        if publish_tasks:
            (yield from asyncio.wait(publish_tasks, loop=(self._loop)))
        if False:
            yield None

    @asyncio.coroutine
    def publish_retained_messages_for_subscription(self, subscription, session):
        self.logger.debug("Begin broadcasting messages retained due to subscription on '%s' from %s" % (
         subscription[0], format_client_message(session=session)))
        publish_tasks = []
        handler = self._get_handler(session)
        for d_topic in self._retained_messages:
            self.logger.debug('matching : %s %s' % (d_topic, subscription[0]))
            if self.matches(d_topic, subscription[0]):
                self.logger.debug('%s and %s match' % (d_topic, subscription[0]))
                retained = self._retained_messages[d_topic]
                publish_tasks.append(asyncio.Task((handler.mqtt_publish(retained.topic, retained.data, subscription[1], True)),
                  loop=(self._loop)))
        else:
            if publish_tasks:
                (yield from asyncio.wait(publish_tasks, loop=(self._loop)))
            self.logger.debug("End broadcasting messages retained due to subscription on '%s' from %s" % (
             subscription[0], format_client_message(session=session)))

        if False:
            yield None

    def delete_session(self, client_id):
        """
        Delete an existing session data, for example due to clean session set in CONNECT
        :param client_id:
        :return:
        """
        try:
            session = self._sessions[client_id][0]
        except KeyError:
            session = None
        else:
            if session is None:
                self.logger.debug("Delete session : session %s doesn't exist" % client_id)
                return None
            self.logger.debug('deleting session %s subscriptions' % repr(session))
            self._del_all_subscriptions(session)
            self.logger.debug('deleting existing session %s' % repr(self._sessions[client_id]))
            del self._sessions[client_id]

    def _get_handler--- This code section failed: ---

 L. 795         0  LOAD_FAST                'session'
                2  LOAD_ATTR                client_id
                4  STORE_FAST               'client_id'

 L. 796         6  LOAD_FAST                'client_id'
                8  POP_JUMP_IF_FALSE    48  'to 48'

 L. 797        10  SETUP_FINALLY        28  'to 28'

 L. 798        12  LOAD_FAST                'self'
               14  LOAD_ATTR                _sessions
               16  LOAD_FAST                'client_id'
               18  BINARY_SUBSCR    
               20  LOAD_CONST               1
               22  BINARY_SUBSCR    
               24  POP_BLOCK        
               26  RETURN_VALUE     
             28_0  COME_FROM_FINALLY    10  '10'

 L. 799        28  DUP_TOP          
               30  LOAD_GLOBAL              KeyError
               32  COMPARE_OP               exception-match
               34  POP_JUMP_IF_FALSE    46  'to 46'
               36  POP_TOP          
               38  POP_TOP          
               40  POP_TOP          

 L. 800        42  POP_EXCEPT       
               44  JUMP_FORWARD         48  'to 48'
             46_0  COME_FROM            34  '34'
               46  END_FINALLY      
             48_0  COME_FROM            44  '44'
             48_1  COME_FROM             8  '8'

Parse error at or near `POP_TOP' instruction at offset 38