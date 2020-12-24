# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\weebapi\request_lib.py
# Compiled at: 2018-05-20 05:45:37
# Size of source mod 2**32: 4963 bytes
import logging, sys, traceback, aiohttp, asyncio
from weebapi import __version__
from .errors import *
logger = logging.getLogger()

class krequest(object):

    def __init__(self, return_json=True, global_headers={}, loop=asyncio.get_event_loop(), **kwargs):
        self.bot = kwargs.get('bot', None)
        self.loop = loop
        self.session = aiohttp.ClientSession(loop=(self.loop))
        self.headers = {'User-Agent':'{}WeebAPI.py/{} (Github: AndyTempel) KRequests/alpha (Custom asynchronous HTTP client)'.format(f"{self.bot.user.username}/{self.bot.user.discriminator} " if self.bot else '', __version__), 
         'X-Powered-By':'{}'.format(sys.version)}
        self.return_json = return_json
        for name, value in global_headers:
            logger.info(f"WEEB.SH Added global header {name}")
            self.headers.update({name: value})

        logger.debug(f"Here are global headers: {str(self.headers)}")

    async def _proc_resp(self, response):
        logger.debug(f"Request {response.method}: {response.url}")
        logger.debug(f"Response headers: {str(response.headers)}")
        if self.return_json:
            try:
                resp = await response.json()
                logger.debug(f"Response content: {str(resp)}")
                return resp
            except Exception:
                print(traceback.format_exc())
                print(response)
                resp = await response.text()
                logger.debug(f"Response content: {str(resp)}")
                return {}

        else:
            resp = await response.text()
            logger.debug(f"Response content: {str(resp)}")
            return resp

    async def get--- This code section failed: ---

 L.  56         0  LOAD_FAST                'headers'
                2  JUMP_IF_TRUE_OR_POP     6  'to 6'
                4  BUILD_MAP_0           0 
              6_0  COME_FROM             2  '2'
                6  STORE_FAST               'headers'

 L.  57         8  LOAD_FAST                'headers'
               10  LOAD_ATTR                update
               12  LOAD_FAST                'self'
               14  LOAD_ATTR                headers
               16  CALL_FUNCTION_1       1  '1 positional argument'
               18  POP_TOP          

 L.  58        20  LOAD_FAST                'self'
               22  LOAD_ATTR                session
               24  LOAD_ATTR                get
               26  LOAD_FAST                'url'
               28  LOAD_FAST                'params'
               30  LOAD_FAST                'headers'
               32  LOAD_CONST               ('params', 'headers')
               34  CALL_FUNCTION_KW_3     3  '3 total positional and keyword args'
               36  BEFORE_ASYNC_WITH
               38  GET_AWAITABLE    
               40  LOAD_CONST               None
               42  YIELD_FROM       
               44  SETUP_ASYNC_WITH     82  'to 82'
               46  STORE_FAST               'resp'

 L.  59        48  LOAD_FAST                'self'
               50  LOAD_ATTR                _proc_resp
               52  LOAD_FAST                'resp'
               54  CALL_FUNCTION_1       1  '1 positional argument'
               56  GET_AWAITABLE    
               58  LOAD_CONST               None
               60  YIELD_FROM       
               62  STORE_FAST               'r'

 L.  60        64  LOAD_FAST                'resp'
               66  LOAD_ATTR                release
               68  CALL_FUNCTION_0       0  '0 positional arguments'
               70  GET_AWAITABLE    
               72  LOAD_CONST               None
               74  YIELD_FROM       
               76  POP_TOP          

 L.  61        78  LOAD_FAST                'r'
               80  RETURN_VALUE     
             82_0  COME_FROM_ASYNC_WITH    44  '44'
               82  WITH_CLEANUP_START
               84  GET_AWAITABLE    
               86  LOAD_CONST               None
               88  YIELD_FROM       
               90  WITH_CLEANUP_FINISH
               92  END_FINALLY      

Parse error at or near `WITH_CLEANUP_FINISH' instruction at offset 90

    async def delete--- This code section failed: ---

 L.  64         0  LOAD_FAST                'headers'
                2  JUMP_IF_TRUE_OR_POP     6  'to 6'
                4  BUILD_MAP_0           0 
              6_0  COME_FROM             2  '2'
                6  STORE_FAST               'headers'

 L.  65         8  LOAD_FAST                'headers'
               10  LOAD_ATTR                update
               12  LOAD_FAST                'self'
               14  LOAD_ATTR                headers
               16  CALL_FUNCTION_1       1  '1 positional argument'
               18  POP_TOP          

 L.  66        20  LOAD_FAST                'self'
               22  LOAD_ATTR                session
               24  LOAD_ATTR                delete
               26  LOAD_FAST                'url'
               28  LOAD_FAST                'params'
               30  LOAD_FAST                'headers'
               32  LOAD_CONST               ('params', 'headers')
               34  CALL_FUNCTION_KW_3     3  '3 total positional and keyword args'
               36  BEFORE_ASYNC_WITH
               38  GET_AWAITABLE    
               40  LOAD_CONST               None
               42  YIELD_FROM       
               44  SETUP_ASYNC_WITH     82  'to 82'
               46  STORE_FAST               'resp'

 L.  67        48  LOAD_FAST                'self'
               50  LOAD_ATTR                _proc_resp
               52  LOAD_FAST                'resp'
               54  CALL_FUNCTION_1       1  '1 positional argument'
               56  GET_AWAITABLE    
               58  LOAD_CONST               None
               60  YIELD_FROM       
               62  STORE_FAST               'r'

 L.  68        64  LOAD_FAST                'resp'
               66  LOAD_ATTR                release
               68  CALL_FUNCTION_0       0  '0 positional arguments'
               70  GET_AWAITABLE    
               72  LOAD_CONST               None
               74  YIELD_FROM       
               76  POP_TOP          

 L.  69        78  LOAD_FAST                'r'
               80  RETURN_VALUE     
             82_0  COME_FROM_ASYNC_WITH    44  '44'
               82  WITH_CLEANUP_START
               84  GET_AWAITABLE    
               86  LOAD_CONST               None
               88  YIELD_FROM       
               90  WITH_CLEANUP_FINISH
               92  END_FINALLY      

Parse error at or near `WITH_CLEANUP_FINISH' instruction at offset 90

    async def post--- This code section failed: ---

 L.  72         0  LOAD_FAST                'headers'
                2  JUMP_IF_TRUE_OR_POP     6  'to 6'
                4  BUILD_MAP_0           0 
              6_0  COME_FROM             2  '2'
                6  STORE_FAST               'headers'

 L.  73         8  LOAD_FAST                'headers'
               10  LOAD_ATTR                update
               12  LOAD_FAST                'self'
               14  LOAD_ATTR                headers
               16  CALL_FUNCTION_1       1  '1 positional argument'
               18  POP_TOP          

 L.  74        20  LOAD_FAST                'json'
               22  LOAD_CONST               None
               24  COMPARE_OP               is-not
               26  POP_JUMP_IF_FALSE   104  'to 104'

 L.  75        28  LOAD_FAST                'self'
               30  LOAD_ATTR                session
               32  LOAD_ATTR                post
               34  LOAD_FAST                'url'
               36  LOAD_FAST                'json'
               38  LOAD_FAST                'headers'
               40  LOAD_CONST               ('json', 'headers')
               42  CALL_FUNCTION_KW_3     3  '3 total positional and keyword args'
               44  BEFORE_ASYNC_WITH
               46  GET_AWAITABLE    
               48  LOAD_CONST               None
               50  YIELD_FROM       
               52  SETUP_ASYNC_WITH     90  'to 90'
               54  STORE_FAST               'resp'

 L.  76        56  LOAD_FAST                'self'
               58  LOAD_ATTR                _proc_resp
               60  LOAD_FAST                'resp'
               62  CALL_FUNCTION_1       1  '1 positional argument'
               64  GET_AWAITABLE    
               66  LOAD_CONST               None
               68  YIELD_FROM       
               70  STORE_FAST               'r'

 L.  77        72  LOAD_FAST                'resp'
               74  LOAD_ATTR                release
               76  CALL_FUNCTION_0       0  '0 positional arguments'
               78  GET_AWAITABLE    
               80  LOAD_CONST               None
               82  YIELD_FROM       
               84  POP_TOP          

 L.  78        86  LOAD_FAST                'r'
               88  RETURN_VALUE     
             90_0  COME_FROM_ASYNC_WITH    52  '52'
               90  WITH_CLEANUP_START
               92  GET_AWAITABLE    
               94  LOAD_CONST               None
               96  YIELD_FROM       
               98  WITH_CLEANUP_FINISH
              100  END_FINALLY      
              102  JUMP_FORWARD        178  'to 178'

 L.  80       104  LOAD_FAST                'self'
              106  LOAD_ATTR                session
              108  LOAD_ATTR                post
              110  LOAD_FAST                'url'
              112  LOAD_FAST                'data'
              114  LOAD_FAST                'headers'
              116  LOAD_CONST               ('data', 'headers')
              118  CALL_FUNCTION_KW_3     3  '3 total positional and keyword args'
              120  BEFORE_ASYNC_WITH
              122  GET_AWAITABLE    
              124  LOAD_CONST               None
              126  YIELD_FROM       
              128  SETUP_ASYNC_WITH    166  'to 166'
              130  STORE_FAST               'resp'

 L.  81       132  LOAD_FAST                'self'
              134  LOAD_ATTR                _proc_resp
              136  LOAD_FAST                'resp'
              138  CALL_FUNCTION_1       1  '1 positional argument'
              140  GET_AWAITABLE    
              142  LOAD_CONST               None
              144  YIELD_FROM       
              146  STORE_FAST               'r'

 L.  82       148  LOAD_FAST                'resp'
              150  LOAD_ATTR                release
              152  CALL_FUNCTION_0       0  '0 positional arguments'
              154  GET_AWAITABLE    
              156  LOAD_CONST               None
              158  YIELD_FROM       
              160  POP_TOP          

 L.  83       162  LOAD_FAST                'r'
              164  RETURN_VALUE     
            166_0  COME_FROM_ASYNC_WITH   128  '128'
              166  WITH_CLEANUP_START
              168  GET_AWAITABLE    
              170  LOAD_CONST               None
              172  YIELD_FROM       
              174  WITH_CLEANUP_FINISH
              176  END_FINALLY      
            178_0  COME_FROM           102  '102'

Parse error at or near `JUMP_FORWARD' instruction at offset 102

    async def download_get(self, url, filename, params=None, headers=None, verify=True):
        headers = headers or {}
        headers.update(self.headers)
        async with self.session.get(url, params=params, headers=headers) as response:
            if response.status != 200:
                raise Forbidden
            with open(filename, 'wb') as (f_handle):
                while True:
                    chunk = await response.content.read(1024)
                    if not chunk:
                        break
                    f_handle.write(chunk)

            await response.release()

    async def download_post(self, url, filename, data=None, json=None, headers=None, verify=True):
        headers = headers or {}
        headers.update(self.headers)
        if json is not None:
            async with self.session.post(url, json=json, headers=headers) as response:
                if response.status != 200:
                    raise Forbidden
                with open(filename, 'wb') as (f_handle):
                    while True:
                        chunk = await response.content.read(1024)
                        if not chunk:
                            break
                        f_handle.write(chunk)

                await response.release()
        else:
            async with self.session.post(url, data=data, headers=headers) as response:
                if response.status != 200:
                    raise Forbidden
                with open(filename, 'wb') as (f_handle):
                    while True:
                        chunk = await response.content.read(1024)
                        if not chunk:
                            break
                        f_handle.write(chunk)

                await response.release()