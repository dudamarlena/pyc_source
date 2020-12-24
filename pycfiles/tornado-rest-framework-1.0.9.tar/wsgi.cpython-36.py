# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /opt/work/lib/pyenv/versions/3.6.1/envs/passport/lib/python3.6/site-packages/rest_framework/core/wsgi.py
# Compiled at: 2018-08-22 04:46:34
# Size of source mod 2**32: 2838 bytes
from urllib.parse import unquote
from tornado import httputil
from tornado.wsgi import WSGIAdapter
from rest_framework.core.app import app_setup
from rest_framework.core.request import Request

class ClientDisconnect(Exception):
    pass


class ASGIAdapter:

    def __init__(self, application):
        self.application = application

    @staticmethod
    async def _stream(receive):
        while 1:
            message = await receive()
            if message['type'] == 'http.request':
                yield message.get('body', b'')
                if not message.get('more_body', False):
                    break
            else:
                if message['type'] == 'http.disconnect':
                    raise ClientDisconnect()

    def __call__(self, scope):
        print('--scope---', scope)

        async def asgi_callable--- This code section failed: ---

 L.  40         0  LOAD_GLOBAL              print
                2  LOAD_STR                 '---receive, send--'
                4  LOAD_FAST                'receive'
                6  LOAD_FAST                'send'
                8  CALL_FUNCTION_3       3  '3 positional arguments'
               10  POP_TOP          

 L.  41        12  LOAD_DICTCOMP            '<code_object <dictcomp>>'
               14  LOAD_STR                 'ASGIAdapter.__call__.<locals>.asgi_callable.<locals>.<dictcomp>'
               16  MAKE_FUNCTION_0          'Neither defaults, keyword-only args, annotations, nor closures'
               18  LOAD_DEREF               'scope'
               20  LOAD_STR                 'headers'
               22  BINARY_SUBSCR    
               24  GET_ITER         
               26  CALL_FUNCTION_1       1  '1 positional argument'
               28  STORE_FAST               'header_map'

 L.  42        30  LOAD_GLOBAL              httputil
               32  LOAD_ATTR                HTTPHeaders
               34  BUILD_TUPLE_0         0 
               36  LOAD_FAST                'header_map'
               38  CALL_FUNCTION_EX_KW     1  'keyword and positional arguments'
               40  STORE_FAST               'headers'

 L.  43        42  LOAD_CONST               b''
               44  STORE_FAST               'body'

 L.  44        46  SETUP_LOOP          112  'to 112'
               48  LOAD_DEREF               'self'
               50  LOAD_ATTR                _stream
               52  LOAD_FAST                'receive'
               54  CALL_FUNCTION_1       1  '1 positional argument'
               56  GET_AITER        
               58  LOAD_CONST               None
               60  YIELD_FROM       
               62  SETUP_EXCEPT         76  'to 76'
               64  GET_ANEXT        
               66  LOAD_CONST               None
               68  YIELD_FROM       
               70  STORE_FAST               'chunk'
               72  POP_BLOCK        
               74  JUMP_FORWARD         98  'to 98'
             76_0  COME_FROM_EXCEPT     62  '62'
               76  DUP_TOP          
               78  LOAD_GLOBAL              StopAsyncIteration
               80  COMPARE_OP               exception-match
               82  POP_JUMP_IF_FALSE    96  'to 96'
               84  POP_TOP          
               86  POP_TOP          
               88  POP_TOP          
               90  POP_EXCEPT       
               92  POP_BLOCK        
               94  JUMP_ABSOLUTE       112  'to 112'
               96  END_FINALLY      
             98_0  COME_FROM            74  '74'

 L.  45        98  LOAD_FAST                'body'
              100  LOAD_FAST                'chunk'
              102  INPLACE_ADD      
              104  STORE_FAST               'body'
              106  JUMP_BACK            62  'to 62'
              108  POP_BLOCK        
              110  JUMP_ABSOLUTE       112  'to 112'
            112_0  COME_FROM_LOOP       46  '46'

 L.  46       112  LOAD_GLOBAL              print
              114  LOAD_STR                 '---body---'
              116  LOAD_FAST                'body'
              118  CALL_FUNCTION_2       2  '2 positional arguments'
              120  POP_TOP          

 L.  47       122  LOAD_DEREF               'scope'
              124  LOAD_STR                 'method'
              126  BINARY_SUBSCR    
              128  STORE_FAST               'method'

 L.  48       130  LOAD_DEREF               'scope'
              132  LOAD_ATTR                get
              134  LOAD_STR                 'root_path'
              136  LOAD_STR                 ''
              138  CALL_FUNCTION_2       2  '2 positional arguments'
              140  LOAD_DEREF               'scope'
              142  LOAD_STR                 'path'
              144  BINARY_SUBSCR    
              146  BINARY_ADD       
              148  STORE_FAST               'uri'

 L.  49       150  LOAD_DEREF               'scope'
              152  LOAD_STR                 'query_string'
              154  BINARY_SUBSCR    
              156  STORE_FAST               'query_string'

 L.  50       158  LOAD_FAST                'query_string'
              160  POP_JUMP_IF_FALSE   182  'to 182'

 L.  51       162  LOAD_FAST                'uri'
              164  LOAD_STR                 '?'
              166  LOAD_GLOBAL              unquote
              168  LOAD_FAST                'query_string'
              170  LOAD_ATTR                decode
              172  CALL_FUNCTION_0       0  '0 positional arguments'
              174  CALL_FUNCTION_1       1  '1 positional argument'
              176  BINARY_ADD       
              178  INPLACE_ADD      
              180  STORE_FAST               'uri'
            182_0  COME_FROM           160  '160'

 L.  52       182  LOAD_DEREF               'scope'
              184  LOAD_STR                 'server'
              186  BINARY_SUBSCR    
              188  UNPACK_SEQUENCE_2     2 
              190  STORE_FAST               'host'
              192  STORE_FAST               'port'

 L.  53       194  LOAD_FAST                'host'
              196  FORMAT_VALUE          0  ''
              198  LOAD_STR                 ':'
              200  LOAD_FAST                'port'
              202  FORMAT_VALUE          0  ''
              204  BUILD_STRING_3        3 
              206  STORE_FAST               'hosts'

 L.  54       208  LOAD_GLOBAL              httputil
              210  LOAD_ATTR                HTTPServerRequest

 L.  55       212  LOAD_FAST                'method'
              214  LOAD_FAST                'uri'
              216  LOAD_STR                 'HTTP/1.1'
              218  LOAD_FAST                'headers'
              220  LOAD_FAST                'body'

 L.  56       222  LOAD_FAST                'hosts'
              224  LOAD_CONST               None
              226  LOAD_CONST               ('headers', 'body', 'host', 'connection')
              228  CALL_FUNCTION_KW_7     7  '7 total positional and keyword args'
              230  STORE_FAST               'request'

 L.  57       232  LOAD_FAST                'request'
              234  LOAD_ATTR                _parse_body
              236  CALL_FUNCTION_0       0  '0 positional arguments'
              238  POP_TOP          

 L.  58       240  LOAD_DEREF               'self'
              242  LOAD_ATTR                application
              244  LOAD_ATTR                find_handler
              246  LOAD_FAST                'request'
              248  CALL_FUNCTION_1       1  '1 positional argument'
              250  STORE_FAST               'dispatcher'

 L.  59       252  LOAD_GLOBAL              print
              254  LOAD_STR                 '--dispatcher--'
              256  LOAD_FAST                'dispatcher'
              258  CALL_FUNCTION_2       2  '2 positional arguments'
              260  POP_TOP          

Parse error at or near `JUMP_ABSOLUTE' instruction at offset 110

        return asgi_callable


def get_application(interface=b'asgi'):
    app = app_setup()
    if interface == b'asgi':
        return ASGIAdapter(app)
    else:
        return WSGIAdapter(app)