# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/fw/development/AutoBuddy/aioouimeaux/aioouimeaux/utils.py
# Compiled at: 2018-11-09 09:49:21
# Size of source mod 2**32: 3788 bytes
from functools import wraps
import re, struct, time, asyncio as aio, aiohttp as aioh, async_timeout as aioto, netifaces

def tz_hours():
    delta = time.localtime().tm_hour - time.gmtime().tm_hour
    sign = '-' if delta < 0 else ''
    return '%s%02d.00' % (sign, abs(delta))


def is_dst():
    if time.localtime().tm_isdst:
        return 1
    else:
        return 0


def get_timesync():
    timesync = '\n<?xml version="1.0" encoding="utf-8"?>\n<s:Envelope xmlns:s="http://schemas.xmlsoap.org/soap/envelope/" s:encodingStyle="http://schemas.xmlsoap.org/soap/encoding/">\n <s:Body>\n  <u:TimeSync xmlns:u="urn:Belkin:service:timesync:1">\n   <UTC>{utc}</UTC>\n   <TimeZone>{tz}</TimeZone>\n   <dst>{dst}</dst>\n   <DstSupported>{dstsupported}</DstSupported>\n  </u:TimeSync>\n </s:Body>\n</s:Envelope>'.format(utc=(int(time.time())),
      tz=(tz_hours()),
      dst=(is_dst()),
      dstsupported=(is_dst())).strip()
    return timesync


def get_ip_address():
    return netifaces.ifaddresses(netifaces.gateways()['default'][netifaces.AF_INET][1])[netifaces.AF_INET][0]['addr']


def matcher(match_string):
    pattern = re.compile('.*?'.join(re.escape(c) for c in match_string.lower()))

    def matches(s):
        return pattern.search(s.lower()) is not None

    return matches


_RETRIES = 3
_DELAY = 3
_TIMEOUT = 13

def get_retries():
    return _RETRIES


async def requests_get--- This code section failed: ---

 L.  62         0  LOAD_GLOBAL              _RETRIES
                2  STORE_FAST               'remaining'

 L.  63         4  SETUP_LOOP          242  'to 242'
                6  LOAD_FAST                'remaining'
                8  POP_JUMP_IF_FALSE   240  'to 240'

 L.  64        10  LOAD_FAST                'remaining'
               12  LOAD_CONST               1
               14  INPLACE_SUBTRACT 
               16  STORE_FAST               'remaining'

 L.  65        18  SETUP_EXCEPT        160  'to 160'

 L.  66        20  LOAD_GLOBAL              aioto
               22  LOAD_ATTR                timeout
               24  LOAD_GLOBAL              _TIMEOUT
               26  CALL_FUNCTION_1       1  '1 positional argument'
               28  SETUP_WITH          150  'to 150'
               30  POP_TOP          

 L.  67        32  LOAD_GLOBAL              aioh
               34  LOAD_ATTR                ClientSession
               36  CALL_FUNCTION_0       0  '0 positional arguments'
               38  BEFORE_ASYNC_WITH
               40  GET_AWAITABLE    
               42  LOAD_CONST               None
               44  YIELD_FROM       
               46  SETUP_ASYNC_WITH    134  'to 134'
               48  STORE_FAST               'session'

 L.  68        50  LOAD_FAST                'session'
               52  LOAD_ATTR                get
               54  LOAD_FAST                'url'
               56  BUILD_TUPLE_1         1 
               58  LOAD_STR                 'allow_redirects'
               60  LOAD_FAST                'allow_redirects'
               62  BUILD_MAP_1           1 
               64  LOAD_FAST                'kwargs'
               66  BUILD_MAP_UNPACK_WITH_CALL_2     2 
               68  CALL_FUNCTION_EX_KW     1  'keyword and positional arguments'
               70  BEFORE_ASYNC_WITH
               72  GET_AWAITABLE    
               74  LOAD_CONST               None
               76  YIELD_FROM       
               78  SETUP_ASYNC_WITH    118  'to 118'
               80  STORE_FAST               'response'

 L.  69        82  LOAD_FAST                'response'
               84  LOAD_ATTR                status
               86  LOAD_CONST               200
               88  COMPARE_OP               !=
               90  POP_JUMP_IF_FALSE    98  'to 98'

 L.  71        92  LOAD_GLOBAL              aioh
               94  LOAD_ATTR                ClientConnectionError
               96  RAISE_VARARGS_1       1  'exception'
             98_0  COME_FROM            90  '90'

 L.  72        98  LOAD_FAST                'response'
              100  LOAD_ATTR                read
              102  CALL_FUNCTION_0       0  '0 positional arguments'
              104  GET_AWAITABLE    
              106  LOAD_CONST               None
              108  YIELD_FROM       
              110  LOAD_FAST                'response'
              112  STORE_ATTR               raw_body

 L.  73       114  LOAD_FAST                'response'
              116  RETURN_VALUE     
            118_0  COME_FROM_ASYNC_WITH    78  '78'
              118  WITH_CLEANUP_START
              120  GET_AWAITABLE    
              122  LOAD_CONST               None
              124  YIELD_FROM       
              126  WITH_CLEANUP_FINISH
              128  END_FINALLY      
              130  POP_BLOCK        
              132  LOAD_CONST               None
            134_0  COME_FROM_ASYNC_WITH    46  '46'
              134  WITH_CLEANUP_START
              136  GET_AWAITABLE    
              138  LOAD_CONST               None
              140  YIELD_FROM       
              142  WITH_CLEANUP_FINISH
              144  END_FINALLY      
              146  POP_BLOCK        
              148  LOAD_CONST               None
            150_0  COME_FROM_WITH       28  '28'
              150  WITH_CLEANUP_START
              152  WITH_CLEANUP_FINISH
              154  END_FINALLY      
              156  POP_BLOCK        
              158  JUMP_BACK             6  'to 6'
            160_0  COME_FROM_EXCEPT     18  '18'

 L.  74       160  DUP_TOP          
              162  LOAD_GLOBAL              aio
              164  LOAD_ATTR                TimeoutError
              166  COMPARE_OP               exception-match
              168  POP_JUMP_IF_FALSE   200  'to 200'
              170  POP_TOP          
              172  POP_TOP          
              174  POP_TOP          

 L.  75       176  LOAD_FAST                'remaining'
              178  POP_JUMP_IF_TRUE    186  'to 186'

 L.  76       180  LOAD_GLOBAL              aioh
              182  LOAD_ATTR                ClientConnectionError
              184  RAISE_VARARGS_1       1  'exception'
            186_0  COME_FROM           178  '178'

 L.  77       186  LOAD_GLOBAL              aio
              188  LOAD_ATTR                sleep
              190  LOAD_GLOBAL              _DELAY
              192  CALL_FUNCTION_1       1  '1 positional argument'
              194  POP_TOP          
              196  POP_EXCEPT       
              198  JUMP_BACK             6  'to 6'

 L.  78       200  DUP_TOP          
              202  LOAD_GLOBAL              aioh
              204  LOAD_ATTR                ClientConnectionError
              206  COMPARE_OP               exception-match
              208  POP_JUMP_IF_FALSE   236  'to 236'
              210  POP_TOP          
              212  POP_TOP          
              214  POP_TOP          

 L.  79       216  LOAD_FAST                'remaining'
              218  POP_JUMP_IF_TRUE    222  'to 222'

 L.  80       220  RAISE_VARARGS_0       0  'reraise'
            222_0  COME_FROM           218  '218'

 L.  81       222  LOAD_GLOBAL              aio
              224  LOAD_ATTR                sleep
              226  LOAD_GLOBAL              _DELAY
              228  CALL_FUNCTION_1       1  '1 positional argument'
              230  POP_TOP          
              232  POP_EXCEPT       
              234  JUMP_BACK             6  'to 6'
              236  END_FINALLY      
              238  JUMP_BACK             6  'to 6'
              240  POP_BLOCK        
            242_0  COME_FROM_LOOP        4  '4'

Parse error at or near `COME_FROM_ASYNC_WITH' instruction at offset 118_0


async def requests_post--- This code section failed: ---

 L.  84         0  LOAD_GLOBAL              _RETRIES
                2  STORE_FAST               'remaining'

 L.  85         4  SETUP_LOOP          226  'to 226'
                6  LOAD_FAST                'remaining'
                8  POP_JUMP_IF_FALSE   224  'to 224'

 L.  86        10  LOAD_FAST                'remaining'
               12  LOAD_CONST               1
               14  INPLACE_SUBTRACT 
               16  STORE_FAST               'remaining'

 L.  87        18  SETUP_EXCEPT        144  'to 144'

 L.  88        20  LOAD_GLOBAL              aioto
               22  LOAD_ATTR                timeout
               24  LOAD_GLOBAL              _TIMEOUT
               26  CALL_FUNCTION_1       1  '1 positional argument'
               28  SETUP_WITH          134  'to 134'
               30  POP_TOP          

 L.  89        32  LOAD_GLOBAL              aioh
               34  LOAD_ATTR                ClientSession
               36  CALL_FUNCTION_0       0  '0 positional arguments'
               38  BEFORE_ASYNC_WITH
               40  GET_AWAITABLE    
               42  LOAD_CONST               None
               44  YIELD_FROM       
               46  SETUP_ASYNC_WITH    118  'to 118'
               48  STORE_FAST               'session'

 L.  90        50  LOAD_FAST                'session'
               52  LOAD_ATTR                post
               54  LOAD_FAST                'url'
               56  BUILD_TUPLE_1         1 
               58  LOAD_STR                 'data'
               60  LOAD_FAST                'data'
               62  BUILD_MAP_1           1 
               64  LOAD_FAST                'kwargs'
               66  BUILD_MAP_UNPACK_WITH_CALL_2     2 
               68  CALL_FUNCTION_EX_KW     1  'keyword and positional arguments'
               70  BEFORE_ASYNC_WITH
               72  GET_AWAITABLE    
               74  LOAD_CONST               None
               76  YIELD_FROM       
               78  SETUP_ASYNC_WITH    102  'to 102'
               80  STORE_FAST               'response'

 L.  91        82  LOAD_FAST                'response'
               84  LOAD_ATTR                read
               86  CALL_FUNCTION_0       0  '0 positional arguments'
               88  GET_AWAITABLE    
               90  LOAD_CONST               None
               92  YIELD_FROM       
               94  LOAD_FAST                'response'
               96  STORE_ATTR               raw_body

 L.  92        98  LOAD_FAST                'response'
              100  RETURN_VALUE     
            102_0  COME_FROM_ASYNC_WITH    78  '78'
              102  WITH_CLEANUP_START
              104  GET_AWAITABLE    
              106  LOAD_CONST               None
              108  YIELD_FROM       
              110  WITH_CLEANUP_FINISH
              112  END_FINALLY      
              114  POP_BLOCK        
              116  LOAD_CONST               None
            118_0  COME_FROM_ASYNC_WITH    46  '46'
              118  WITH_CLEANUP_START
              120  GET_AWAITABLE    
              122  LOAD_CONST               None
              124  YIELD_FROM       
              126  WITH_CLEANUP_FINISH
              128  END_FINALLY      
              130  POP_BLOCK        
              132  LOAD_CONST               None
            134_0  COME_FROM_WITH       28  '28'
              134  WITH_CLEANUP_START
              136  WITH_CLEANUP_FINISH
              138  END_FINALLY      
              140  POP_BLOCK        
              142  JUMP_BACK             6  'to 6'
            144_0  COME_FROM_EXCEPT     18  '18'

 L.  93       144  DUP_TOP          
              146  LOAD_GLOBAL              aio
              148  LOAD_ATTR                TimeoutError
              150  COMPARE_OP               exception-match
              152  POP_JUMP_IF_FALSE   184  'to 184'
              154  POP_TOP          
              156  POP_TOP          
              158  POP_TOP          

 L.  94       160  LOAD_FAST                'remaining'
              162  POP_JUMP_IF_TRUE    170  'to 170'

 L.  95       164  LOAD_GLOBAL              aioh
              166  LOAD_ATTR                ClientConnectionError
              168  RAISE_VARARGS_1       1  'exception'
            170_0  COME_FROM           162  '162'

 L.  96       170  LOAD_GLOBAL              aio
              172  LOAD_ATTR                sleep
              174  LOAD_GLOBAL              _DELAY
              176  CALL_FUNCTION_1       1  '1 positional argument'
              178  POP_TOP          
              180  POP_EXCEPT       
              182  JUMP_BACK             6  'to 6'

 L.  97       184  DUP_TOP          
              186  LOAD_GLOBAL              aioh
              188  LOAD_ATTR                ClientConnectionError
              190  COMPARE_OP               exception-match
              192  POP_JUMP_IF_FALSE   220  'to 220'
              194  POP_TOP          
              196  POP_TOP          
              198  POP_TOP          

 L.  98       200  LOAD_FAST                'remaining'
              202  POP_JUMP_IF_TRUE    206  'to 206'

 L.  99       204  RAISE_VARARGS_0       0  'reraise'
            206_0  COME_FROM           202  '202'

 L. 100       206  LOAD_GLOBAL              aio
              208  LOAD_ATTR                sleep
              210  LOAD_GLOBAL              _DELAY
              212  CALL_FUNCTION_1       1  '1 positional argument'
              214  POP_TOP          
              216  POP_EXCEPT       
              218  JUMP_BACK             6  'to 6'
              220  END_FINALLY      
              222  JUMP_BACK             6  'to 6'
              224  POP_BLOCK        
            226_0  COME_FROM_LOOP        4  '4'

Parse error at or near `COME_FROM_ASYNC_WITH' instruction at offset 102_0


async def requests_request--- This code section failed: ---

 L. 103         0  LOAD_GLOBAL              _RETRIES
                2  STORE_FAST               'remaining'

 L. 104         4  SETUP_LOOP          220  'to 220'
                6  LOAD_FAST                'remaining'
                8  POP_JUMP_IF_FALSE   218  'to 218'

 L. 105        10  LOAD_FAST                'remaining'
               12  LOAD_CONST               1
               14  INPLACE_SUBTRACT 
               16  STORE_FAST               'remaining'

 L. 106        18  SETUP_EXCEPT        138  'to 138'

 L. 107        20  LOAD_GLOBAL              aioto
               22  LOAD_ATTR                timeout
               24  LOAD_GLOBAL              _TIMEOUT
               26  CALL_FUNCTION_1       1  '1 positional argument'
               28  SETUP_WITH          128  'to 128'
               30  POP_TOP          

 L. 108        32  LOAD_GLOBAL              aioh
               34  LOAD_ATTR                ClientSession
               36  CALL_FUNCTION_0       0  '0 positional arguments'
               38  BEFORE_ASYNC_WITH
               40  GET_AWAITABLE    
               42  LOAD_CONST               None
               44  YIELD_FROM       
               46  SETUP_ASYNC_WITH    112  'to 112'
               48  STORE_FAST               'session'

 L. 109        50  LOAD_FAST                'session'
               52  LOAD_ATTR                request
               54  LOAD_FAST                'method'
               56  LOAD_FAST                'url'
               58  BUILD_TUPLE_2         2 
               60  LOAD_FAST                'kwargs'
               62  CALL_FUNCTION_EX_KW     1  'keyword and positional arguments'
               64  BEFORE_ASYNC_WITH
               66  GET_AWAITABLE    
               68  LOAD_CONST               None
               70  YIELD_FROM       
               72  SETUP_ASYNC_WITH     96  'to 96'
               74  STORE_FAST               'response'

 L. 110        76  LOAD_FAST                'response'
               78  LOAD_ATTR                read
               80  CALL_FUNCTION_0       0  '0 positional arguments'
               82  GET_AWAITABLE    
               84  LOAD_CONST               None
               86  YIELD_FROM       
               88  LOAD_FAST                'response'
               90  STORE_ATTR               raw_body

 L. 111        92  LOAD_FAST                'response'
               94  RETURN_VALUE     
             96_0  COME_FROM_ASYNC_WITH    72  '72'
               96  WITH_CLEANUP_START
               98  GET_AWAITABLE    
              100  LOAD_CONST               None
              102  YIELD_FROM       
              104  WITH_CLEANUP_FINISH
              106  END_FINALLY      
              108  POP_BLOCK        
              110  LOAD_CONST               None
            112_0  COME_FROM_ASYNC_WITH    46  '46'
              112  WITH_CLEANUP_START
              114  GET_AWAITABLE    
              116  LOAD_CONST               None
              118  YIELD_FROM       
              120  WITH_CLEANUP_FINISH
              122  END_FINALLY      
              124  POP_BLOCK        
              126  LOAD_CONST               None
            128_0  COME_FROM_WITH       28  '28'
              128  WITH_CLEANUP_START
              130  WITH_CLEANUP_FINISH
              132  END_FINALLY      
              134  POP_BLOCK        
              136  JUMP_BACK             6  'to 6'
            138_0  COME_FROM_EXCEPT     18  '18'

 L. 112       138  DUP_TOP          
              140  LOAD_GLOBAL              aio
              142  LOAD_ATTR                TimeoutError
              144  COMPARE_OP               exception-match
              146  POP_JUMP_IF_FALSE   178  'to 178'
              148  POP_TOP          
              150  POP_TOP          
              152  POP_TOP          

 L. 113       154  LOAD_FAST                'remaining'
              156  POP_JUMP_IF_TRUE    164  'to 164'

 L. 114       158  LOAD_GLOBAL              aioh
              160  LOAD_ATTR                ClientConnectionError
              162  RAISE_VARARGS_1       1  'exception'
            164_0  COME_FROM           156  '156'

 L. 115       164  LOAD_GLOBAL              aio
              166  LOAD_ATTR                sleep
              168  LOAD_GLOBAL              _DELAY
              170  CALL_FUNCTION_1       1  '1 positional argument'
              172  POP_TOP          
              174  POP_EXCEPT       
              176  JUMP_BACK             6  'to 6'

 L. 116       178  DUP_TOP          
              180  LOAD_GLOBAL              aioh
              182  LOAD_ATTR                ClientConnectionError
              184  COMPARE_OP               exception-match
              186  POP_JUMP_IF_FALSE   214  'to 214'
              188  POP_TOP          
              190  POP_TOP          
              192  POP_TOP          

 L. 117       194  LOAD_FAST                'remaining'
              196  POP_JUMP_IF_TRUE    200  'to 200'

 L. 118       198  RAISE_VARARGS_0       0  'reraise'
            200_0  COME_FROM           196  '196'

 L. 119       200  LOAD_GLOBAL              aio
              202  LOAD_ATTR                sleep
              204  LOAD_GLOBAL              _DELAY
              206  CALL_FUNCTION_1       1  '1 positional argument'
              208  POP_TOP          
              210  POP_EXCEPT       
              212  JUMP_BACK             6  'to 6'
              214  END_FINALLY      
              216  JUMP_BACK             6  'to 6'
              218  POP_BLOCK        
            220_0  COME_FROM_LOOP        4  '4'

Parse error at or near `COME_FROM_ASYNC_WITH' instruction at offset 96_0