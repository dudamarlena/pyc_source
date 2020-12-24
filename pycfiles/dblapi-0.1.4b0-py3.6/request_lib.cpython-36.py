# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\dblapi\request_lib.py
# Compiled at: 2018-03-18 13:07:26
# Size of source mod 2**32: 3443 bytes
import sys, traceback, aiohttp
from dblapi import __version__

class krequest(object):

    def __init__(self, return_json=True, global_headers=[]):
        self.headers = {'User-Agent':'DBLAPI/{} (Github: AndyTempel) KRequests/alpha (Custom asynchronous HTTP client)'.format(__version__), 
         'X-Powered-By':'Python {}'.format(sys.version)}
        self.return_json = return_json
        for name, value in global_headers:
            self.headers.update({name: value})

    async def _proc_resp(self, response):
        if self.return_json:
            try:
                return await response.json()
            except Exception:
                print(traceback.format_exc())
                print(response)
                return {}

        else:
            return await response.text()

    async def get--- This code section failed: ---

 L.  53         0  LOAD_FAST                'headers'
                2  JUMP_IF_TRUE_OR_POP     6  'to 6'
                4  BUILD_MAP_0           0 
              6_0  COME_FROM             2  '2'
                6  STORE_FAST               'headers'

 L.  54         8  LOAD_FAST                'headers'
               10  LOAD_ATTR                update
               12  LOAD_FAST                'self'
               14  LOAD_ATTR                headers
               16  CALL_FUNCTION_1       1  '1 positional argument'
               18  POP_TOP          

 L.  55        20  LOAD_GLOBAL              aiohttp
               22  LOAD_ATTR                ClientSession
               24  LOAD_GLOBAL              aiohttp
               26  LOAD_ATTR                TCPConnector
               28  LOAD_FAST                'verify'
               30  LOAD_CONST               ('verify_ssl',)
               32  CALL_FUNCTION_KW_1     1  '1 total positional and keyword args'
               34  LOAD_CONST               ('connector',)
               36  CALL_FUNCTION_KW_1     1  '1 total positional and keyword args'
               38  BEFORE_ASYNC_WITH
               40  GET_AWAITABLE    
               42  LOAD_CONST               None
               44  YIELD_FROM       
               46  SETUP_ASYNC_WITH    108  'to 108'
               48  STORE_FAST               'session'

 L.  56        50  LOAD_FAST                'session'
               52  LOAD_ATTR                get
               54  LOAD_FAST                'url'
               56  LOAD_FAST                'params'
               58  LOAD_FAST                'headers'
               60  LOAD_CONST               ('params', 'headers')
               62  CALL_FUNCTION_KW_3     3  '3 total positional and keyword args'
               64  BEFORE_ASYNC_WITH
               66  GET_AWAITABLE    
               68  LOAD_CONST               None
               70  YIELD_FROM       
               72  SETUP_ASYNC_WITH     92  'to 92'
               74  STORE_FAST               'resp'

 L.  57        76  LOAD_FAST                'self'
               78  LOAD_ATTR                _proc_resp
               80  LOAD_FAST                'resp'
               82  CALL_FUNCTION_1       1  '1 positional argument'
               84  GET_AWAITABLE    
               86  LOAD_CONST               None
               88  YIELD_FROM       
               90  RETURN_VALUE     
             92_0  COME_FROM_ASYNC_WITH    72  '72'
               92  WITH_CLEANUP_START
               94  GET_AWAITABLE    
               96  LOAD_CONST               None
               98  YIELD_FROM       
              100  WITH_CLEANUP_FINISH
              102  END_FINALLY      
              104  POP_BLOCK        
              106  LOAD_CONST               None
            108_0  COME_FROM_ASYNC_WITH    46  '46'
              108  WITH_CLEANUP_START
              110  GET_AWAITABLE    
              112  LOAD_CONST               None
              114  YIELD_FROM       
              116  WITH_CLEANUP_FINISH
              118  END_FINALLY      

Parse error at or near `COME_FROM_ASYNC_WITH' instruction at offset 92_0

    async def delete--- This code section failed: ---

 L.  60         0  LOAD_FAST                'headers'
                2  JUMP_IF_TRUE_OR_POP     6  'to 6'
                4  BUILD_MAP_0           0 
              6_0  COME_FROM             2  '2'
                6  STORE_FAST               'headers'

 L.  61         8  LOAD_FAST                'headers'
               10  LOAD_ATTR                update
               12  LOAD_FAST                'self'
               14  LOAD_ATTR                headers
               16  CALL_FUNCTION_1       1  '1 positional argument'
               18  POP_TOP          

 L.  62        20  LOAD_GLOBAL              aiohttp
               22  LOAD_ATTR                ClientSession
               24  LOAD_GLOBAL              aiohttp
               26  LOAD_ATTR                TCPConnector
               28  LOAD_FAST                'verify'
               30  LOAD_CONST               ('verify_ssl',)
               32  CALL_FUNCTION_KW_1     1  '1 total positional and keyword args'
               34  LOAD_CONST               ('connector',)
               36  CALL_FUNCTION_KW_1     1  '1 total positional and keyword args'
               38  BEFORE_ASYNC_WITH
               40  GET_AWAITABLE    
               42  LOAD_CONST               None
               44  YIELD_FROM       
               46  SETUP_ASYNC_WITH    108  'to 108'
               48  STORE_FAST               'session'

 L.  63        50  LOAD_FAST                'session'
               52  LOAD_ATTR                delete
               54  LOAD_FAST                'url'
               56  LOAD_FAST                'params'
               58  LOAD_FAST                'headers'
               60  LOAD_CONST               ('params', 'headers')
               62  CALL_FUNCTION_KW_3     3  '3 total positional and keyword args'
               64  BEFORE_ASYNC_WITH
               66  GET_AWAITABLE    
               68  LOAD_CONST               None
               70  YIELD_FROM       
               72  SETUP_ASYNC_WITH     92  'to 92'
               74  STORE_FAST               'resp'

 L.  64        76  LOAD_FAST                'self'
               78  LOAD_ATTR                _proc_resp
               80  LOAD_FAST                'resp'
               82  CALL_FUNCTION_1       1  '1 positional argument'
               84  GET_AWAITABLE    
               86  LOAD_CONST               None
               88  YIELD_FROM       
               90  RETURN_VALUE     
             92_0  COME_FROM_ASYNC_WITH    72  '72'
               92  WITH_CLEANUP_START
               94  GET_AWAITABLE    
               96  LOAD_CONST               None
               98  YIELD_FROM       
              100  WITH_CLEANUP_FINISH
              102  END_FINALLY      
              104  POP_BLOCK        
              106  LOAD_CONST               None
            108_0  COME_FROM_ASYNC_WITH    46  '46'
              108  WITH_CLEANUP_START
              110  GET_AWAITABLE    
              112  LOAD_CONST               None
              114  YIELD_FROM       
              116  WITH_CLEANUP_FINISH
              118  END_FINALLY      

Parse error at or near `COME_FROM_ASYNC_WITH' instruction at offset 92_0

    async def post--- This code section failed: ---

 L.  67         0  LOAD_FAST                'headers'
                2  JUMP_IF_TRUE_OR_POP     6  'to 6'
                4  BUILD_MAP_0           0 
              6_0  COME_FROM             2  '2'
                6  STORE_FAST               'headers'

 L.  68         8  LOAD_FAST                'headers'
               10  LOAD_ATTR                update
               12  LOAD_FAST                'self'
               14  LOAD_ATTR                headers
               16  CALL_FUNCTION_1       1  '1 positional argument'
               18  POP_TOP          

 L.  69        20  LOAD_GLOBAL              aiohttp
               22  LOAD_ATTR                ClientSession
               24  LOAD_GLOBAL              aiohttp
               26  LOAD_ATTR                TCPConnector
               28  LOAD_FAST                'verify'
               30  LOAD_CONST               ('verify_ssl',)
               32  CALL_FUNCTION_KW_1     1  '1 total positional and keyword args'
               34  LOAD_CONST               ('connector',)
               36  CALL_FUNCTION_KW_1     1  '1 total positional and keyword args'
               38  BEFORE_ASYNC_WITH
               40  GET_AWAITABLE    
               42  LOAD_CONST               None
               44  YIELD_FROM       
               46  SETUP_ASYNC_WITH    172  'to 172'
               48  STORE_FAST               'session'

 L.  70        50  LOAD_FAST                'json'
               52  LOAD_CONST               None
               54  COMPARE_OP               is-not
               56  POP_JUMP_IF_FALSE   114  'to 114'

 L.  71        58  LOAD_FAST                'session'
               60  LOAD_ATTR                post
               62  LOAD_FAST                'url'
               64  LOAD_FAST                'json'
               66  LOAD_FAST                'headers'
               68  LOAD_CONST               ('json', 'headers')
               70  CALL_FUNCTION_KW_3     3  '3 total positional and keyword args'
               72  BEFORE_ASYNC_WITH
               74  GET_AWAITABLE    
               76  LOAD_CONST               None
               78  YIELD_FROM       
               80  SETUP_ASYNC_WITH    100  'to 100'
               82  STORE_FAST               'resp'

 L.  72        84  LOAD_FAST                'self'
               86  LOAD_ATTR                _proc_resp
               88  LOAD_FAST                'resp'
               90  CALL_FUNCTION_1       1  '1 positional argument'
               92  GET_AWAITABLE    
               94  LOAD_CONST               None
               96  YIELD_FROM       
               98  RETURN_VALUE     
            100_0  COME_FROM_ASYNC_WITH    80  '80'
              100  WITH_CLEANUP_START
              102  GET_AWAITABLE    
              104  LOAD_CONST               None
              106  YIELD_FROM       
              108  WITH_CLEANUP_FINISH
              110  END_FINALLY      
              112  JUMP_FORWARD        168  'to 168'

 L.  74       114  LOAD_FAST                'session'
              116  LOAD_ATTR                post
              118  LOAD_FAST                'url'
              120  LOAD_FAST                'data'
              122  LOAD_FAST                'headers'
              124  LOAD_CONST               ('data', 'headers')
              126  CALL_FUNCTION_KW_3     3  '3 total positional and keyword args'
              128  BEFORE_ASYNC_WITH
              130  GET_AWAITABLE    
              132  LOAD_CONST               None
              134  YIELD_FROM       
              136  SETUP_ASYNC_WITH    156  'to 156'
              138  STORE_FAST               'resp'

 L.  75       140  LOAD_FAST                'self'
              142  LOAD_ATTR                _proc_resp
              144  LOAD_FAST                'resp'
              146  CALL_FUNCTION_1       1  '1 positional argument'
              148  GET_AWAITABLE    
              150  LOAD_CONST               None
              152  YIELD_FROM       
              154  RETURN_VALUE     
            156_0  COME_FROM_ASYNC_WITH   136  '136'
              156  WITH_CLEANUP_START
              158  GET_AWAITABLE    
              160  LOAD_CONST               None
              162  YIELD_FROM       
              164  WITH_CLEANUP_FINISH
              166  END_FINALLY      
            168_0  COME_FROM           112  '112'
              168  POP_BLOCK        
              170  LOAD_CONST               None
            172_0  COME_FROM_ASYNC_WITH    46  '46'
              172  WITH_CLEANUP_START
              174  GET_AWAITABLE    
              176  LOAD_CONST               None
              178  YIELD_FROM       
              180  WITH_CLEANUP_FINISH
              182  END_FINALLY      

Parse error at or near `COME_FROM_ASYNC_WITH' instruction at offset 100_0