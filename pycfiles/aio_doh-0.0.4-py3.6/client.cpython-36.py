# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/doh/client.py
# Compiled at: 2017-12-16 15:37:57
# Size of source mod 2**32: 1950 bytes
from enum import Enum
import string, random, aiohttp
from .exceptions import DNSException, DOHException
from .utils import random_padding
__all__ = [
 'RecordType', 'DOHClient']

class RecordType(Enum):
    A = 1
    AAAA = 28
    CNAME = 5
    MX = 15
    SOA = 6
    SRV = 33
    TXT = 16
    PTR = 12


NOERROR = 0

class DOHClient:

    def __init__(self, loop, *, url: str='https://dns.google.com/resolve', cd: bool=False, edns_client_subnet: str='0.0.0.0/0', random_padding: str=True):
        self.loop = loop
        self.url = url
        self.random_padding = random_padding
        self.edns_client_subnet = edns_client_subnet

    async def query--- This code section failed: ---

 L.  43         0  LOAD_GLOBAL              aiohttp
                2  LOAD_ATTR                ClientSession
                4  LOAD_FAST                'self'
                6  LOAD_ATTR                loop
                8  LOAD_CONST               ('loop',)
               10  CALL_FUNCTION_KW_1     1  '1 total positional and keyword args'
               12  BEFORE_ASYNC_WITH
               14  GET_AWAITABLE    
               16  LOAD_CONST               None
               18  YIELD_FROM       
               20  SETUP_ASYNC_WITH    154  'to 154'
               22  STORE_FAST               'session'

 L.  45        24  LOAD_GLOBAL              dict
               26  LOAD_FAST                'hosthame'

 L.  46        28  LOAD_FAST                'type'

 L.  47        30  LOAD_GLOBAL              int
               32  LOAD_FAST                'dnssec'
               34  UNARY_NOT        
               36  CALL_FUNCTION_1       1  '1 positional argument'

 L.  48        38  LOAD_FAST                'self'
               40  LOAD_ATTR                edns_client_subnet
               42  LOAD_CONST               ('name', 'type', 'cd', 'edns_client_subnet')
               44  CALL_FUNCTION_KW_4     4  '4 total positional and keyword args'
               46  STORE_FAST               'params'

 L.  50        48  LOAD_FAST                'self'
               50  LOAD_ATTR                random_padding
               52  POP_JUMP_IF_FALSE    68  'to 68'

 L.  51        54  LOAD_FAST                'params'
               56  LOAD_ATTR                update
               58  LOAD_GLOBAL              random_padding
               60  CALL_FUNCTION_0       0  '0 positional arguments'
               62  LOAD_CONST               ('random_padding',)
               64  CALL_FUNCTION_KW_1     1  '1 total positional and keyword args'
               66  POP_TOP          
             68_0  COME_FROM            52  '52'

 L.  53        68  LOAD_FAST                'session'
               70  LOAD_ATTR                get
               72  LOAD_FAST                'self'
               74  LOAD_ATTR                url
               76  LOAD_FAST                'params'
               78  LOAD_CONST               ('params',)
               80  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
               82  BEFORE_ASYNC_WITH
               84  GET_AWAITABLE    
               86  LOAD_CONST               None
               88  YIELD_FROM       
               90  SETUP_ASYNC_WITH    138  'to 138'
               92  STORE_FAST               'response'

 L.  54        94  LOAD_FAST                'response'
               96  LOAD_ATTR                status
               98  LOAD_CONST               200
              100  COMPARE_OP               !=
              102  POP_JUMP_IF_FALSE   120  'to 120'

 L.  55       104  LOAD_GLOBAL              DOHException
              106  LOAD_STR                 'Bad response status: '
              108  LOAD_FAST                'response'
              110  LOAD_ATTR                status
              112  FORMAT_VALUE          0  ''
              114  BUILD_STRING_2        2 
              116  CALL_FUNCTION_1       1  '1 positional argument'
              118  RAISE_VARARGS_1       1  'exception'
            120_0  COME_FROM           102  '102'

 L.  57       120  LOAD_FAST                'response'
              122  LOAD_ATTR                json
              124  LOAD_STR                 'application/x-javascript'
              126  LOAD_CONST               ('content_type',)
              128  CALL_FUNCTION_KW_1     1  '1 total positional and keyword args'
              130  GET_AWAITABLE    
              132  LOAD_CONST               None
              134  YIELD_FROM       
              136  RETURN_VALUE     
            138_0  COME_FROM_ASYNC_WITH    90  '90'
              138  WITH_CLEANUP_START
              140  GET_AWAITABLE    
              142  LOAD_CONST               None
              144  YIELD_FROM       
              146  WITH_CLEANUP_FINISH
              148  END_FINALLY      
              150  POP_BLOCK        
              152  LOAD_CONST               None
            154_0  COME_FROM_ASYNC_WITH    20  '20'
              154  WITH_CLEANUP_START
              156  GET_AWAITABLE    
              158  LOAD_CONST               None
              160  YIELD_FROM       
              162  WITH_CLEANUP_FINISH
              164  END_FINALLY      

Parse error at or near `COME_FROM_ASYNC_WITH' instruction at offset 138_0

    async def resolve(self, hostname: str, type=RecordType.A.name):
        response = await self.query(hostname, type=type)
        if response['Status'] != NOERROR:
            raise DNSException.from_responseresponse
        return [r['data'] for r in response['Answer'] if r['type'] in (type, RecordType[type].value) if r['data']]

    async def gethostbyname(self, hostname: str):
        return await self.resolvehostname[0]