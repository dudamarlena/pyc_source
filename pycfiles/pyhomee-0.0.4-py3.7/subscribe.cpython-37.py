# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.14-x86_64/egg/pyhomee/subscribe.py
# Compiled at: 2019-08-04 06:38:55
# Size of source mod 2**32: 6377 bytes
"""Module to listen for homee events."""
import asyncio, collections, json, logging, sched, socket, ssl, threading, time
from asyncio import CancelledError
import websockets
from pyhomee.models import Attribute, Node, Group
_LOGGER = logging.getLogger(__name__)

class SubscriptionRegistry(object):
    __doc__ = 'Class for subscribing to homee events.'

    def __init__(self, cube, loop=None):
        """Setup websocket."""
        self.ws = None
        self.cube = cube
        self.hostname = cube.hostname
        self.connected = False
        self._nodes = {}
        self._groups = []
        self._node_callbacks = collections.defaultdict(list)
        self._callbacks = list()
        self._exiting = False
        self._event_loop_thread = None
        self._loop = loop or asyncio.get_event_loop()

    async def run(self):
        token = None
        while True:
            try:
                token = await self.cube.get_token()
                break
            except Exception as e:
                try:
                    _LOGGER.error('Failed to get homee token, trying again later: %s', e)
                    await asyncio.sleep(30)
                finally:
                    e = None
                    del e

        uri = 'ws://{}:7681/connection?access_token={}'.format(self.hostname, token)
        while True:
            try:
                self.connection = websockets.connect(uri, subprotocols=['v2'])
                async with self.connection as ws:
                    self.ws = ws
                    _LOGGER.info('Connected to websocket')
                    await ws.send(str('GET:all'))
                    while True:
                        try:
                            message = await ws.recv()
                        except (asyncio.TimeoutError, websockets.exceptions.ConnectionClosed):
                            try:
                                pong = await ws.ping()
                                await asyncio.wait_for(pong, timeout=30)
                                _LOGGER.debug('Ping OK, keeping connection alive...')
                                continue
                            except:
                                await asyncio.sleep(10)
                                break

                        await self.on_message(message)

            except socket.gaierror:
                _LOGGER.error('Websocket connection failed')
                continue
            except ConnectionRefusedError:
                _LOGGER.error('Websocket connection refused')
                continue
            except CancelledError:
                _LOGGER.error('Websocket client stopped')
                break

    def register(self, node, callback):
        """Register a callback.

        node: node to be updated by subscription
        callback: callback for notification of changes
        """
        if not node:
            _LOGGER.error('Received an invalid node: %r', node)
            return
        _LOGGER.debug('Subscribing to events for %s', node)
        self._node_callbacks[node.id].append(callback)

    def register_all(self, callback):
        """Register a callback to all received events

        callback: callback for notification of changes
        """
        _LOGGER.debug('Subscribing to all events %s')
        self._callbacks.append(callback)

    def start(self):
        """Start a thread to connect to homee websocket."""
        self._loop.run_until_complete(self.run())
        self._loop.run_forever()
        self._loop.close()
        _LOGGER.info('Thread started')

    async def send_command(self, command):
        try:
            await self.ws.send(command)
        except:
            _LOGGER.info('Sending command failed, restarting')

    async def send_node_command(self, node, attribute, target_value):
        return await self.send_command('PUT:nodes/{}/attributes/{}?target_value={}'.format(node.id, attribute.id, target_value))

    async def play_homeegram(self, id):
        return await self.send_command('PUT:homeegrams/{}?play=1'.format(id))

    def _run_event_loop(self):
        token = self.cube.get_token()
        self.ws = websocket.WebSocketApp(('ws://{}:7681/connection?access_token={}'.format(self.hostname, token)), subprotocols=[
         'v2'],
          on_message=(self.on_message),
          on_error=(self.on_error),
          on_close=(self.on_close))
        self.ws.on_open = self.on_open
        self.ws.run_forever()

    async def on_message--- This code section failed: ---

 L. 136         0  LOAD_FAST                'message'
                2  LOAD_STR                 'pong'
                4  COMPARE_OP               ==
                6  POP_JUMP_IF_FALSE    28  'to 28'

 L. 137         8  LOAD_CONST               True
               10  LOAD_FAST                'self'
               12  STORE_ATTR               connected

 L. 138        14  LOAD_GLOBAL              _LOGGER
               16  LOAD_METHOD              debug
               18  LOAD_STR                 'pong received'
               20  CALL_METHOD_1         1  '1 positional argument'
               22  POP_TOP          

 L. 139        24  LOAD_CONST               None
               26  RETURN_VALUE     
             28_0  COME_FROM             6  '6'

 L. 140        28  SETUP_EXCEPT         44  'to 44'

 L. 141        30  LOAD_GLOBAL              json
               32  LOAD_METHOD              loads
               34  LOAD_FAST                'message'
               36  CALL_METHOD_1         1  '1 positional argument'
               38  STORE_FAST               'parsed'
               40  POP_BLOCK        
               42  JUMP_FORWARD         96  'to 96'
             44_0  COME_FROM_EXCEPT     28  '28'

 L. 142        44  DUP_TOP          
               46  LOAD_GLOBAL              Exception
               48  COMPARE_OP               exception-match
               50  POP_JUMP_IF_FALSE    94  'to 94'
               52  POP_TOP          
               54  STORE_FAST               'e'
               56  POP_TOP          
               58  SETUP_FINALLY        82  'to 82'

 L. 143        60  LOAD_GLOBAL              _LOGGER
               62  LOAD_METHOD              error
               64  LOAD_STR                 'Failed to parse json: '
               66  LOAD_GLOBAL              str
               68  LOAD_FAST                'e'
               70  CALL_FUNCTION_1       1  '1 positional argument'
               72  BINARY_ADD       
               74  CALL_METHOD_1         1  '1 positional argument'
               76  POP_TOP          

 L. 144        78  LOAD_CONST               None
               80  RETURN_VALUE     
             82_0  COME_FROM_FINALLY    58  '58'
               82  LOAD_CONST               None
               84  STORE_FAST               'e'
               86  DELETE_FAST              'e'
               88  END_FINALLY      
               90  POP_EXCEPT       
               92  JUMP_FORWARD         96  'to 96'
             94_0  COME_FROM            50  '50'
               94  END_FINALLY      
             96_0  COME_FROM            92  '92'
             96_1  COME_FROM            42  '42'

 L. 145        96  LOAD_STR                 'all'
               98  LOAD_FAST                'parsed'
              100  COMPARE_OP               in
              102  POP_JUMP_IF_FALSE   198  'to 198'

 L. 146       104  LOAD_STR                 'nodes'
              106  LOAD_FAST                'parsed'
              108  LOAD_STR                 'all'
              110  BINARY_SUBSCR    
              112  COMPARE_OP               in
              114  POP_JUMP_IF_FALSE   148  'to 148'

 L. 147       116  SETUP_LOOP          148  'to 148'
              118  LOAD_FAST                'parsed'
              120  LOAD_STR                 'all'
              122  BINARY_SUBSCR    
              124  LOAD_STR                 'nodes'
              126  BINARY_SUBSCR    
              128  GET_ITER         
              130  FOR_ITER            146  'to 146'
              132  STORE_FAST               'node'

 L. 148       134  LOAD_FAST                'self'
              136  LOAD_METHOD              _parse_node
              138  LOAD_FAST                'node'
              140  CALL_METHOD_1         1  '1 positional argument'
              142  POP_TOP          
              144  JUMP_BACK           130  'to 130'
              146  POP_BLOCK        
            148_0  COME_FROM_LOOP      116  '116'
            148_1  COME_FROM           114  '114'

 L. 149       148  LOAD_STR                 'groups'
              150  LOAD_FAST                'parsed'
              152  LOAD_STR                 'all'
              154  BINARY_SUBSCR    
              156  COMPARE_OP               in
              158  POP_JUMP_IF_FALSE   198  'to 198'

 L. 150       160  SETUP_LOOP          198  'to 198'
              162  LOAD_FAST                'parsed'
              164  LOAD_STR                 'all'
              166  BINARY_SUBSCR    
              168  LOAD_STR                 'groups'
              170  BINARY_SUBSCR    
              172  GET_ITER         
              174  FOR_ITER            196  'to 196'
              176  STORE_FAST               'group'

 L. 151       178  LOAD_FAST                'self'
              180  LOAD_ATTR                _groups
              182  LOAD_METHOD              append
              184  LOAD_GLOBAL              Group
              186  LOAD_FAST                'group'
              188  CALL_FUNCTION_1       1  '1 positional argument'
              190  CALL_METHOD_1         1  '1 positional argument'
              192  POP_TOP          
              194  JUMP_BACK           174  'to 174'
              196  POP_BLOCK        
            198_0  COME_FROM_LOOP      160  '160'
            198_1  COME_FROM           158  '158'
            198_2  COME_FROM           102  '102'

 L. 153       198  LOAD_STR                 'node'
              200  LOAD_FAST                'parsed'
              202  COMPARE_OP               in
              204  POP_JUMP_IF_FALSE   220  'to 220'

 L. 154       206  LOAD_FAST                'self'
              208  LOAD_METHOD              _parse_node
              210  LOAD_FAST                'parsed'
              212  LOAD_STR                 'node'
              214  BINARY_SUBSCR    
              216  CALL_METHOD_1         1  '1 positional argument'
              218  POP_TOP          
            220_0  COME_FROM           204  '204'

 L. 156       220  LOAD_STR                 'attribute'
              222  LOAD_FAST                'parsed'
              224  COMPARE_OP               in
          226_228  POP_JUMP_IF_FALSE   300  'to 300'

 L. 157       230  LOAD_GLOBAL              Attribute
              232  LOAD_FAST                'parsed'
              234  LOAD_STR                 'attribute'
              236  BINARY_SUBSCR    
              238  CALL_FUNCTION_1       1  '1 positional argument'
              240  STORE_FAST               'attribute'

 L. 158       242  LOAD_FAST                'attribute'
              244  LOAD_ATTR                node_id
              246  LOAD_FAST                'self'
              248  LOAD_ATTR                _node_callbacks
              250  COMPARE_OP               in
          252_254  POP_JUMP_IF_FALSE   300  'to 300'

 L. 159       256  SETUP_LOOP          300  'to 300'
              258  LOAD_FAST                'self'
              260  LOAD_ATTR                _node_callbacks
              262  LOAD_FAST                'attribute'
              264  LOAD_ATTR                node_id
              266  BINARY_SUBSCR    
              268  GET_ITER         
              270  FOR_ITER            296  'to 296'
              272  STORE_FAST               'callback'

 L. 160       274  LOAD_FAST                'self'
              276  LOAD_ATTR                _loop
              278  LOAD_METHOD              create_task
              280  LOAD_FAST                'callback'
              282  LOAD_CONST               None
              284  LOAD_FAST                'attribute'
              286  CALL_FUNCTION_2       2  '2 positional arguments'
              288  CALL_METHOD_1         1  '1 positional argument'
              290  POP_TOP          
          292_294  JUMP_BACK           270  'to 270'
              296  POP_BLOCK        
              298  JUMP_FORWARD        300  'to 300'
            300_0  COME_FROM           298  '298'
            300_1  COME_FROM_LOOP      256  '256'
            300_2  COME_FROM           252  '252'
            300_3  COME_FROM           226  '226'

Parse error at or near `COME_FROM' instruction at offset 300_2

    def _parse_node(self, parsed):
        node = Node(parsed)
        self._nodes[node.id] = node
        for callback in self._callbacks:
            self._loop.create_task(callback(node))

        if node.id in self._node_callbacks:
            for callback in self._node_callbacks[node.id]:
                self._loop.create_task(callbacknodeNone)

    def on_error(self, error):
        _LOGGER.error('Websocket Error %s', error)
        self.restart()

    def on_close(self):
        pass

    def on_open(self):
        _LOGGER.info('Websocket opened')
        self.connected = True
        self.ping()