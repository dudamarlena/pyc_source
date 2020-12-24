# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/lib/python3.8/site-packages/hbmqtt/client.py
# Compiled at: 2020-01-25 09:04:28
# Size of source mod 2**32: 22584 bytes
import asyncio, logging, ssl, copy
from urllib.parse import urlparse, urlunparse
from functools import wraps
from hbmqtt.utils import not_in_dict_or_none
from hbmqtt.session import Session
from hbmqtt.mqtt.connack import CONNECTION_ACCEPTED
from hbmqtt.mqtt.protocol.client_handler import ClientProtocolHandler
from hbmqtt.adapters import StreamReaderAdapter, StreamWriterAdapter, WebSocketsReader, WebSocketsWriter
from hbmqtt.plugins.manager import PluginManager, BaseContext
from hbmqtt.mqtt.protocol.handler import ProtocolHandlerException
from hbmqtt.mqtt.constants import QOS_0, QOS_1, QOS_2
import websockets
from websockets.uri import InvalidURI
from websockets.exceptions import InvalidHandshake
from collections import deque
_defaults = {'keep_alive':10, 
 'ping_delay':1, 
 'default_qos':0, 
 'default_retain':False, 
 'auto_reconnect':True, 
 'reconnect_max_interval':10, 
 'reconnect_retries':2}

class ClientException(Exception):
    pass


class ConnectException(ClientException):
    pass


class ClientContext(BaseContext):
    __doc__ = '\n        ClientContext is used as the context passed to plugins interacting with the client.\n        It act as an adapter to client services from plugins\n    '

    def __init__(self):
        super().__init__()
        self.config = None


base_logger = logging.getLogger(__name__)

def mqtt_connected(func):
    """
        MQTTClient coroutines decorator which will wait until connection before calling the decorated method.
        :param func: coroutine to be called once connected
        :return: coroutine result
    """

    @asyncio.coroutine
    @wraps(func)
    def wrapper(self, *args, **kwargs):
        if not self._connected_state.is_set():
            base_logger.warning('Client not connected, waiting for it')
            _, pending = yield from asyncio.wait([self._connected_state.wait(), self._no_more_connections.wait()], return_when=(asyncio.FIRST_COMPLETED))
            for t in pending:
                t.cancel()
            else:
                if self._no_more_connections.is_set():
                    raise ClientException('Will not reconnect')

        return (yield from func(self, *args, **kwargs))
        if False:
            yield None

    return wrapper


class MQTTClient:
    __doc__ = '\n        MQTT client implementation.\n\n        MQTTClient instances provides API for connecting to a broker and send/receive messages using the MQTT protocol.\n\n        :param client_id: MQTT client ID to use when connecting to the broker. If none, it will generated randomly by :func:`hbmqtt.utils.gen_client_id`\n        :param config: Client configuration\n        :param loop: asynio loop to use\n        :return: class instance\n    '

    def __init__(self, client_id=None, config=None, loop=None):
        self.logger = logging.getLogger(__name__)
        self.config = copy.deepcopy(_defaults)
        if config is not None:
            self.config.update(config)
        else:
            if client_id is not None:
                self.client_id = client_id
            else:
                from hbmqtt.utils import gen_client_id
                self.client_id = gen_client_id()
                self.logger.debug('Using generated client ID : %s' % self.client_id)
            if loop is not None:
                self._loop = loop
            else:
                self._loop = asyncio.get_event_loop()
        self.session = None
        self._handler = None
        self._disconnect_task = None
        self._connected_state = asyncio.Event(loop=(self._loop))
        self._no_more_connections = asyncio.Event(loop=(self._loop))
        self.extra_headers = {}
        context = ClientContext()
        context.config = self.config
        self.plugins_manager = PluginManager('hbmqtt.client.plugins', context)
        self.client_tasks = deque()

    @asyncio.coroutine
    def connect--- This code section failed: ---

 L. 144         0  LOAD_FAST                'self'
                2  LOAD_METHOD              _initsession
                4  LOAD_FAST                'uri'
                6  LOAD_FAST                'cleansession'
                8  LOAD_FAST                'cafile'
               10  LOAD_FAST                'capath'
               12  LOAD_FAST                'cadata'
               14  CALL_METHOD_5         5  ''
               16  LOAD_FAST                'self'
               18  STORE_ATTR               session

 L. 145        20  LOAD_FAST                'extra_headers'
               22  LOAD_FAST                'self'
               24  STORE_ATTR               extra_headers

 L. 146        26  LOAD_FAST                'self'
               28  LOAD_ATTR                logger
               30  LOAD_METHOD              debug
               32  LOAD_STR                 'Connect to: %s'
               34  LOAD_FAST                'uri'
               36  BINARY_MODULO    
               38  CALL_METHOD_1         1  ''
               40  POP_TOP          

 L. 148        42  SETUP_FINALLY        60  'to 60'

 L. 149        44  LOAD_FAST                'self'
               46  LOAD_METHOD              _do_connect
               48  CALL_METHOD_0         0  ''
               50  GET_YIELD_FROM_ITER
               52  LOAD_CONST               None
               54  YIELD_FROM       
               56  POP_BLOCK        
               58  RETURN_VALUE     
             60_0  COME_FROM_FINALLY    42  '42'

 L. 150        60  DUP_TOP          
               62  LOAD_GLOBAL              BaseException
               64  COMPARE_OP               exception-match
               66  POP_JUMP_IF_FALSE   152  'to 152'
               68  POP_TOP          
               70  STORE_FAST               'be'
               72  POP_TOP          
               74  SETUP_FINALLY       140  'to 140'

 L. 151        76  LOAD_FAST                'self'
               78  LOAD_ATTR                logger
               80  LOAD_METHOD              warning
               82  LOAD_STR                 'Connection failed: %r'
               84  LOAD_FAST                'be'
               86  BINARY_MODULO    
               88  CALL_METHOD_1         1  ''
               90  POP_TOP          

 L. 152        92  LOAD_FAST                'self'
               94  LOAD_ATTR                config
               96  LOAD_METHOD              get
               98  LOAD_STR                 'auto_reconnect'
              100  LOAD_CONST               False
              102  CALL_METHOD_2         2  ''
              104  STORE_FAST               'auto_reconnect'

 L. 153       106  LOAD_FAST                'auto_reconnect'
              108  POP_JUMP_IF_TRUE    114  'to 114'

 L. 154       110  RAISE_VARARGS_0       0  'reraise'
              112  JUMP_FORWARD        136  'to 136'
            114_0  COME_FROM           108  '108'

 L. 156       114  LOAD_FAST                'self'
              116  LOAD_METHOD              reconnect
              118  CALL_METHOD_0         0  ''
              120  GET_YIELD_FROM_ITER
              122  LOAD_CONST               None
              124  YIELD_FROM       
              126  ROT_FOUR         
              128  POP_BLOCK        
              130  POP_EXCEPT       
              132  CALL_FINALLY        140  'to 140'
              134  RETURN_VALUE     
            136_0  COME_FROM           112  '112'
              136  POP_BLOCK        
              138  BEGIN_FINALLY    
            140_0  COME_FROM           132  '132'
            140_1  COME_FROM_FINALLY    74  '74'
              140  LOAD_CONST               None
              142  STORE_FAST               'be'
              144  DELETE_FAST              'be'
              146  END_FINALLY      
              148  POP_EXCEPT       
              150  JUMP_FORWARD        154  'to 154'
            152_0  COME_FROM            66  '66'
              152  END_FINALLY      
            154_0  COME_FROM           150  '150'

Parse error at or near `POP_BLOCK' instruction at offset 128

    @asyncio.coroutine
    def disconnect(self):
        """
            Disconnect from the connected broker.

            This method sends a `DISCONNECT <http://docs.oasis-open.org/mqtt/mqtt/v3.1.1/os/mqtt-v3.1.1-os.html#_Toc398718090>`_ message and closes the network socket.

            This method is a *coroutine*.
        """
        (yield from self.cancel_tasks())
        if self.session.transitions.is_connected():
            if not self._disconnect_task.done():
                self._disconnect_task.cancel()
            (yield from self._handler.mqtt_disconnect())
            self._connected_state.clear()
            (yield from self._handler.stop())
            self.session.transitions.disconnect()
        else:
            self.logger.warning('Client session is not currently connected, ignoring call')
        if False:
            yield None

    @asyncio.coroutine
    def cancel_tasks(self):
        """
        Before disconnection need to cancel all pending tasks
        :return:
        """
        try:
            while True:
                task = self.client_tasks.pop()
                task.cancel()

        except IndexError as err:
            try:
                pass
            finally:
                err = None
                del err

    @asyncio.coroutine
    def reconnect--- This code section failed: ---

 L. 206         0  LOAD_FAST                'self'
                2  LOAD_ATTR                session
                4  LOAD_ATTR                transitions
                6  LOAD_METHOD              is_connected
                8  CALL_METHOD_0         0  ''
               10  POP_JUMP_IF_FALSE    28  'to 28'

 L. 207        12  LOAD_FAST                'self'
               14  LOAD_ATTR                logger
               16  LOAD_METHOD              warning
               18  LOAD_STR                 'Client already connected'
               20  CALL_METHOD_1         1  ''
               22  POP_TOP          

 L. 208        24  LOAD_GLOBAL              CONNECTION_ACCEPTED
               26  RETURN_VALUE     
             28_0  COME_FROM            10  '10'

 L. 210        28  LOAD_FAST                'cleansession'
               30  POP_JUMP_IF_FALSE    40  'to 40'

 L. 211        32  LOAD_FAST                'cleansession'
               34  LOAD_FAST                'self'
               36  LOAD_ATTR                session
               38  STORE_ATTR               clean_session
             40_0  COME_FROM            30  '30'

 L. 212        40  LOAD_FAST                'self'
               42  LOAD_ATTR                logger
               44  LOAD_METHOD              debug
               46  LOAD_STR                 'Reconnecting with session parameters: %s'
               48  LOAD_FAST                'self'
               50  LOAD_ATTR                session
               52  BINARY_MODULO    
               54  CALL_METHOD_1         1  ''
               56  POP_TOP          

 L. 213        58  LOAD_FAST                'self'
               60  LOAD_ATTR                config
               62  LOAD_METHOD              get
               64  LOAD_STR                 'reconnect_max_interval'
               66  LOAD_CONST               10
               68  CALL_METHOD_2         2  ''
               70  STORE_FAST               'reconnect_max_interval'

 L. 214        72  LOAD_FAST                'self'
               74  LOAD_ATTR                config
               76  LOAD_METHOD              get
               78  LOAD_STR                 'reconnect_retries'
               80  LOAD_CONST               5
               82  CALL_METHOD_2         2  ''
               84  STORE_FAST               'reconnect_retries'

 L. 215        86  LOAD_CONST               1
               88  STORE_FAST               'nb_attempt'

 L. 216        90  LOAD_GLOBAL              asyncio
               92  LOAD_ATTR                sleep
               94  LOAD_CONST               1
               96  LOAD_FAST                'self'
               98  LOAD_ATTR                _loop
              100  LOAD_CONST               ('loop',)
              102  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              104  GET_YIELD_FROM_ITER
              106  LOAD_CONST               None
              108  YIELD_FROM       
              110  POP_TOP          

 L. 218       112  SETUP_FINALLY       146  'to 146'

 L. 219       114  LOAD_FAST                'self'
              116  LOAD_ATTR                logger
              118  LOAD_METHOD              debug
              120  LOAD_STR                 'Reconnect attempt %d ...'
              122  LOAD_FAST                'nb_attempt'
              124  BINARY_MODULO    
              126  CALL_METHOD_1         1  ''
              128  POP_TOP          

 L. 220       130  LOAD_FAST                'self'
              132  LOAD_METHOD              _do_connect
              134  CALL_METHOD_0         0  ''
              136  GET_YIELD_FROM_ITER
              138  LOAD_CONST               None
              140  YIELD_FROM       
              142  POP_BLOCK        
              144  RETURN_VALUE     
            146_0  COME_FROM_FINALLY   112  '112'

 L. 221       146  DUP_TOP          
              148  LOAD_GLOBAL              BaseException
              150  COMPARE_OP               exception-match
          152_154  POP_JUMP_IF_FALSE   302  'to 302'
              156  POP_TOP          
              158  STORE_FAST               'e'
              160  POP_TOP          
              162  SETUP_FINALLY       290  'to 290'

 L. 222       164  LOAD_FAST                'self'
              166  LOAD_ATTR                logger
              168  LOAD_METHOD              warning
              170  LOAD_STR                 'Reconnection attempt failed: %r'
              172  LOAD_FAST                'e'
              174  BINARY_MODULO    
              176  CALL_METHOD_1         1  ''
              178  POP_TOP          

 L. 223       180  LOAD_FAST                'reconnect_retries'
              182  LOAD_CONST               0
              184  COMPARE_OP               >=
              186  POP_JUMP_IF_FALSE   216  'to 216'
              188  LOAD_FAST                'nb_attempt'
              190  LOAD_FAST                'reconnect_retries'
              192  COMPARE_OP               >
              194  POP_JUMP_IF_FALSE   216  'to 216'

 L. 224       196  LOAD_FAST                'self'
              198  LOAD_ATTR                logger
              200  LOAD_METHOD              error
              202  LOAD_STR                 'Maximum number of connection attempts reached. Reconnection aborted'
              204  CALL_METHOD_1         1  ''
              206  POP_TOP          

 L. 225       208  LOAD_GLOBAL              ConnectException
              210  LOAD_STR                 'Too many connection attempts failed'
              212  CALL_FUNCTION_1       1  ''
              214  RAISE_VARARGS_1       1  'exception instance'
            216_0  COME_FROM           194  '194'
            216_1  COME_FROM           186  '186'

 L. 226       216  LOAD_CONST               2
              218  LOAD_FAST                'nb_attempt'
              220  BINARY_POWER     
              222  STORE_FAST               'exp'

 L. 227       224  LOAD_FAST                'exp'
              226  LOAD_FAST                'reconnect_max_interval'
              228  COMPARE_OP               <
              230  POP_JUMP_IF_FALSE   236  'to 236'
              232  LOAD_FAST                'exp'
              234  JUMP_FORWARD        238  'to 238'
            236_0  COME_FROM           230  '230'
              236  LOAD_FAST                'reconnect_max_interval'
            238_0  COME_FROM           234  '234'
              238  STORE_FAST               'delay'

 L. 228       240  LOAD_FAST                'self'
              242  LOAD_ATTR                logger
              244  LOAD_METHOD              debug
              246  LOAD_STR                 'Waiting %d second before next attempt'
              248  LOAD_FAST                'delay'
              250  BINARY_MODULO    
              252  CALL_METHOD_1         1  ''
              254  POP_TOP          

 L. 229       256  LOAD_GLOBAL              asyncio
              258  LOAD_ATTR                sleep
              260  LOAD_FAST                'delay'
              262  LOAD_FAST                'self'
              264  LOAD_ATTR                _loop
              266  LOAD_CONST               ('loop',)
              268  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              270  GET_YIELD_FROM_ITER
              272  LOAD_CONST               None
              274  YIELD_FROM       
              276  POP_TOP          

 L. 230       278  LOAD_FAST                'nb_attempt'
              280  LOAD_CONST               1
              282  INPLACE_ADD      
              284  STORE_FAST               'nb_attempt'
              286  POP_BLOCK        
              288  BEGIN_FINALLY    
            290_0  COME_FROM_FINALLY   162  '162'
              290  LOAD_CONST               None
              292  STORE_FAST               'e'
              294  DELETE_FAST              'e'
              296  END_FINALLY      
              298  POP_EXCEPT       
              300  JUMP_BACK           112  'to 112'
            302_0  COME_FROM           152  '152'
              302  END_FINALLY      
              304  JUMP_BACK           112  'to 112'

Parse error at or near `JUMP_BACK' instruction at offset 300

    @asyncio.coroutine
    def _do_connect(self):
        return_code = yield from self._connect_coro()
        self._disconnect_task = asyncio.ensure_future((self.handle_connection_close()), loop=(self._loop))
        return return_code
        if False:
            yield None

    @mqtt_connected
    @asyncio.coroutine
    def ping(self):
        """
            Ping the broker.

            Send a MQTT `PINGREQ <http://docs.oasis-open.org/mqtt/mqtt/v3.1.1/os/mqtt-v3.1.1-os.html#_Toc398718081>`_ message for response.

            This method is a *coroutine*.
        """
        if self.session.transitions.is_connected():
            (yield from self._handler.mqtt_ping())
        else:
            self.logger.warning("MQTT PING request incompatible with current session state '%s'" % self.session.transitions.state)
        if False:
            yield None

    @mqtt_connected
    @asyncio.coroutine
    def publish(self, topic, message, qos=None, retain=None, ack_timeout=None):
        """
            Publish a message to the broker.

            Send a MQTT `PUBLISH <http://docs.oasis-open.org/mqtt/mqtt/v3.1.1/os/mqtt-v3.1.1-os.html#_Toc398718037>`_ message and wait for acknowledgment depending on Quality Of Service

            This method is a *coroutine*.

            :param topic: topic name to which message data is published
            :param message: payload message (as bytes) to send.
            :param qos: requested publish quality of service : QOS_0, QOS_1 or QOS_2. Defaults to ``default_qos`` config parameter or QOS_0.
            :param retain: retain flag. Defaults to ``default_retain`` config parameter or False.
        """

        def get_retain_and_qos():
            if qos:
                assert qos in (QOS_0, QOS_1, QOS_2)
                _qos = qos
            else:
                _qos = self.config['default_qos']
                try:
                    _qos = self.config['topics'][topic]['qos']
                except KeyError:
                    pass
                else:
                    if retain:
                        _retain = retain
                    else:
                        _retain = self.config['default_retain']
                        try:
                            _retain = self.config['topics'][topic]['retain']
                        except KeyError:
                            pass
                        else:
                            return (
                             _qos, _retain)

        app_qos, app_retain = get_retain_and_qos()
        return (yield from self._handler.mqtt_publishtopicmessageapp_qosapp_retainack_timeout)
        if False:
            yield None

    @mqtt_connected
    @asyncio.coroutine
    def subscribe(self, topics):
        """
            Subscribe to some topics.

            Send a MQTT `SUBSCRIBE <http://docs.oasis-open.org/mqtt/mqtt/v3.1.1/os/mqtt-v3.1.1-os.html#_Toc398718063>`_ message and wait for broker acknowledgment.

            This method is a *coroutine*.

            :param topics: array of topics pattern to subscribe with associated QoS.
            :return: `SUBACK <http://docs.oasis-open.org/mqtt/mqtt/v3.1.1/os/mqtt-v3.1.1-os.html#_Toc398718068>`_ message return code.

            Example of ``topics`` argument expected structure:
            ::

                [
                    ('$SYS/broker/uptime', QOS_1),
                    ('$SYS/broker/load/#', QOS_2),
                ]
        """
        return (yield from self._handler.mqtt_subscribetopicsself.session.next_packet_id)
        if False:
            yield None

    @mqtt_connected
    @asyncio.coroutine
    def unsubscribe(self, topics):
        """
            Unsubscribe from some topics.

            Send a MQTT `UNSUBSCRIBE <http://docs.oasis-open.org/mqtt/mqtt/v3.1.1/os/mqtt-v3.1.1-os.html#_Toc398718072>`_ message and wait for broker `UNSUBACK <http://docs.oasis-open.org/mqtt/mqtt/v3.1.1/os/mqtt-v3.1.1-os.html#_Toc398718077>`_ message.

            This method is a *coroutine*.

            :param topics: array of topics to unsubscribe from.

            Example of ``topics`` argument expected structure:
            ::

                ['$SYS/broker/uptime', '$SYS/broker/load/#']
        """
        (yield from self._handler.mqtt_unsubscribetopicsself.session.next_packet_id)
        if False:
            yield None

    @asyncio.coroutine
    def deliver_message(self, timeout=None):
        """
            Deliver next received message.

            Deliver next message received from the broker. If no message is available, this methods waits until next message arrives or ``timeout`` occurs.

            This method is a *coroutine*.

            :param timeout: maximum number of seconds to wait before returning. If timeout is not specified or None, there is no limit to the wait time until next message arrives.
            :return: instance of :class:`hbmqtt.session.ApplicationMessage` containing received message information flow.
            :raises: :class:`asyncio.TimeoutError` if timeout occurs before a message is delivered
        """
        deliver_task = asyncio.ensure_future((self._handler.mqtt_deliver_next_message()), loop=(self._loop))
        self.client_tasks.append(deliver_task)
        self.logger.debug('Waiting message delivery')
        done, pending = yield from asyncio.wait([deliver_task], loop=(self._loop), return_when=(asyncio.FIRST_EXCEPTION), timeout=timeout)
        if deliver_task in done:
            if deliver_task.exception() is not None:
                raise deliver_task.exception()
            self.client_tasks.pop()
            return deliver_task.result()
        deliver_task.cancel()
        raise asyncio.TimeoutError
        if False:
            yield None

    @asyncio.coroutine
    def _connect_coro--- This code section failed: ---

 L. 365         0  LOAD_GLOBAL              dict
                2  CALL_FUNCTION_0       0  ''
                4  STORE_FAST               'kwargs'

 L. 368         6  LOAD_GLOBAL              urlparse
                8  LOAD_FAST                'self'
               10  LOAD_ATTR                session
               12  LOAD_ATTR                broker_uri
               14  CALL_FUNCTION_1       1  ''
               16  STORE_FAST               'uri_attributes'

 L. 369        18  LOAD_FAST                'uri_attributes'
               20  LOAD_ATTR                scheme
               22  STORE_FAST               'scheme'

 L. 370        24  LOAD_FAST                'scheme'
               26  LOAD_CONST               ('mqtts', 'wss')
               28  COMPARE_OP               in
               30  POP_JUMP_IF_FALSE    36  'to 36'
               32  LOAD_CONST               True
               34  JUMP_FORWARD         38  'to 38'
             36_0  COME_FROM            30  '30'
               36  LOAD_CONST               False
             38_0  COME_FROM            34  '34'
               38  STORE_FAST               'secure'

 L. 371        40  LOAD_FAST                'self'
               42  LOAD_ATTR                session
               44  LOAD_ATTR                username
               46  POP_JUMP_IF_FALSE    56  'to 56'
               48  LOAD_FAST                'self'
               50  LOAD_ATTR                session
               52  LOAD_ATTR                username
               54  JUMP_FORWARD         60  'to 60'
             56_0  COME_FROM            46  '46'
               56  LOAD_FAST                'uri_attributes'
               58  LOAD_ATTR                username
             60_0  COME_FROM            54  '54'
               60  LOAD_FAST                'self'
               62  LOAD_ATTR                session
               64  STORE_ATTR               username

 L. 372        66  LOAD_FAST                'self'
               68  LOAD_ATTR                session
               70  LOAD_ATTR                password
               72  POP_JUMP_IF_FALSE    82  'to 82'
               74  LOAD_FAST                'self'
               76  LOAD_ATTR                session
               78  LOAD_ATTR                password
               80  JUMP_FORWARD         86  'to 86'
             82_0  COME_FROM            72  '72'
               82  LOAD_FAST                'uri_attributes'
               84  LOAD_ATTR                password
             86_0  COME_FROM            80  '80'
               86  LOAD_FAST                'self'
               88  LOAD_ATTR                session
               90  STORE_ATTR               password

 L. 373        92  LOAD_FAST                'uri_attributes'
               94  LOAD_ATTR                hostname
               96  LOAD_FAST                'self'
               98  LOAD_ATTR                session
              100  STORE_ATTR               remote_address

 L. 374       102  LOAD_FAST                'uri_attributes'
              104  LOAD_ATTR                port
              106  LOAD_FAST                'self'
              108  LOAD_ATTR                session
              110  STORE_ATTR               remote_port

 L. 375       112  LOAD_FAST                'scheme'
              114  LOAD_CONST               ('mqtt', 'mqtts')
              116  COMPARE_OP               in
              118  POP_JUMP_IF_FALSE   148  'to 148'
              120  LOAD_FAST                'self'
              122  LOAD_ATTR                session
              124  LOAD_ATTR                remote_port
              126  POP_JUMP_IF_TRUE    148  'to 148'

 L. 376       128  LOAD_FAST                'scheme'
              130  LOAD_STR                 'mqtts'
              132  COMPARE_OP               ==
              134  POP_JUMP_IF_FALSE   140  'to 140'
              136  LOAD_CONST               8883
              138  JUMP_FORWARD        142  'to 142'
            140_0  COME_FROM           134  '134'
              140  LOAD_CONST               1883
            142_0  COME_FROM           138  '138'
              142  LOAD_FAST                'self'
              144  LOAD_ATTR                session
              146  STORE_ATTR               remote_port
            148_0  COME_FROM           126  '126'
            148_1  COME_FROM           118  '118'

 L. 377       148  LOAD_FAST                'scheme'
              150  LOAD_CONST               ('ws', 'wss')
              152  COMPARE_OP               in
              154  POP_JUMP_IF_FALSE   184  'to 184'
              156  LOAD_FAST                'self'
              158  LOAD_ATTR                session
              160  LOAD_ATTR                remote_port
              162  POP_JUMP_IF_TRUE    184  'to 184'

 L. 378       164  LOAD_FAST                'scheme'
              166  LOAD_STR                 'wss'
              168  COMPARE_OP               ==
              170  POP_JUMP_IF_FALSE   176  'to 176'
              172  LOAD_CONST               443
              174  JUMP_FORWARD        178  'to 178'
            176_0  COME_FROM           170  '170'
              176  LOAD_CONST               80
            178_0  COME_FROM           174  '174'
              178  LOAD_FAST                'self'
              180  LOAD_ATTR                session
              182  STORE_ATTR               remote_port
            184_0  COME_FROM           162  '162'
            184_1  COME_FROM           154  '154'

 L. 379       184  LOAD_FAST                'scheme'
              186  LOAD_CONST               ('ws', 'wss')
              188  COMPARE_OP               in
          190_192  POP_JUMP_IF_FALSE   258  'to 258'

 L. 381       194  LOAD_FAST                'scheme'
              196  LOAD_FAST                'self'
              198  LOAD_ATTR                session
              200  LOAD_ATTR                remote_address
              202  LOAD_STR                 ':'
              204  BINARY_ADD       
              206  LOAD_GLOBAL              str
              208  LOAD_FAST                'self'
              210  LOAD_ATTR                session
              212  LOAD_ATTR                remote_port
              214  CALL_FUNCTION_1       1  ''
              216  BINARY_ADD       
              218  LOAD_FAST                'uri_attributes'
              220  LOAD_CONST               2
              222  BINARY_SUBSCR    

 L. 382       224  LOAD_FAST                'uri_attributes'
              226  LOAD_CONST               3
              228  BINARY_SUBSCR    

 L. 382       230  LOAD_FAST                'uri_attributes'
              232  LOAD_CONST               4
              234  BINARY_SUBSCR    

 L. 382       236  LOAD_FAST                'uri_attributes'
              238  LOAD_CONST               5
              240  BINARY_SUBSCR    

 L. 381       242  BUILD_TUPLE_6         6 
              244  STORE_FAST               'uri'

 L. 383       246  LOAD_GLOBAL              urlunparse
              248  LOAD_FAST                'uri'
              250  CALL_FUNCTION_1       1  ''
              252  LOAD_FAST                'self'
              254  LOAD_ATTR                session
              256  STORE_ATTR               broker_uri
            258_0  COME_FROM           190  '190'

 L. 386       258  LOAD_GLOBAL              ClientProtocolHandler
              260  LOAD_FAST                'self'
              262  LOAD_ATTR                plugins_manager
              264  LOAD_FAST                'self'
              266  LOAD_ATTR                _loop
              268  LOAD_CONST               ('loop',)
              270  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              272  LOAD_FAST                'self'
              274  STORE_ATTR               _handler

 L. 388       276  LOAD_FAST                'secure'
          278_280  POP_JUMP_IF_FALSE   414  'to 414'

 L. 389       282  LOAD_GLOBAL              ssl
              284  LOAD_ATTR                create_default_context

 L. 390       286  LOAD_GLOBAL              ssl
              288  LOAD_ATTR                Purpose
              290  LOAD_ATTR                SERVER_AUTH

 L. 391       292  LOAD_FAST                'self'
              294  LOAD_ATTR                session
              296  LOAD_ATTR                cafile

 L. 392       298  LOAD_FAST                'self'
              300  LOAD_ATTR                session
              302  LOAD_ATTR                capath

 L. 393       304  LOAD_FAST                'self'
              306  LOAD_ATTR                session
              308  LOAD_ATTR                cadata

 L. 389       310  LOAD_CONST               ('cafile', 'capath', 'cadata')
              312  CALL_FUNCTION_KW_4     4  '4 total positional and keyword args'
              314  STORE_FAST               'sc'

 L. 394       316  LOAD_STR                 'certfile'
              318  LOAD_FAST                'self'
              320  LOAD_ATTR                config
              322  COMPARE_OP               in
          324_326  POP_JUMP_IF_FALSE   364  'to 364'
              328  LOAD_STR                 'keyfile'
              330  LOAD_FAST                'self'
              332  LOAD_ATTR                config
              334  COMPARE_OP               in
          336_338  POP_JUMP_IF_FALSE   364  'to 364'

 L. 395       340  LOAD_FAST                'sc'
              342  LOAD_METHOD              load_cert_chain
              344  LOAD_FAST                'self'
              346  LOAD_ATTR                config
              348  LOAD_STR                 'certfile'
              350  BINARY_SUBSCR    
              352  LOAD_FAST                'self'
              354  LOAD_ATTR                config
              356  LOAD_STR                 'keyfile'
              358  BINARY_SUBSCR    
              360  CALL_METHOD_2         2  ''
              362  POP_TOP          
            364_0  COME_FROM           336  '336'
            364_1  COME_FROM           324  '324'

 L. 396       364  LOAD_STR                 'check_hostname'
              366  LOAD_FAST                'self'
              368  LOAD_ATTR                config
              370  COMPARE_OP               in
          372_374  POP_JUMP_IF_FALSE   406  'to 406'
              376  LOAD_GLOBAL              isinstance
              378  LOAD_FAST                'self'
              380  LOAD_ATTR                config
              382  LOAD_STR                 'check_hostname'
              384  BINARY_SUBSCR    
              386  LOAD_GLOBAL              bool
              388  CALL_FUNCTION_2       2  ''
          390_392  POP_JUMP_IF_FALSE   406  'to 406'

 L. 397       394  LOAD_FAST                'self'
              396  LOAD_ATTR                config
              398  LOAD_STR                 'check_hostname'
              400  BINARY_SUBSCR    
              402  LOAD_FAST                'sc'
              404  STORE_ATTR               check_hostname
            406_0  COME_FROM           390  '390'
            406_1  COME_FROM           372  '372'

 L. 398       406  LOAD_FAST                'sc'
              408  LOAD_FAST                'kwargs'
              410  LOAD_STR                 'ssl'
              412  STORE_SUBSCR     
            414_0  COME_FROM           278  '278'

 L. 400   414_416  SETUP_FINALLY       740  'to 740'

 L. 401       418  LOAD_CONST               None
              420  STORE_FAST               'reader'

 L. 402       422  LOAD_CONST               None
              424  STORE_FAST               'writer'

 L. 403       426  LOAD_FAST                'self'
              428  LOAD_ATTR                _connected_state
              430  LOAD_METHOD              clear
              432  CALL_METHOD_0         0  ''
              434  POP_TOP          

 L. 405       436  LOAD_FAST                'scheme'
              438  LOAD_CONST               ('mqtt', 'mqtts')
              440  COMPARE_OP               in
          442_444  POP_JUMP_IF_FALSE   508  'to 508'

 L. 407       446  LOAD_GLOBAL              asyncio
              448  LOAD_ATTR                open_connection

 L. 408       450  LOAD_FAST                'self'
              452  LOAD_ATTR                session
              454  LOAD_ATTR                remote_address

 L. 409       456  LOAD_FAST                'self'
              458  LOAD_ATTR                session
              460  LOAD_ATTR                remote_port

 L. 407       462  BUILD_TUPLE_2         2 
              464  LOAD_STR                 'loop'

 L. 409       466  LOAD_FAST                'self'
              468  LOAD_ATTR                _loop

 L. 407       470  BUILD_MAP_1           1 

 L. 409       472  LOAD_FAST                'kwargs'

 L. 407       474  BUILD_MAP_UNPACK_WITH_CALL_2     2 
              476  CALL_FUNCTION_EX_KW     1  'keyword and positional arguments'
              478  GET_YIELD_FROM_ITER
              480  LOAD_CONST               None
              482  YIELD_FROM       

 L. 406       484  UNPACK_SEQUENCE_2     2 
              486  STORE_FAST               'conn_reader'
              488  STORE_FAST               'conn_writer'

 L. 410       490  LOAD_GLOBAL              StreamReaderAdapter
              492  LOAD_FAST                'conn_reader'
              494  CALL_FUNCTION_1       1  ''
              496  STORE_FAST               'reader'

 L. 411       498  LOAD_GLOBAL              StreamWriterAdapter
              500  LOAD_FAST                'conn_writer'
              502  CALL_FUNCTION_1       1  ''
              504  STORE_FAST               'writer'
              506  JUMP_FORWARD        576  'to 576'
            508_0  COME_FROM           442  '442'

 L. 412       508  LOAD_FAST                'scheme'
              510  LOAD_CONST               ('ws', 'wss')
              512  COMPARE_OP               in
          514_516  POP_JUMP_IF_FALSE   576  'to 576'

 L. 413       518  LOAD_GLOBAL              websockets
              520  LOAD_ATTR                connect

 L. 414       522  LOAD_FAST                'self'
              524  LOAD_ATTR                session
              526  LOAD_ATTR                broker_uri

 L. 413       528  BUILD_TUPLE_1         1 

 L. 415       530  LOAD_STR                 'mqtt'
              532  BUILD_LIST_1          1 

 L. 416       534  LOAD_FAST                'self'
              536  LOAD_ATTR                _loop

 L. 417       538  LOAD_FAST                'self'
              540  LOAD_ATTR                extra_headers

 L. 413       542  LOAD_CONST               ('subprotocols', 'loop', 'extra_headers')
              544  BUILD_CONST_KEY_MAP_3     3 

 L. 418       546  LOAD_FAST                'kwargs'

 L. 413       548  BUILD_MAP_UNPACK_WITH_CALL_2     2 
              550  CALL_FUNCTION_EX_KW     1  'keyword and positional arguments'
              552  GET_YIELD_FROM_ITER
              554  LOAD_CONST               None
              556  YIELD_FROM       
              558  STORE_FAST               'websocket'

 L. 419       560  LOAD_GLOBAL              WebSocketsReader
              562  LOAD_FAST                'websocket'
              564  CALL_FUNCTION_1       1  ''
              566  STORE_FAST               'reader'

 L. 420       568  LOAD_GLOBAL              WebSocketsWriter
              570  LOAD_FAST                'websocket'
              572  CALL_FUNCTION_1       1  ''
              574  STORE_FAST               'writer'
            576_0  COME_FROM           514  '514'
            576_1  COME_FROM           506  '506'

 L. 422       576  LOAD_FAST                'self'
              578  LOAD_ATTR                _handler
              580  LOAD_METHOD              attach
              582  LOAD_FAST                'self'
              584  LOAD_ATTR                session
              586  LOAD_FAST                'reader'
              588  LOAD_FAST                'writer'
              590  CALL_METHOD_3         3  ''
              592  POP_TOP          

 L. 423       594  LOAD_FAST                'self'
              596  LOAD_ATTR                _handler
              598  LOAD_METHOD              mqtt_connect
              600  CALL_METHOD_0         0  ''
              602  GET_YIELD_FROM_ITER
              604  LOAD_CONST               None
              606  YIELD_FROM       
              608  STORE_FAST               'return_code'

 L. 424       610  LOAD_FAST                'return_code'
              612  LOAD_GLOBAL              CONNECTION_ACCEPTED
              614  COMPARE_OP               is-not
          616_618  POP_JUMP_IF_FALSE   668  'to 668'

 L. 425       620  LOAD_FAST                'self'
              622  LOAD_ATTR                session
              624  LOAD_ATTR                transitions
              626  LOAD_METHOD              disconnect
              628  CALL_METHOD_0         0  ''
              630  POP_TOP          

 L. 426       632  LOAD_FAST                'self'
              634  LOAD_ATTR                logger
              636  LOAD_METHOD              warning
              638  LOAD_STR                 "Connection rejected with code '%s'"
              640  LOAD_FAST                'return_code'
              642  BINARY_MODULO    
              644  CALL_METHOD_1         1  ''
              646  POP_TOP          

 L. 427       648  LOAD_GLOBAL              ConnectException
              650  LOAD_STR                 'Connection rejected by broker'
              652  CALL_FUNCTION_1       1  ''
              654  STORE_FAST               'exc'

 L. 428       656  LOAD_FAST                'return_code'
              658  LOAD_FAST                'exc'
              660  STORE_ATTR               return_code

 L. 429       662  LOAD_FAST                'exc'
              664  RAISE_VARARGS_1       1  'exception instance'
              666  JUMP_FORWARD        734  'to 734'
            668_0  COME_FROM           616  '616'

 L. 432       668  LOAD_FAST                'self'
              670  LOAD_ATTR                _handler
              672  LOAD_METHOD              start
              674  CALL_METHOD_0         0  ''
              676  GET_YIELD_FROM_ITER
              678  LOAD_CONST               None
              680  YIELD_FROM       
              682  POP_TOP          

 L. 433       684  LOAD_FAST                'self'
              686  LOAD_ATTR                session
              688  LOAD_ATTR                transitions
              690  LOAD_METHOD              connect
              692  CALL_METHOD_0         0  ''
              694  POP_TOP          

 L. 434       696  LOAD_FAST                'self'
              698  LOAD_ATTR                _connected_state
              700  LOAD_METHOD              set
              702  CALL_METHOD_0         0  ''
              704  POP_TOP          

 L. 435       706  LOAD_FAST                'self'
              708  LOAD_ATTR                logger
              710  LOAD_METHOD              debug
              712  LOAD_STR                 'connected to %s:%s'
              714  LOAD_FAST                'self'
              716  LOAD_ATTR                session
              718  LOAD_ATTR                remote_address
              720  LOAD_FAST                'self'
              722  LOAD_ATTR                session
              724  LOAD_ATTR                remote_port
              726  BUILD_TUPLE_2         2 
              728  BINARY_MODULO    
              730  CALL_METHOD_1         1  ''
              732  POP_TOP          
            734_0  COME_FROM           666  '666'

 L. 436       734  LOAD_FAST                'return_code'
              736  POP_BLOCK        
              738  RETURN_VALUE     
            740_0  COME_FROM_FINALLY   414  '414'

 L. 437       740  DUP_TOP          
              742  LOAD_GLOBAL              InvalidURI
              744  COMPARE_OP               exception-match
          746_748  POP_JUMP_IF_FALSE   824  'to 824'
              750  POP_TOP          
              752  STORE_FAST               'iuri'
              754  POP_TOP          
              756  SETUP_FINALLY       812  'to 812'

 L. 438       758  LOAD_FAST                'self'
              760  LOAD_ATTR                logger
              762  LOAD_METHOD              warning
              764  LOAD_STR                 "connection failed: invalid URI '%s'"
              766  LOAD_FAST                'self'
              768  LOAD_ATTR                session
              770  LOAD_ATTR                broker_uri
              772  BINARY_MODULO    
              774  CALL_METHOD_1         1  ''
              776  POP_TOP          

 L. 439       778  LOAD_FAST                'self'
              780  LOAD_ATTR                session
              782  LOAD_ATTR                transitions
              784  LOAD_METHOD              disconnect
              786  CALL_METHOD_0         0  ''
              788  POP_TOP          

 L. 440       790  LOAD_GLOBAL              ConnectException
              792  LOAD_STR                 "connection failed: invalid URI '%s'"
              794  LOAD_FAST                'self'
              796  LOAD_ATTR                session
              798  LOAD_ATTR                broker_uri
              800  BINARY_MODULO    
              802  LOAD_FAST                'iuri'
              804  CALL_FUNCTION_2       2  ''
              806  RAISE_VARARGS_1       1  'exception instance'
              808  POP_BLOCK        
              810  BEGIN_FINALLY    
            812_0  COME_FROM_FINALLY   756  '756'
              812  LOAD_CONST               None
              814  STORE_FAST               'iuri'
              816  DELETE_FAST              'iuri'
              818  END_FINALLY      
              820  POP_EXCEPT       
              822  JUMP_FORWARD        970  'to 970'
            824_0  COME_FROM           746  '746'

 L. 441       824  DUP_TOP          
              826  LOAD_GLOBAL              InvalidHandshake
              828  COMPARE_OP               exception-match
          830_832  POP_JUMP_IF_FALSE   892  'to 892'
              834  POP_TOP          
              836  STORE_FAST               'ihs'
              838  POP_TOP          
              840  SETUP_FINALLY       880  'to 880'

 L. 442       842  LOAD_FAST                'self'
              844  LOAD_ATTR                logger
              846  LOAD_METHOD              warning
              848  LOAD_STR                 'connection failed: invalid websocket handshake'
              850  CALL_METHOD_1         1  ''
              852  POP_TOP          

 L. 443       854  LOAD_FAST                'self'
              856  LOAD_ATTR                session
              858  LOAD_ATTR                transitions
              860  LOAD_METHOD              disconnect
              862  CALL_METHOD_0         0  ''
              864  POP_TOP          

 L. 444       866  LOAD_GLOBAL              ConnectException
              868  LOAD_STR                 'connection failed: invalid websocket handshake'
              870  LOAD_FAST                'ihs'
              872  CALL_FUNCTION_2       2  ''
              874  RAISE_VARARGS_1       1  'exception instance'
              876  POP_BLOCK        
              878  BEGIN_FINALLY    
            880_0  COME_FROM_FINALLY   840  '840'
              880  LOAD_CONST               None
              882  STORE_FAST               'ihs'
              884  DELETE_FAST              'ihs'
              886  END_FINALLY      
              888  POP_EXCEPT       
              890  JUMP_FORWARD        970  'to 970'
            892_0  COME_FROM           830  '830'

 L. 445       892  DUP_TOP          
              894  LOAD_GLOBAL              ProtocolHandlerException
              896  LOAD_GLOBAL              ConnectionError
              898  LOAD_GLOBAL              OSError
              900  BUILD_TUPLE_3         3 
              902  COMPARE_OP               exception-match
          904_906  POP_JUMP_IF_FALSE   968  'to 968'
              908  POP_TOP          
              910  STORE_FAST               'e'
              912  POP_TOP          
              914  SETUP_FINALLY       956  'to 956'

 L. 446       916  LOAD_FAST                'self'
              918  LOAD_ATTR                logger
              920  LOAD_METHOD              warning
              922  LOAD_STR                 'MQTT connection failed: %r'
              924  LOAD_FAST                'e'
              926  BINARY_MODULO    
              928  CALL_METHOD_1         1  ''
              930  POP_TOP          

 L. 447       932  LOAD_FAST                'self'
              934  LOAD_ATTR                session
              936  LOAD_ATTR                transitions
              938  LOAD_METHOD              disconnect
              940  CALL_METHOD_0         0  ''
              942  POP_TOP          

 L. 448       944  LOAD_GLOBAL              ConnectException
              946  LOAD_FAST                'e'
              948  CALL_FUNCTION_1       1  ''
              950  RAISE_VARARGS_1       1  'exception instance'
              952  POP_BLOCK        
              954  BEGIN_FINALLY    
            956_0  COME_FROM_FINALLY   914  '914'
              956  LOAD_CONST               None
              958  STORE_FAST               'e'
              960  DELETE_FAST              'e'
              962  END_FINALLY      
              964  POP_EXCEPT       
              966  JUMP_FORWARD        970  'to 970'
            968_0  COME_FROM           904  '904'
              968  END_FINALLY      
            970_0  COME_FROM           966  '966'
            970_1  COME_FROM           890  '890'
            970_2  COME_FROM           822  '822'

Parse error at or near `DUP_TOP' instruction at offset 824

    @asyncio.coroutine
    def handle_connection_close(self):

        def cancel_tasks():
            self._no_more_connections.set()
            while self.client_tasks:
                task = self.client_tasks.popleft()
                if not task.done():
                    task.set_exception(ClientException('Connection lost'))

        self.logger.debug('Watch broker disconnection')
        (yield from self._handler.wait_disconnect())
        self.logger.warning('Disconnected from broker')
        self._connected_state.clear()
        self._handler.detach()
        self.session.transitions.disconnect()
        if self.config.get'auto_reconnect'False:
            self.logger.debug('Auto-reconnecting')
            try:
                (yield from self.reconnect())
            except ConnectException:
                cancel_tasks()

        else:
            cancel_tasks()
        if False:
            yield None

    def _initsession(self, uri=None, cleansession=None, cafile=None, capath=None, cadata=None) -> Session:
        broker_conf = self.config.get'broker'dict().copy()
        if uri:
            broker_conf['uri'] = uri
        if cafile:
            broker_conf['cafile'] = cafile
        else:
            if 'cafile' not in broker_conf:
                broker_conf['cafile'] = None
            elif capath:
                broker_conf['capath'] = capath
            else:
                if 'capath' not in broker_conf:
                    broker_conf['capath'] = None
        if cadata:
            broker_conf['cadata'] = cadata
        else:
            if 'cadata' not in broker_conf:
                broker_conf['cadata'] = None
            else:
                if cleansession is not None:
                    broker_conf['cleansession'] = cleansession
                for key in ('uri', ):
                    if not_in_dict_or_none(broker_conf, key):
                        raise ClientException("Missing connection parameter '%s'" % key)
                else:
                    s = Session()
                    s.broker_uri = uri
                    s.client_id = self.client_id
                    s.cafile = broker_conf['cafile']
                    s.capath = broker_conf['capath']
                    s.cadata = broker_conf['cadata']
                    if cleansession is not None:
                        s.clean_session = cleansession
                    else:
                        s.clean_session = self.config.get'cleansession'True
                    s.keep_alive = self.config['keep_alive'] - self.config['ping_delay']
                    if 'will' in self.config:
                        s.will_flag = True
                        s.will_retain = self.config['will']['retain']
                        s.will_topic = self.config['will']['topic']
                        s.will_message = self.config['will']['message']
                        s.will_qos = self.config['will']['qos']
                    else:
                        s.will_flag = False
                    s.will_retain = False
                    s.will_topic = None
                    s.will_message = None

            return s