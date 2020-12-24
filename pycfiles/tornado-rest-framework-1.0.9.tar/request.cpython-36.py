# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /opt/work/lib/pyenv/versions/3.6.1/envs/maestro/lib/python3.6/site-packages/rest_framework/core/request.py
# Compiled at: 2018-10-19 23:03:13
# Size of source mod 2**32: 2798 bytes
import typing
from collections.abc import Mapping
from rest_framework.core.types import Scope, Receive
from rest_framework.utils.escape import json_decode
from rest_framework.core.datastructures import URL, Headers, QueryParams

class ClientDisconnect(Exception):
    pass


class Request(Mapping):

    def __init__(self, scope: Scope, receive: Receive=None) -> None:
        assert scope['type'] == 'http'
        self._scope = scope
        self._receive = receive
        self.context = {}
        self._stream_consumed = False

    def __getitem__(self, key: str) -> str:
        return self._scope[key]

    def __iter__(self) -> typing.Iterator[str]:
        return iter(self._scope)

    def __len__(self) -> int:
        return len(self._scope)

    @property
    def method(self) -> bytes:
        return self._scope['method'].encode()

    @property
    def url(self) -> URL:
        if not hasattr(self, '_url'):
            setattr(self, '_url', URL(scope=(self._scope)))
        return self._url

    @property
    def headers(self) -> Headers:
        if not hasattr(self, '_headers'):
            setattr(self, '_headers', Headers(self._scope['headers']))
        return self._headers

    @property
    def query_params(self) -> QueryParams:
        if not hasattr(self, '_query_params'):
            query_string = self._scope['query_string'].decode()
            setattr(self, '_query_params', QueryParams(query_string))
        return self._query_params

    async def stream(self) -> typing.AsyncGenerator[(bytes, None)]:
        if hasattr(self, '_body'):
            yield self._body
            return
        else:
            if self._stream_consumed:
                raise RuntimeError('Stream consumed')
            if self._receive is None:
                raise RuntimeError('Receive channel has not been made available')
        self._stream_consumed = True
        while 1:
            message = await self._receive()
            message_type = message['type']
            if message_type == 'http.request':
                yield message.get('body', b'')
                if not message.get('more_body', False):
                    break
            else:
                if message_type == 'http.disconnect':
                    raise ClientDisconnect()

    async def body--- This code section failed: ---

 L.  79         0  LOAD_GLOBAL              hasattr
                2  LOAD_FAST                'self'
                4  LOAD_STR                 '_body'
                6  CALL_FUNCTION_2       2  '2 positional arguments'
                8  POP_JUMP_IF_TRUE     90  'to 90'

 L.  80        10  LOAD_CONST               b''
               12  STORE_FAST               'body'

 L.  82        14  SETUP_LOOP           78  'to 78'
               16  LOAD_FAST                'self'
               18  LOAD_ATTR                stream
               20  CALL_FUNCTION_0       0  '0 positional arguments'
               22  GET_AITER        
               24  LOAD_CONST               None
               26  YIELD_FROM       
               28  SETUP_EXCEPT         42  'to 42'
               30  GET_ANEXT        
               32  LOAD_CONST               None
               34  YIELD_FROM       
               36  STORE_FAST               'chunk'
               38  POP_BLOCK        
               40  JUMP_FORWARD         64  'to 64'
             42_0  COME_FROM_EXCEPT     28  '28'
               42  DUP_TOP          
               44  LOAD_GLOBAL              StopAsyncIteration
               46  COMPARE_OP               exception-match
               48  POP_JUMP_IF_FALSE    62  'to 62'
               50  POP_TOP          
               52  POP_TOP          
               54  POP_TOP          
               56  POP_EXCEPT       
               58  POP_BLOCK        
               60  JUMP_ABSOLUTE        78  'to 78'
               62  END_FINALLY      
             64_0  COME_FROM            40  '40'

 L.  83        64  LOAD_FAST                'body'
               66  LOAD_FAST                'chunk'
               68  INPLACE_ADD      
               70  STORE_FAST               'body'
               72  JUMP_BACK            28  'to 28'
               74  POP_BLOCK        
               76  JUMP_ABSOLUTE        78  'to 78'
             78_0  COME_FROM_LOOP       14  '14'

 L.  85        78  LOAD_GLOBAL              setattr
               80  LOAD_FAST                'self'
               82  LOAD_STR                 '_body'
               84  LOAD_FAST                'body'
               86  CALL_FUNCTION_3       3  '3 positional arguments'
               88  POP_TOP          
             90_0  COME_FROM             8  '8'

 L.  87        90  LOAD_FAST                'self'
               92  LOAD_ATTR                _body
               94  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `JUMP_ABSOLUTE' instruction at offset 76

    async def json(self) -> typing.Any:
        if not hasattr(self, '_json'):
            body = await self.body()
            json_data = json_decode(body) if body else {}
            setattr(self, '_json', json_data)
        return self._json

    def client_ip(self):
        return self._scope['client'][0]