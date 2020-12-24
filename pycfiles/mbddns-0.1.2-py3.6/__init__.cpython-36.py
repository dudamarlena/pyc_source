# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/mbddns/__init__.py
# Compiled at: 2018-11-29 11:03:42
# Size of source mod 2**32: 1108 bytes
import asyncio, aiohttp, logging
_LOGGER = logging.getLogger(__name__)

async def update--- This code section failed: ---

 L.   9         0  LOAD_FAST                'domain'

 L.  10         2  LOAD_FAST                'password'

 L.  11         4  LOAD_STR                 'REPLACE {} {} A DYNAMIC_IP'
                6  LOAD_ATTR                format
                8  LOAD_FAST                'host'
               10  LOAD_FAST                'ttl'
               12  CALL_FUNCTION_2       2  '2 positional arguments'
               14  LOAD_CONST               ('domain', 'password', 'command')
               16  BUILD_CONST_KEY_MAP_3     3 
               18  STORE_FAST               'data'

 L.  14        20  LOAD_FAST                'session'
               22  JUMP_IF_TRUE_OR_POP    30  'to 30'
               24  LOAD_GLOBAL              aiohttp
               26  LOAD_ATTR                ClientSession
               28  CALL_FUNCTION_0       0  '0 positional arguments'
             30_0  COME_FROM            22  '22'
               30  BEFORE_ASYNC_WITH
               32  GET_AWAITABLE    
               34  LOAD_CONST               None
               36  YIELD_FROM       
               38  SETUP_ASYNC_WITH    232  'to 232'
               40  STORE_FAST               'session'

 L.  15        42  SETUP_EXCEPT        182  'to 182'

 L.  16        44  LOAD_GLOBAL              asyncio
               46  LOAD_ATTR                gather
               48  LOAD_FAST                'session'
               50  LOAD_ATTR                post
               52  LOAD_STR                 'https://dnsapi4.mythic-beasts.com/'
               54  LOAD_FAST                'data'
               56  LOAD_CONST               ('data',)
               58  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
               60  CALL_FUNCTION_1       1  '1 positional argument'
               62  GET_AWAITABLE    
               64  LOAD_CONST               None
               66  YIELD_FROM       
               68  STORE_FAST               'resp'

 L.  17        70  LOAD_FAST                'resp'
               72  LOAD_CONST               0
               74  BINARY_SUBSCR    
               76  LOAD_ATTR                text
               78  CALL_FUNCTION_0       0  '0 positional arguments'
               80  GET_AWAITABLE    
               82  LOAD_CONST               None
               84  YIELD_FROM       
               86  STORE_FAST               'body'

 L.  19        88  LOAD_FAST                'body'
               90  LOAD_ATTR                startswith
               92  LOAD_STR                 'REPLACE'
               94  CALL_FUNCTION_1       1  '1 positional argument'
               96  POP_JUMP_IF_FALSE   114  'to 114'

 L.  20        98  LOAD_GLOBAL              _LOGGER
              100  LOAD_ATTR                debug
              102  LOAD_STR                 'Updating Mythic Beasts successful: %s'
              104  LOAD_FAST                'body'
              106  CALL_FUNCTION_2       2  '2 positional arguments'
              108  POP_TOP          

 L.  21       110  LOAD_CONST               True
              112  RETURN_END_IF    
            114_0  COME_FROM            96  '96'

 L.  23       114  LOAD_FAST                'body'
              116  LOAD_ATTR                startswith
              118  LOAD_STR                 'ERR'
              120  CALL_FUNCTION_1       1  '1 positional argument'
              122  POP_JUMP_IF_FALSE   146  'to 146'

 L.  24       124  LOAD_GLOBAL              _LOGGER
              126  LOAD_ATTR                error
              128  LOAD_STR                 'Updating Mythic Beasts failed: %s'

 L.  25       130  LOAD_FAST                'body'
              132  LOAD_ATTR                partition
              134  LOAD_STR                 ' '
              136  CALL_FUNCTION_1       1  '1 positional argument'
              138  LOAD_CONST               2
              140  BINARY_SUBSCR    
              142  CALL_FUNCTION_2       2  '2 positional arguments'
              144  POP_TOP          
            146_0  COME_FROM           122  '122'

 L.  27       146  LOAD_FAST                'body'
              148  LOAD_ATTR                startswith
              150  LOAD_STR                 'NREPLACE'
              152  CALL_FUNCTION_1       1  '1 positional argument'
              154  POP_JUMP_IF_FALSE   178  'to 178'

 L.  28       156  LOAD_GLOBAL              _LOGGER
              158  LOAD_ATTR                warning
              160  LOAD_STR                 'Updating Mythic Beasts failed: %s'

 L.  29       162  LOAD_FAST                'body'
              164  LOAD_ATTR                partition
              166  LOAD_STR                 ';'
              168  CALL_FUNCTION_1       1  '1 positional argument'
              170  LOAD_CONST               2
              172  BINARY_SUBSCR    
              174  CALL_FUNCTION_2       2  '2 positional arguments'
              176  POP_TOP          
            178_0  COME_FROM           154  '154'
              178  POP_BLOCK        
              180  JUMP_FORWARD        228  'to 228'
            182_0  COME_FROM_EXCEPT     42  '42'

 L.  31       182  DUP_TOP          
              184  LOAD_GLOBAL              Exception
              186  COMPARE_OP               exception-match
              188  POP_JUMP_IF_FALSE   226  'to 226'
              190  POP_TOP          
              192  STORE_FAST               'e'
              194  POP_TOP          
              196  SETUP_FINALLY       216  'to 216'

 L.  32       198  LOAD_GLOBAL              _LOGGER
              200  LOAD_ATTR                error
              202  LOAD_STR                 'Updating Mythic Beasts failed: %s'
              204  LOAD_FAST                'e'
              206  CALL_FUNCTION_2       2  '2 positional arguments'
              208  POP_TOP          
              210  POP_BLOCK        
              212  POP_EXCEPT       
              214  LOAD_CONST               None
            216_0  COME_FROM_FINALLY   196  '196'
              216  LOAD_CONST               None
              218  STORE_FAST               'e'
              220  DELETE_FAST              'e'
              222  END_FINALLY      
              224  JUMP_FORWARD        228  'to 228'
              226  END_FINALLY      
            228_0  COME_FROM           224  '224'
            228_1  COME_FROM           180  '180'

 L.  34       228  LOAD_CONST               False
              230  RETURN_VALUE     
            232_0  COME_FROM_ASYNC_WITH    38  '38'
              232  WITH_CLEANUP_START
              234  GET_AWAITABLE    
              236  LOAD_CONST               None
              238  YIELD_FROM       
              240  WITH_CLEANUP_FINISH
              242  END_FINALLY      

Parse error at or near `COME_FROM_ASYNC_WITH' instruction at offset 232_0