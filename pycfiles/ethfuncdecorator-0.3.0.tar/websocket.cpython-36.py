# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /private/var/folders/q3/1b9f00755fngs2554s60x4_h0000gn/T/pycharm-packaging/web3/web3/providers/websocket.py
# Compiled at: 2018-05-28 04:44:24
# Size of source mod 2**32: 2120 bytes
import asyncio, json, os
from threading import Thread
import websockets
from web3.providers.base import JSONBaseProvider

def _start_event_loop(loop):
    asyncio.set_event_loop(loop)
    loop.run_forever()
    loop.close()


def _get_threaded_loop():
    new_loop = asyncio.new_event_loop()
    thread_loop = Thread(target=_start_event_loop, args=(new_loop,), daemon=True)
    thread_loop.start()
    return new_loop


def get_default_endpoint():
    return os.environ.get('WEB3_WS_PROVIDER_URI', 'ws://127.0.0.1:8546')


class PersistentWebSocket:

    def __init__(self, endpoint_uri, loop):
        self.ws = None
        self.endpoint_uri = endpoint_uri
        self.loop = loop

    async def __aenter__(self):
        if self.ws is None:
            self.ws = await websockets.connect(uri=(self.endpoint_uri), loop=(self.loop))
        return self.ws

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if exc_val is not None:
            try:
                await self.ws.close()
            except Exception:
                pass

            self.ws = None


class WebsocketProvider(JSONBaseProvider):
    _loop = None

    def __init__(self, endpoint_uri=None):
        self.endpoint_uri = endpoint_uri
        if self.endpoint_uri is None:
            self.endpoint_uri = get_default_endpoint()
        if WebsocketProvider._loop is None:
            WebsocketProvider._loop = _get_threaded_loop()
        self.conn = PersistentWebSocket(self.endpoint_uri, WebsocketProvider._loop)
        super().__init__()

    def __str__(self):
        return 'WS connection {0}'.format(self.endpoint_uri)

    async def coro_make_request--- This code section failed: ---

 L.  70         0  LOAD_FAST                'self'
                2  LOAD_ATTR                conn
                4  BEFORE_ASYNC_WITH
                6  GET_AWAITABLE    
                8  LOAD_CONST               None
               10  YIELD_FROM       
               12  SETUP_ASYNC_WITH     52  'to 52'
               14  STORE_FAST               'conn'

 L.  71        16  LOAD_FAST                'conn'
               18  LOAD_ATTR                send
               20  LOAD_FAST                'request_data'
               22  CALL_FUNCTION_1       1  '1 positional argument'
               24  GET_AWAITABLE    
               26  LOAD_CONST               None
               28  YIELD_FROM       
               30  POP_TOP          

 L.  72        32  LOAD_GLOBAL              json
               34  LOAD_ATTR                loads
               36  LOAD_FAST                'conn'
               38  LOAD_ATTR                recv
               40  CALL_FUNCTION_0       0  '0 positional arguments'
               42  GET_AWAITABLE    
               44  LOAD_CONST               None
               46  YIELD_FROM       
               48  CALL_FUNCTION_1       1  '1 positional argument'
               50  RETURN_VALUE     
             52_0  COME_FROM_ASYNC_WITH    12  '12'
               52  WITH_CLEANUP_START
               54  GET_AWAITABLE    
               56  LOAD_CONST               None
               58  YIELD_FROM       
               60  WITH_CLEANUP_FINISH
               62  END_FINALLY      

Parse error at or near `WITH_CLEANUP_FINISH' instruction at offset 60

    def make_request(self, method, params):
        request_data = self.encode_rpc_request(method, params)
        future = asyncio.run_coroutine_threadsafe(self.coro_make_request(request_data), WebsocketProvider._loop)
        return future.result()