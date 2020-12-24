# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\ksoftapi\http.py
# Compiled at: 2020-04-19 15:03:20
# Size of source mod 2**32: 3004 bytes
import logging, sys, aiohttp
from . import __version__
from .errors import APIError
logger = logging.getLogger()

class HttpClient:
    BASE = 'https://api.ksoft.si'

    def __init__(self, authorization, loop):
        self._default_headers = {'Authorization':'Bearer ' + authorization, 
         'User-Agent':'KSoftApi.py/{} (https://github.com/KSoft-Si/ksoftapi.py)'.format(__version__), 
         'X-Powered-By':'aiohttp {}/Python {}'.format(aiohttp.__version__, sys.version)}
        self._session = aiohttp.ClientSession(loop=loop)

    async def close(self):
        await self._session.close()

    async def _validate_response(self, response: aiohttp.ClientResponse):
        if response.status >= 500:
            raise APIError(response.status, 'The API encountered an internal server error.')
        if 'content-type' in response.headers:
            if response.headers['content-type'] == 'application/json':
                json = await response.json()
                if json.get('error', False):
                    code = json.get('code', response.status)
                    message = json.get('message', '<No message>')
                    raise APIError(code, message)

    async def get--- This code section failed: ---

 L.  46         0  LOAD_FAST                'headers'
                2  POP_JUMP_IF_FALSE    14  'to 14'
                4  LOAD_FAST                'headers'
                6  LOAD_FAST                'self'
                8  LOAD_ATTR                _default_headers
               10  BUILD_MAP_UNPACK_2     2 
               12  JUMP_FORWARD         18  'to 18'
             14_0  COME_FROM             2  '2'
               14  LOAD_FAST                'self'
               16  LOAD_ATTR                _default_headers
             18_0  COME_FROM            12  '12'
               18  STORE_FAST               'merged_headers'

 L.  48        20  LOAD_FAST                'params'
               22  POP_JUMP_IF_FALSE    68  'to 68'

 L.  49        24  LOAD_FAST                'params'
               26  LOAD_METHOD              items
               28  CALL_METHOD_0         0  ''
               30  GET_ITER         
             32_0  COME_FROM            48  '48'
               32  FOR_ITER             68  'to 68'
               34  UNPACK_SEQUENCE_2     2 
               36  STORE_FAST               'key'
               38  STORE_FAST               'val'

 L.  50        40  LOAD_GLOBAL              isinstance
               42  LOAD_FAST                'val'
               44  LOAD_GLOBAL              bool
               46  CALL_FUNCTION_2       2  ''
               48  POP_JUMP_IF_FALSE    32  'to 32'

 L.  51        50  LOAD_GLOBAL              str
               52  LOAD_FAST                'val'
               54  CALL_FUNCTION_1       1  ''
               56  LOAD_METHOD              lower
               58  CALL_METHOD_0         0  ''
               60  LOAD_FAST                'params'
               62  LOAD_FAST                'key'
               64  STORE_SUBSCR     
               66  JUMP_BACK            32  'to 32'
             68_0  COME_FROM            22  '22'

 L.  53        68  LOAD_FAST                'self'
               70  LOAD_ATTR                _session
               72  LOAD_ATTR                get
               74  LOAD_FAST                'self'
               76  LOAD_ATTR                BASE
               78  LOAD_FAST                'path'
               80  BINARY_ADD       
               82  LOAD_FAST                'params'
               84  LOAD_FAST                'merged_headers'
               86  LOAD_CONST               ('params', 'headers')
               88  CALL_FUNCTION_KW_3     3  '3 total positional and keyword args'
               90  BEFORE_ASYNC_WITH
               92  GET_AWAITABLE    
               94  LOAD_CONST               None
               96  YIELD_FROM       
               98  SETUP_ASYNC_WITH    186  'to 186'
              100  STORE_FAST               'res'

 L.  54       102  LOAD_FAST                'self'
              104  LOAD_METHOD              _validate_response
              106  LOAD_FAST                'res'
              108  CALL_METHOD_1         1  ''
              110  GET_AWAITABLE    
              112  LOAD_CONST               None
              114  YIELD_FROM       
              116  POP_TOP          

 L.  56       118  LOAD_FAST                'to_json'
              120  POP_JUMP_IF_FALSE   154  'to 154'

 L.  57       122  LOAD_FAST                'res'
              124  LOAD_METHOD              json
              126  CALL_METHOD_0         0  ''
              128  GET_AWAITABLE    
              130  LOAD_CONST               None
              132  YIELD_FROM       
              134  POP_BLOCK        
              136  ROT_TWO          
              138  BEGIN_FINALLY    
              140  WITH_CLEANUP_START
              142  GET_AWAITABLE    
              144  LOAD_CONST               None
              146  YIELD_FROM       
              148  WITH_CLEANUP_FINISH
              150  POP_FINALLY           0  ''
              152  RETURN_VALUE     
            154_0  COME_FROM           120  '120'

 L.  59       154  LOAD_FAST                'res'
              156  LOAD_METHOD              text
              158  CALL_METHOD_0         0  ''
              160  GET_AWAITABLE    
              162  LOAD_CONST               None
              164  YIELD_FROM       
              166  POP_BLOCK        
              168  ROT_TWO          
              170  BEGIN_FINALLY    
              172  WITH_CLEANUP_START
              174  GET_AWAITABLE    
              176  LOAD_CONST               None
              178  YIELD_FROM       
              180  WITH_CLEANUP_FINISH
              182  POP_FINALLY           0  ''
              184  RETURN_VALUE     
            186_0  COME_FROM_ASYNC_WITH    98  '98'
              186  WITH_CLEANUP_START
              188  GET_AWAITABLE    
              190  LOAD_CONST               None
              192  YIELD_FROM       
              194  WITH_CLEANUP_FINISH
              196  END_FINALLY      

Parse error at or near `ROT_TWO' instruction at offset 136

    async def post--- This code section failed: ---

 L.  62         0  LOAD_FAST                'headers'
                2  POP_JUMP_IF_FALSE    14  'to 14'
                4  LOAD_FAST                'headers'
                6  LOAD_FAST                'self'
                8  LOAD_ATTR                _default_headers
               10  BUILD_MAP_UNPACK_2     2 
               12  JUMP_FORWARD         18  'to 18'
             14_0  COME_FROM             2  '2'
               14  LOAD_FAST                'self'
               16  LOAD_ATTR                _default_headers
             18_0  COME_FROM            12  '12'
               18  STORE_FAST               'merged_headers'

 L.  63        20  LOAD_GLOBAL              isinstance
               22  LOAD_FAST                'body'
               24  LOAD_GLOBAL              dict
               26  CALL_FUNCTION_2       2  ''
               28  POP_JUMP_IF_FALSE    38  'to 38'
               30  LOAD_STR                 'json'
               32  LOAD_FAST                'body'
               34  BUILD_MAP_1           1 
               36  JUMP_FORWARD         44  'to 44'
             38_0  COME_FROM            28  '28'
               38  LOAD_STR                 'data'
               40  LOAD_FAST                'body'
               42  BUILD_MAP_1           1 
             44_0  COME_FROM            36  '36'
               44  STORE_FAST               'payload'

 L.  64        46  LOAD_FAST                'self'
               48  LOAD_ATTR                _session
               50  LOAD_ATTR                post
               52  LOAD_FAST                'self'
               54  LOAD_ATTR                BASE
               56  LOAD_FAST                'path'
               58  BINARY_ADD       
               60  BUILD_TUPLE_1         1 
               62  LOAD_FAST                'payload'
               64  LOAD_STR                 'headers'
               66  LOAD_FAST                'merged_headers'
               68  BUILD_MAP_1           1 
               70  BUILD_MAP_UNPACK_WITH_CALL_2     2 
               72  CALL_FUNCTION_EX_KW     1  'keyword and positional arguments'
               74  BEFORE_ASYNC_WITH
               76  GET_AWAITABLE    
               78  LOAD_CONST               None
               80  YIELD_FROM       
               82  SETUP_ASYNC_WITH    170  'to 170'
               84  STORE_FAST               'res'

 L.  65        86  LOAD_FAST                'self'
               88  LOAD_METHOD              _validate_response
               90  LOAD_FAST                'res'
               92  CALL_METHOD_1         1  ''
               94  GET_AWAITABLE    
               96  LOAD_CONST               None
               98  YIELD_FROM       
              100  POP_TOP          

 L.  67       102  LOAD_FAST                'to_json'
              104  POP_JUMP_IF_FALSE   138  'to 138'

 L.  68       106  LOAD_FAST                'res'
              108  LOAD_METHOD              json
              110  CALL_METHOD_0         0  ''
              112  GET_AWAITABLE    
              114  LOAD_CONST               None
              116  YIELD_FROM       
              118  POP_BLOCK        
              120  ROT_TWO          
              122  BEGIN_FINALLY    
              124  WITH_CLEANUP_START
              126  GET_AWAITABLE    
              128  LOAD_CONST               None
              130  YIELD_FROM       
              132  WITH_CLEANUP_FINISH
              134  POP_FINALLY           0  ''
              136  RETURN_VALUE     
            138_0  COME_FROM           104  '104'

 L.  70       138  LOAD_FAST                'res'
              140  LOAD_METHOD              text
              142  CALL_METHOD_0         0  ''
              144  GET_AWAITABLE    
              146  LOAD_CONST               None
              148  YIELD_FROM       
              150  POP_BLOCK        
              152  ROT_TWO          
              154  BEGIN_FINALLY    
              156  WITH_CLEANUP_START
              158  GET_AWAITABLE    
              160  LOAD_CONST               None
              162  YIELD_FROM       
              164  WITH_CLEANUP_FINISH
              166  POP_FINALLY           0  ''
              168  RETURN_VALUE     
            170_0  COME_FROM_ASYNC_WITH    82  '82'
              170  WITH_CLEANUP_START
              172  GET_AWAITABLE    
              174  LOAD_CONST               None
              176  YIELD_FROM       
              178  WITH_CLEANUP_FINISH
              180  END_FINALLY      

Parse error at or near `ROT_TWO' instruction at offset 120

    async def delete--- This code section failed: ---

 L.  73         0  LOAD_FAST                'headers'
                2  POP_JUMP_IF_FALSE    14  'to 14'
                4  LOAD_FAST                'headers'
                6  LOAD_FAST                'self'
                8  LOAD_ATTR                _default_headers
               10  BUILD_MAP_UNPACK_2     2 
               12  JUMP_FORWARD         18  'to 18'
             14_0  COME_FROM             2  '2'
               14  LOAD_FAST                'self'
               16  LOAD_ATTR                _default_headers
             18_0  COME_FROM            12  '12'
               18  STORE_FAST               'merged_headers'

 L.  74        20  LOAD_FAST                'self'
               22  LOAD_ATTR                _session
               24  LOAD_ATTR                delete
               26  LOAD_FAST                'self'
               28  LOAD_ATTR                BASE
               30  LOAD_FAST                'path'
               32  BINARY_ADD       
               34  LOAD_FAST                'params'
               36  LOAD_FAST                'merged_headers'
               38  LOAD_CONST               ('params', 'headers')
               40  CALL_FUNCTION_KW_3     3  '3 total positional and keyword args'
               42  BEFORE_ASYNC_WITH
               44  GET_AWAITABLE    
               46  LOAD_CONST               None
               48  YIELD_FROM       
               50  SETUP_ASYNC_WITH    138  'to 138'
               52  STORE_FAST               'res'

 L.  75        54  LOAD_FAST                'self'
               56  LOAD_METHOD              _validate_response
               58  LOAD_FAST                'res'
               60  CALL_METHOD_1         1  ''
               62  GET_AWAITABLE    
               64  LOAD_CONST               None
               66  YIELD_FROM       
               68  POP_TOP          

 L.  77        70  LOAD_FAST                'to_json'
               72  POP_JUMP_IF_FALSE   106  'to 106'

 L.  78        74  LOAD_FAST                'res'
               76  LOAD_METHOD              json
               78  CALL_METHOD_0         0  ''
               80  GET_AWAITABLE    
               82  LOAD_CONST               None
               84  YIELD_FROM       
               86  POP_BLOCK        
               88  ROT_TWO          
               90  BEGIN_FINALLY    
               92  WITH_CLEANUP_START
               94  GET_AWAITABLE    
               96  LOAD_CONST               None
               98  YIELD_FROM       
              100  WITH_CLEANUP_FINISH
              102  POP_FINALLY           0  ''
              104  RETURN_VALUE     
            106_0  COME_FROM            72  '72'

 L.  80       106  LOAD_FAST                'res'
              108  LOAD_METHOD              text
              110  CALL_METHOD_0         0  ''
              112  GET_AWAITABLE    
              114  LOAD_CONST               None
              116  YIELD_FROM       
              118  POP_BLOCK        
              120  ROT_TWO          
              122  BEGIN_FINALLY    
              124  WITH_CLEANUP_START
              126  GET_AWAITABLE    
              128  LOAD_CONST               None
              130  YIELD_FROM       
              132  WITH_CLEANUP_FINISH
              134  POP_FINALLY           0  ''
              136  RETURN_VALUE     
            138_0  COME_FROM_ASYNC_WITH    50  '50'
              138  WITH_CLEANUP_START
              140  GET_AWAITABLE    
              142  LOAD_CONST               None
              144  YIELD_FROM       
              146  WITH_CLEANUP_FINISH
              148  END_FINALLY      

Parse error at or near `ROT_TWO' instruction at offset 88