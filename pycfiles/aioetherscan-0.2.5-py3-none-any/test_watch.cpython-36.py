# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/test/test_watch.py
# Compiled at: 2018-05-26 21:48:07
# Size of source mod 2**32: 14063 bytes
import unittest, functools, asyncio
from grpc import RpcError
from aioetcd3.client import client
from aioetcd3.help import range_all, range_prefix
from aioetcd3.watch import EVENT_TYPE_CREATE, EVENT_TYPE_DELETE, EVENT_TYPE_MODIFY, CompactRevisonException, WatchException

def asynctest(f):

    @functools.wraps(f)
    def _f(self):
        return asyncio.get_event_loop().run_until_complete(f(self))

    return _f


class WatchTest(unittest.TestCase):

    def setUp(self):
        self.endpoints = '127.0.0.1:2379'
        self.client = client(endpoint=(self.endpoints))
        self.tearDown()

    @asynctest
    async def test_watch_1(self):
        f1 = asyncio.get_event_loop().create_future()

        async def watch_1--- This code section failed: ---

 L.  30         0  LOAD_CONST               0
                2  STORE_FAST               'i'

 L.  31         4  LOAD_DEREF               'self'
                6  LOAD_ATTR                client
                8  LOAD_ATTR                watch_scope
               10  LOAD_STR                 '/foo'
               12  CALL_FUNCTION_1       1  ''
               14  BEFORE_ASYNC_WITH
               16  GET_AWAITABLE    
               18  LOAD_CONST               None
               20  YIELD_FROM       
               22  SETUP_ASYNC_WITH    242  'to 242'
               24  STORE_FAST               'response'

 L.  32        26  LOAD_DEREF               'f1'
               28  LOAD_ATTR                set_result
               30  LOAD_CONST               None
               32  CALL_FUNCTION_1       1  ''
               34  POP_TOP          

 L.  33        36  SETUP_LOOP          238  'to 238'
               38  LOAD_FAST                'response'
               40  GET_AITER        
               42  LOAD_CONST               None
               44  YIELD_FROM       
               46  SETUP_EXCEPT         60  'to 60'
               48  GET_ANEXT        
               50  LOAD_CONST               None
               52  YIELD_FROM       
               54  STORE_FAST               'event'
               56  POP_BLOCK        
               58  JUMP_FORWARD         82  'to 82'
             60_0  COME_FROM_EXCEPT     46  '46'
               60  DUP_TOP          
               62  LOAD_GLOBAL              StopAsyncIteration
               64  COMPARE_OP               exception-match
               66  POP_JUMP_IF_FALSE    80  'to 80'
               68  POP_TOP          
               70  POP_TOP          
               72  POP_TOP          
               74  POP_EXCEPT       
               76  POP_BLOCK        
               78  JUMP_ABSOLUTE       238  'to 238'
               80  END_FINALLY      
             82_0  COME_FROM            58  '58'

 L.  34        82  LOAD_FAST                'i'
               84  LOAD_CONST               1
               86  BINARY_ADD       
               88  STORE_FAST               'i'

 L.  35        90  LOAD_FAST                'i'
               92  LOAD_CONST               1
               94  COMPARE_OP               ==
               96  POP_JUMP_IF_FALSE   142  'to 142'

 L.  36        98  LOAD_DEREF               'self'
              100  LOAD_ATTR                assertEqual
              102  LOAD_FAST                'event'
              104  LOAD_ATTR                type
              106  LOAD_GLOBAL              EVENT_TYPE_CREATE
              108  CALL_FUNCTION_2       2  ''
              110  POP_TOP          

 L.  37       112  LOAD_DEREF               'self'
              114  LOAD_ATTR                assertEqual
              116  LOAD_FAST                'event'
              118  LOAD_ATTR                key
              120  LOAD_STR                 '/foo'
              122  CALL_FUNCTION_2       2  ''
              124  POP_TOP          

 L.  38       126  LOAD_DEREF               'self'
              128  LOAD_ATTR                assertEqual
              130  LOAD_FAST                'event'
              132  LOAD_ATTR                value
              134  LOAD_STR                 'foo'
              136  CALL_FUNCTION_2       2  ''
              138  POP_TOP          
              140  JUMP_BACK            46  'to 46'
              142  ELSE                     '232'

 L.  39       142  LOAD_FAST                'i'
              144  LOAD_CONST               2
              146  COMPARE_OP               ==
              148  POP_JUMP_IF_FALSE   194  'to 194'

 L.  40       150  LOAD_DEREF               'self'
              152  LOAD_ATTR                assertEqual
              154  LOAD_FAST                'event'
              156  LOAD_ATTR                type
              158  LOAD_GLOBAL              EVENT_TYPE_MODIFY
              160  CALL_FUNCTION_2       2  ''
              162  POP_TOP          

 L.  41       164  LOAD_DEREF               'self'
              166  LOAD_ATTR                assertEqual
              168  LOAD_FAST                'event'
              170  LOAD_ATTR                key
              172  LOAD_STR                 '/foo'
              174  CALL_FUNCTION_2       2  ''
              176  POP_TOP          

 L.  42       178  LOAD_DEREF               'self'
              180  LOAD_ATTR                assertEqual
              182  LOAD_FAST                'event'
              184  LOAD_ATTR                value
              186  LOAD_STR                 'foo1'
              188  CALL_FUNCTION_2       2  ''
              190  POP_TOP          
              192  JUMP_BACK            46  'to 46'
              194  ELSE                     '232'

 L.  43       194  LOAD_FAST                'i'
              196  LOAD_CONST               3
              198  COMPARE_OP               ==
              200  POP_JUMP_IF_FALSE    46  'to 46'

 L.  44       202  LOAD_DEREF               'self'
              204  LOAD_ATTR                assertEqual
              206  LOAD_FAST                'event'
              208  LOAD_ATTR                type
              210  LOAD_GLOBAL              EVENT_TYPE_DELETE
              212  CALL_FUNCTION_2       2  ''
              214  POP_TOP          

 L.  45       216  LOAD_DEREF               'self'
              218  LOAD_ATTR                assertEqual
              220  LOAD_FAST                'event'
              222  LOAD_ATTR                key
              224  LOAD_STR                 '/foo'
              226  CALL_FUNCTION_2       2  ''
              228  POP_TOP          

 L.  48       230  BREAK_LOOP       
            232_0  COME_FROM           200  '200'
              232  JUMP_BACK            46  'to 46'
              234  POP_BLOCK        
              236  JUMP_ABSOLUTE       238  'to 238'
            238_0  COME_FROM_LOOP       36  '36'
              238  POP_BLOCK        
              240  LOAD_CONST               None
            242_0  COME_FROM_ASYNC_WITH    22  '22'
              242  WITH_CLEANUP_START
              244  GET_AWAITABLE    
              246  LOAD_CONST               None
              248  YIELD_FROM       
              250  WITH_CLEANUP_FINISH
              252  END_FINALLY      

Parse error at or near `JUMP_ABSOLUTE' instruction at offset 236

        f2 = asyncio.get_event_loop().create_future()

        async def watch_2--- This code section failed: ---

 L.  52         0  LOAD_CONST               0
                2  STORE_FAST               'i'

 L.  53         4  SETUP_LOOP          254  'to 254'
                6  LOAD_DEREF               'self'
                8  LOAD_ATTR                client
               10  LOAD_ATTR                watch
               12  LOAD_STR                 '/foo'
               14  LOAD_CONST               True
               16  LOAD_CONST               True
               18  LOAD_CONST               ('prev_kv', 'create_event')
               20  CALL_FUNCTION_KW_3     3  '3 total positional and keyword args'
               22  GET_AITER        
               24  LOAD_CONST               None
               26  YIELD_FROM       
               28  SETUP_EXCEPT         42  'to 42'
               30  GET_ANEXT        
               32  LOAD_CONST               None
               34  YIELD_FROM       
               36  STORE_FAST               'event'
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
               60  JUMP_ABSOLUTE       254  'to 254'
               62  END_FINALLY      
             64_0  COME_FROM            40  '40'

 L.  54        64  LOAD_FAST                'event'
               66  LOAD_CONST               None
               68  COMPARE_OP               is
               70  POP_JUMP_IF_FALSE    84  'to 84'

 L.  55        72  LOAD_DEREF               'f2'
               74  LOAD_ATTR                set_result
               76  LOAD_CONST               None
               78  CALL_FUNCTION_1       1  ''
               80  POP_TOP          

 L.  56        82  CONTINUE             28  'to 28'

 L.  58        84  LOAD_FAST                'i'
               86  LOAD_CONST               1
               88  BINARY_ADD       
               90  STORE_FAST               'i'

 L.  59        92  LOAD_FAST                'i'
               94  LOAD_CONST               1
               96  COMPARE_OP               ==
               98  POP_JUMP_IF_FALSE   144  'to 144'

 L.  60       100  LOAD_DEREF               'self'
              102  LOAD_ATTR                assertEqual
              104  LOAD_FAST                'event'
              106  LOAD_ATTR                type
              108  LOAD_GLOBAL              EVENT_TYPE_CREATE
              110  CALL_FUNCTION_2       2  ''
              112  POP_TOP          

 L.  61       114  LOAD_DEREF               'self'
              116  LOAD_ATTR                assertEqual
              118  LOAD_FAST                'event'
              120  LOAD_ATTR                key
              122  LOAD_STR                 '/foo'
              124  CALL_FUNCTION_2       2  ''
              126  POP_TOP          

 L.  62       128  LOAD_DEREF               'self'
              130  LOAD_ATTR                assertEqual
              132  LOAD_FAST                'event'
              134  LOAD_ATTR                value
              136  LOAD_STR                 'foo'
              138  CALL_FUNCTION_2       2  ''
              140  POP_TOP          
              142  JUMP_BACK            28  'to 28'
              144  ELSE                     '248'

 L.  63       144  LOAD_FAST                'i'
              146  LOAD_CONST               2
              148  COMPARE_OP               ==
              150  POP_JUMP_IF_FALSE   210  'to 210'

 L.  64       152  LOAD_DEREF               'self'
              154  LOAD_ATTR                assertEqual
              156  LOAD_FAST                'event'
              158  LOAD_ATTR                type
              160  LOAD_GLOBAL              EVENT_TYPE_MODIFY
              162  CALL_FUNCTION_2       2  ''
              164  POP_TOP          

 L.  65       166  LOAD_DEREF               'self'
              168  LOAD_ATTR                assertEqual
              170  LOAD_FAST                'event'
              172  LOAD_ATTR                key
              174  LOAD_STR                 '/foo'
              176  CALL_FUNCTION_2       2  ''
              178  POP_TOP          

 L.  66       180  LOAD_DEREF               'self'
              182  LOAD_ATTR                assertEqual
              184  LOAD_FAST                'event'
              186  LOAD_ATTR                value
              188  LOAD_STR                 'foo1'
              190  CALL_FUNCTION_2       2  ''
              192  POP_TOP          

 L.  67       194  LOAD_DEREF               'self'
              196  LOAD_ATTR                assertEqual
              198  LOAD_FAST                'event'
              200  LOAD_ATTR                pre_value
              202  LOAD_STR                 'foo'
              204  CALL_FUNCTION_2       2  ''
              206  POP_TOP          
              208  JUMP_BACK            28  'to 28'
              210  ELSE                     '248'

 L.  68       210  LOAD_FAST                'i'
              212  LOAD_CONST               3
              214  COMPARE_OP               ==
              216  POP_JUMP_IF_FALSE    28  'to 28'

 L.  69       218  LOAD_DEREF               'self'
              220  LOAD_ATTR                assertEqual
              222  LOAD_FAST                'event'
              224  LOAD_ATTR                type
              226  LOAD_GLOBAL              EVENT_TYPE_DELETE
              228  CALL_FUNCTION_2       2  ''
              230  POP_TOP          

 L.  70       232  LOAD_DEREF               'self'
              234  LOAD_ATTR                assertEqual
              236  LOAD_FAST                'event'
              238  LOAD_ATTR                key
              240  LOAD_STR                 '/foo'
              242  CALL_FUNCTION_2       2  ''
              244  POP_TOP          

 L.  72       246  BREAK_LOOP       
            248_0  COME_FROM           216  '216'
              248  JUMP_BACK            28  'to 28'
              250  POP_BLOCK        
              252  JUMP_ABSOLUTE       254  'to 254'
            254_0  COME_FROM_LOOP        4  '4'

Parse error at or near `JUMP_ABSOLUTE' instruction at offset 252

        f3 = asyncio.get_event_loop().create_future()

        async def watch_3--- This code section failed: ---

 L.  76         0  LOAD_CONST               0
                2  STORE_FAST               'i'

 L.  77         4  SETUP_LOOP          138  'to 138'
                6  LOAD_DEREF               'self'
                8  LOAD_ATTR                client
               10  LOAD_ATTR                watch
               12  LOAD_STR                 '/foo'
               14  LOAD_CONST               True
               16  LOAD_CONST               True
               18  LOAD_CONST               True
               20  LOAD_CONST               ('prev_kv', 'noput', 'create_event')
               22  CALL_FUNCTION_KW_4     4  '4 total positional and keyword args'
               24  GET_AITER        
               26  LOAD_CONST               None
               28  YIELD_FROM       
               30  SETUP_EXCEPT         44  'to 44'
               32  GET_ANEXT        
               34  LOAD_CONST               None
               36  YIELD_FROM       
               38  STORE_FAST               'event'
               40  POP_BLOCK        
               42  JUMP_FORWARD         66  'to 66'
             44_0  COME_FROM_EXCEPT     30  '30'
               44  DUP_TOP          
               46  LOAD_GLOBAL              StopAsyncIteration
               48  COMPARE_OP               exception-match
               50  POP_JUMP_IF_FALSE    64  'to 64'
               52  POP_TOP          
               54  POP_TOP          
               56  POP_TOP          
               58  POP_EXCEPT       
               60  POP_BLOCK        
               62  JUMP_ABSOLUTE       138  'to 138'
               64  END_FINALLY      
             66_0  COME_FROM            42  '42'

 L.  78        66  LOAD_FAST                'event'
               68  LOAD_CONST               None
               70  COMPARE_OP               is
               72  POP_JUMP_IF_FALSE    86  'to 86'

 L.  79        74  LOAD_DEREF               'f3'
               76  LOAD_ATTR                set_result
               78  LOAD_CONST               None
               80  CALL_FUNCTION_1       1  ''
               82  POP_TOP          

 L.  80        84  CONTINUE             30  'to 30'

 L.  82        86  LOAD_FAST                'i'
               88  LOAD_CONST               1
               90  BINARY_ADD       
               92  STORE_FAST               'i'

 L.  83        94  LOAD_FAST                'i'
               96  LOAD_CONST               1
               98  COMPARE_OP               ==
              100  POP_JUMP_IF_FALSE    30  'to 30'

 L.  84       102  LOAD_DEREF               'self'
              104  LOAD_ATTR                assertEqual
              106  LOAD_FAST                'event'
              108  LOAD_ATTR                type
              110  LOAD_GLOBAL              EVENT_TYPE_DELETE
              112  CALL_FUNCTION_2       2  ''
              114  POP_TOP          

 L.  85       116  LOAD_DEREF               'self'
              118  LOAD_ATTR                assertEqual
              120  LOAD_FAST                'event'
              122  LOAD_ATTR                key
              124  LOAD_STR                 '/foo'
              126  CALL_FUNCTION_2       2  ''
              128  POP_TOP          

 L.  87       130  BREAK_LOOP       
            132_0  COME_FROM           100  '100'
              132  JUMP_BACK            30  'to 30'
              134  POP_BLOCK        
              136  JUMP_ABSOLUTE       138  'to 138'
            138_0  COME_FROM_LOOP        4  '4'

Parse error at or near `JUMP_ABSOLUTE' instruction at offset 136

        f4 = asyncio.get_event_loop().create_future()

        async def watch_4--- This code section failed: ---

 L.  91         0  LOAD_CONST               0
                2  STORE_FAST               'i'

 L.  92         4  SETUP_LOOP          218  'to 218'
                6  LOAD_DEREF               'self'
                8  LOAD_ATTR                client
               10  LOAD_ATTR                watch
               12  LOAD_STR                 '/foo'
               14  LOAD_CONST               True
               16  LOAD_CONST               True
               18  LOAD_CONST               True
               20  LOAD_CONST               ('prev_kv', 'nodelete', 'create_event')
               22  CALL_FUNCTION_KW_4     4  '4 total positional and keyword args'
               24  GET_AITER        
               26  LOAD_CONST               None
               28  YIELD_FROM       
               30  SETUP_EXCEPT         44  'to 44'
               32  GET_ANEXT        
               34  LOAD_CONST               None
               36  YIELD_FROM       
               38  STORE_FAST               'event'
               40  POP_BLOCK        
               42  JUMP_FORWARD         66  'to 66'
             44_0  COME_FROM_EXCEPT     30  '30'
               44  DUP_TOP          
               46  LOAD_GLOBAL              StopAsyncIteration
               48  COMPARE_OP               exception-match
               50  POP_JUMP_IF_FALSE    64  'to 64'
               52  POP_TOP          
               54  POP_TOP          
               56  POP_TOP          
               58  POP_EXCEPT       
               60  POP_BLOCK        
               62  JUMP_ABSOLUTE       218  'to 218'
               64  END_FINALLY      
             66_0  COME_FROM            42  '42'

 L.  93        66  LOAD_FAST                'event'
               68  LOAD_CONST               None
               70  COMPARE_OP               is
               72  POP_JUMP_IF_FALSE    86  'to 86'

 L.  94        74  LOAD_DEREF               'f4'
               76  LOAD_ATTR                set_result
               78  LOAD_CONST               None
               80  CALL_FUNCTION_1       1  ''
               82  POP_TOP          

 L.  95        84  CONTINUE             30  'to 30'

 L.  97        86  LOAD_FAST                'i'
               88  LOAD_CONST               1
               90  BINARY_ADD       
               92  STORE_FAST               'i'

 L.  98        94  LOAD_FAST                'i'
               96  LOAD_CONST               1
               98  COMPARE_OP               ==
              100  POP_JUMP_IF_FALSE   146  'to 146'

 L.  99       102  LOAD_DEREF               'self'
              104  LOAD_ATTR                assertEqual
              106  LOAD_FAST                'event'
              108  LOAD_ATTR                type
              110  LOAD_GLOBAL              EVENT_TYPE_CREATE
              112  CALL_FUNCTION_2       2  ''
              114  POP_TOP          

 L. 100       116  LOAD_DEREF               'self'
              118  LOAD_ATTR                assertEqual
              120  LOAD_FAST                'event'
              122  LOAD_ATTR                key
              124  LOAD_STR                 '/foo'
              126  CALL_FUNCTION_2       2  ''
              128  POP_TOP          

 L. 101       130  LOAD_DEREF               'self'
              132  LOAD_ATTR                assertEqual
              134  LOAD_FAST                'event'
              136  LOAD_ATTR                value
              138  LOAD_STR                 'foo'
              140  CALL_FUNCTION_2       2  ''
              142  POP_TOP          
              144  JUMP_BACK            30  'to 30'
              146  ELSE                     '212'

 L. 102       146  LOAD_FAST                'i'
              148  LOAD_CONST               2
              150  COMPARE_OP               ==
              152  POP_JUMP_IF_FALSE    30  'to 30'

 L. 103       154  LOAD_DEREF               'self'
              156  LOAD_ATTR                assertEqual
              158  LOAD_FAST                'event'
              160  LOAD_ATTR                type
              162  LOAD_GLOBAL              EVENT_TYPE_MODIFY
              164  CALL_FUNCTION_2       2  ''
              166  POP_TOP          

 L. 104       168  LOAD_DEREF               'self'
              170  LOAD_ATTR                assertEqual
              172  LOAD_FAST                'event'
              174  LOAD_ATTR                key
              176  LOAD_STR                 '/foo'
              178  CALL_FUNCTION_2       2  ''
              180  POP_TOP          

 L. 105       182  LOAD_DEREF               'self'
              184  LOAD_ATTR                assertEqual
              186  LOAD_FAST                'event'
              188  LOAD_ATTR                value
              190  LOAD_STR                 'foo1'
              192  CALL_FUNCTION_2       2  ''
              194  POP_TOP          

 L. 106       196  LOAD_DEREF               'self'
              198  LOAD_ATTR                assertEqual
              200  LOAD_FAST                'event'
              202  LOAD_ATTR                pre_value
              204  LOAD_STR                 'foo'
              206  CALL_FUNCTION_2       2  ''
              208  POP_TOP          

 L. 107       210  BREAK_LOOP       
            212_0  COME_FROM           152  '152'
              212  JUMP_BACK            30  'to 30'
              214  POP_BLOCK        
              216  JUMP_ABSOLUTE       218  'to 218'
            218_0  COME_FROM_LOOP        4  '4'

Parse error at or near `JUMP_ABSOLUTE' instruction at offset 216

        w1 = asyncio.ensure_future(watch_1())
        w2 = asyncio.ensure_future(watch_2())
        w3 = asyncio.ensure_future(watch_3())
        w4 = asyncio.ensure_future(watch_4())
        await asyncio.wait_for(asyncio.wait([f1, f2, f3, f4]), 2)
        await self.client.put('/foo', 'foo')
        await self.client.put('/foo', 'foo1')
        await self.client.delete('/foo')
        done, pending = await asyncio.wait([w1, w2, w3, w4], timeout=20)
        for t in done:
            t.result()

    @asynctest
    async def test_watch_reconnect(self):
        f1 = asyncio.get_event_loop().create_future()
        f2 = asyncio.get_event_loop().create_future()

        async def watch_1--- This code section failed: ---

 L. 129         0  LOAD_CONST               0
                2  STORE_FAST               'i'

 L. 130         4  LOAD_DEREF               'self'
                6  LOAD_ATTR                client
                8  LOAD_ATTR                watch_scope
               10  LOAD_STR                 '/foo'
               12  CALL_FUNCTION_1       1  ''
               14  BEFORE_ASYNC_WITH
               16  GET_AWAITABLE    
               18  LOAD_CONST               None
               20  YIELD_FROM       
               22  SETUP_ASYNC_WITH    252  'to 252'
               24  STORE_FAST               'response'

 L. 131        26  LOAD_DEREF               'f1'
               28  LOAD_ATTR                set_result
               30  LOAD_CONST               None
               32  CALL_FUNCTION_1       1  ''
               34  POP_TOP          

 L. 132        36  SETUP_LOOP          248  'to 248'
               38  LOAD_FAST                'response'
               40  GET_AITER        
               42  LOAD_CONST               None
               44  YIELD_FROM       
               46  SETUP_EXCEPT         60  'to 60'
               48  GET_ANEXT        
               50  LOAD_CONST               None
               52  YIELD_FROM       
               54  STORE_FAST               'event'
               56  POP_BLOCK        
               58  JUMP_FORWARD         82  'to 82'
             60_0  COME_FROM_EXCEPT     46  '46'
               60  DUP_TOP          
               62  LOAD_GLOBAL              StopAsyncIteration
               64  COMPARE_OP               exception-match
               66  POP_JUMP_IF_FALSE    80  'to 80'
               68  POP_TOP          
               70  POP_TOP          
               72  POP_TOP          
               74  POP_EXCEPT       
               76  POP_BLOCK        
               78  JUMP_ABSOLUTE       248  'to 248'
               80  END_FINALLY      
             82_0  COME_FROM            58  '58'

 L. 133        82  LOAD_FAST                'i'
               84  LOAD_CONST               1
               86  BINARY_ADD       
               88  STORE_FAST               'i'

 L. 134        90  LOAD_FAST                'i'
               92  LOAD_CONST               1
               94  COMPARE_OP               ==
               96  POP_JUMP_IF_FALSE   152  'to 152'

 L. 135        98  LOAD_DEREF               'self'
              100  LOAD_ATTR                assertEqual
              102  LOAD_FAST                'event'
              104  LOAD_ATTR                type
              106  LOAD_GLOBAL              EVENT_TYPE_CREATE
              108  CALL_FUNCTION_2       2  ''
              110  POP_TOP          

 L. 136       112  LOAD_DEREF               'self'
              114  LOAD_ATTR                assertEqual
              116  LOAD_FAST                'event'
              118  LOAD_ATTR                key
              120  LOAD_STR                 '/foo'
              122  CALL_FUNCTION_2       2  ''
              124  POP_TOP          

 L. 137       126  LOAD_DEREF               'self'
              128  LOAD_ATTR                assertEqual
              130  LOAD_FAST                'event'
              132  LOAD_ATTR                value
              134  LOAD_STR                 'foo'
              136  CALL_FUNCTION_2       2  ''
              138  POP_TOP          

 L. 138       140  LOAD_DEREF               'f2'
              142  LOAD_ATTR                set_result
              144  LOAD_CONST               None
              146  CALL_FUNCTION_1       1  ''
              148  POP_TOP          
              150  JUMP_BACK            46  'to 46'
              152  ELSE                     '242'

 L. 139       152  LOAD_FAST                'i'
              154  LOAD_CONST               2
              156  COMPARE_OP               ==
              158  POP_JUMP_IF_FALSE   204  'to 204'

 L. 140       160  LOAD_DEREF               'self'
              162  LOAD_ATTR                assertEqual
              164  LOAD_FAST                'event'
              166  LOAD_ATTR                type
              168  LOAD_GLOBAL              EVENT_TYPE_MODIFY
              170  CALL_FUNCTION_2       2  ''
              172  POP_TOP          

 L. 141       174  LOAD_DEREF               'self'
              176  LOAD_ATTR                assertEqual
              178  LOAD_FAST                'event'
              180  LOAD_ATTR                key
              182  LOAD_STR                 '/foo'
              184  CALL_FUNCTION_2       2  ''
              186  POP_TOP          

 L. 142       188  LOAD_DEREF               'self'
              190  LOAD_ATTR                assertEqual
              192  LOAD_FAST                'event'
              194  LOAD_ATTR                value
              196  LOAD_STR                 'foo1'
              198  CALL_FUNCTION_2       2  ''
              200  POP_TOP          
              202  JUMP_BACK            46  'to 46'
              204  ELSE                     '242'

 L. 143       204  LOAD_FAST                'i'
              206  LOAD_CONST               3
              208  COMPARE_OP               ==
              210  POP_JUMP_IF_FALSE    46  'to 46'

 L. 144       212  LOAD_DEREF               'self'
              214  LOAD_ATTR                assertEqual
              216  LOAD_FAST                'event'
              218  LOAD_ATTR                type
              220  LOAD_GLOBAL              EVENT_TYPE_DELETE
              222  CALL_FUNCTION_2       2  ''
              224  POP_TOP          

 L. 145       226  LOAD_DEREF               'self'
              228  LOAD_ATTR                assertEqual
              230  LOAD_FAST                'event'
              232  LOAD_ATTR                key
              234  LOAD_STR                 '/foo'
              236  CALL_FUNCTION_2       2  ''
              238  POP_TOP          

 L. 148       240  BREAK_LOOP       
            242_0  COME_FROM           210  '210'
              242  JUMP_BACK            46  'to 46'
              244  POP_BLOCK        
              246  JUMP_ABSOLUTE       248  'to 248'
            248_0  COME_FROM_LOOP       36  '36'
              248  POP_BLOCK        
              250  LOAD_CONST               None
            252_0  COME_FROM_ASYNC_WITH    22  '22'
              252  WITH_CLEANUP_START
              254  GET_AWAITABLE    
              256  LOAD_CONST               None
              258  YIELD_FROM       
              260  WITH_CLEANUP_FINISH
              262  END_FINALLY      

Parse error at or near `JUMP_ABSOLUTE' instruction at offset 246

        t1 = asyncio.ensure_future(watch_1())
        await f1
        await self.client.put('/foo', 'foo')
        await f2
        self.client.update_server_list(self.endpoints)
        await self.client.put('/foo', 'foo1')
        await self.client.delete('/foo')
        await t1

    @asynctest
    async def test_watch_create_cancel(self):

        async def watch_1():
            async with self.client.watch_scope('/foo') as _:
                pass

        async def watch_2():
            async with self.client.watch_scope('/foo') as _:
                await asyncio.sleep(5)

        for _ in range(0, 5):
            watches = [asyncio.ensure_future(watch_1() if i % 2 else watch_2()) for i in range(0, 200)]
            await asyncio.sleep(1)
            for w in watches[::3]:
                w.cancel()

            self.client.update_server_list(self.endpoints)
            await asyncio.sleep(0.01)
            for w in watches[1::3]:
                w.cancel()

            await asyncio.sleep(0.3)
            for w in watches[2::3]:
                w.cancel()

            await asyncio.wait_for(asyncio.wait(watches), 3)
            results = await (asyncio.gather)(*watches, **{'return_exceptions': True})
            print('Finished:', len([r for r in results if r is None]), 'Cancelled:', len([r for r in results if r is not None]))
            self.assertIsNotNone(self.client._watch_task_running)

        await asyncio.sleep(3)
        self.assertIsNone(self.client._watch_task_running)

    @asynctest
    async def test_batch_events(self):
        f1 = asyncio.get_event_loop().create_future()
        f2 = asyncio.get_event_loop().create_future()

        def _check_event(e, criterias):
            if criterias[0]:
                self.assertEqual(e.type, criterias[0])
            else:
                if criterias[1]:
                    self.assertEqual(e.key, criterias[1])
                if criterias[2]:
                    self.assertEqual(e.value, criterias[2])

        async def watch_1--- This code section failed: ---

 L. 197         0  LOAD_GLOBAL              EVENT_TYPE_CREATE
                2  LOAD_STR                 '/foo/1'
                4  LOAD_STR                 '1'
                6  BUILD_TUPLE_3         3 

 L. 198         8  LOAD_GLOBAL              EVENT_TYPE_CREATE
               10  LOAD_STR                 '/foo/2'
               12  LOAD_STR                 '2'
               14  BUILD_TUPLE_3         3 

 L. 199        16  LOAD_GLOBAL              EVENT_TYPE_MODIFY
               18  LOAD_STR                 '/foo/1'
               20  LOAD_STR                 '2'
               22  BUILD_TUPLE_3         3 

 L. 200        24  LOAD_GLOBAL              EVENT_TYPE_MODIFY
               26  LOAD_STR                 '/foo/2'
               28  LOAD_STR                 '3'
               30  BUILD_TUPLE_3         3 

 L. 201        32  LOAD_GLOBAL              EVENT_TYPE_DELETE
               34  LOAD_STR                 '/foo/1'
               36  LOAD_CONST               None
               38  BUILD_TUPLE_3         3 

 L. 202        40  LOAD_GLOBAL              EVENT_TYPE_DELETE
               42  LOAD_STR                 '/foo/2'
               44  LOAD_CONST               None
               46  BUILD_TUPLE_3         3 
               48  BUILD_LIST_6          6 
               50  STORE_FAST               'asserts'

 L. 203        52  LOAD_DEREF               'self'
               54  LOAD_ATTR                client
               56  LOAD_ATTR                watch_scope
               58  LOAD_GLOBAL              range_prefix
               60  LOAD_STR                 '/foo/'
               62  CALL_FUNCTION_1       1  ''
               64  CALL_FUNCTION_1       1  ''
               66  BEFORE_ASYNC_WITH
               68  GET_AWAITABLE    
               70  LOAD_CONST               None
               72  YIELD_FROM       
               74  SETUP_ASYNC_WITH    166  'to 166'
               76  STORE_FAST               'response'

 L. 204        78  LOAD_DEREF               'f1'
               80  LOAD_ATTR                set_result
               82  LOAD_CONST               None
               84  CALL_FUNCTION_1       1  ''
               86  POP_TOP          

 L. 205        88  SETUP_LOOP          162  'to 162'
               90  LOAD_FAST                'response'
               92  GET_AITER        
               94  LOAD_CONST               None
               96  YIELD_FROM       
               98  SETUP_EXCEPT        112  'to 112'
              100  GET_ANEXT        
              102  LOAD_CONST               None
              104  YIELD_FROM       
              106  STORE_FAST               'e'
              108  POP_BLOCK        
              110  JUMP_FORWARD        134  'to 134'
            112_0  COME_FROM_EXCEPT     98  '98'
              112  DUP_TOP          
              114  LOAD_GLOBAL              StopAsyncIteration
              116  COMPARE_OP               exception-match
              118  POP_JUMP_IF_FALSE   132  'to 132'
              120  POP_TOP          
              122  POP_TOP          
              124  POP_TOP          
              126  POP_EXCEPT       
              128  POP_BLOCK        
              130  JUMP_ABSOLUTE       162  'to 162'
              132  END_FINALLY      
            134_0  COME_FROM           110  '110'

 L. 206       134  LOAD_DEREF               '_check_event'
              136  LOAD_FAST                'e'
              138  LOAD_FAST                'asserts'
              140  LOAD_ATTR                pop
              142  LOAD_CONST               0
              144  CALL_FUNCTION_1       1  ''
              146  CALL_FUNCTION_2       2  ''
              148  POP_TOP          

 L. 207       150  LOAD_FAST                'asserts'
              152  POP_JUMP_IF_TRUE     98  'to 98'

 L. 208       154  BREAK_LOOP       
            156_0  COME_FROM           152  '152'
              156  JUMP_BACK            98  'to 98'
              158  POP_BLOCK        
              160  JUMP_ABSOLUTE       162  'to 162'
            162_0  COME_FROM_LOOP       88  '88'
              162  POP_BLOCK        
              164  LOAD_CONST               None
            166_0  COME_FROM_ASYNC_WITH    74  '74'
              166  WITH_CLEANUP_START
              168  GET_AWAITABLE    
              170  LOAD_CONST               None
              172  YIELD_FROM       
              174  WITH_CLEANUP_FINISH
              176  END_FINALLY      

Parse error at or near `JUMP_ABSOLUTE' instruction at offset 160

        async def watch_2--- This code section failed: ---

 L. 211         0  LOAD_GLOBAL              EVENT_TYPE_CREATE
                2  LOAD_STR                 '/foo/1'
                4  LOAD_STR                 '1'
                6  BUILD_TUPLE_3         3 

 L. 212         8  LOAD_GLOBAL              EVENT_TYPE_CREATE
               10  LOAD_STR                 '/foo/2'
               12  LOAD_STR                 '2'
               14  BUILD_TUPLE_3         3 
               16  BUILD_TUPLE_2         2 

 L. 213        18  LOAD_GLOBAL              EVENT_TYPE_MODIFY
               20  LOAD_STR                 '/foo/1'
               22  LOAD_STR                 '2'
               24  BUILD_TUPLE_3         3 
               26  BUILD_TUPLE_1         1 

 L. 214        28  LOAD_GLOBAL              EVENT_TYPE_MODIFY
               30  LOAD_STR                 '/foo/2'
               32  LOAD_STR                 '3'
               34  BUILD_TUPLE_3         3 
               36  BUILD_TUPLE_1         1 

 L. 215        38  LOAD_GLOBAL              EVENT_TYPE_DELETE
               40  LOAD_STR                 '/foo/1'
               42  LOAD_CONST               None
               44  BUILD_TUPLE_3         3 

 L. 216        46  LOAD_GLOBAL              EVENT_TYPE_DELETE
               48  LOAD_STR                 '/foo/2'
               50  LOAD_CONST               None
               52  BUILD_TUPLE_3         3 
               54  BUILD_TUPLE_2         2 
               56  BUILD_LIST_4          4 
               58  STORE_FAST               'asserts'

 L. 217        60  LOAD_DEREF               'self'
               62  LOAD_ATTR                client
               64  LOAD_ATTR                watch_scope
               66  LOAD_GLOBAL              range_prefix
               68  LOAD_STR                 '/foo/'
               70  CALL_FUNCTION_1       1  ''
               72  LOAD_CONST               True
               74  LOAD_CONST               ('batch_events',)
               76  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
               78  BEFORE_ASYNC_WITH
               80  GET_AWAITABLE    
               82  LOAD_CONST               None
               84  YIELD_FROM       
               86  SETUP_ASYNC_WITH    226  'to 226'

 L. 218        88  STORE_FAST               'response'

 L. 219        90  LOAD_DEREF               'f2'
               92  LOAD_ATTR                set_result
               94  LOAD_CONST               None
               96  CALL_FUNCTION_1       1  ''
               98  POP_TOP          

 L. 220       100  SETUP_LOOP          222  'to 222'
              102  LOAD_FAST                'response'
              104  GET_AITER        
              106  LOAD_CONST               None
              108  YIELD_FROM       
              110  SETUP_EXCEPT        124  'to 124'
              112  GET_ANEXT        
              114  LOAD_CONST               None
              116  YIELD_FROM       
              118  STORE_FAST               'es'
              120  POP_BLOCK        
              122  JUMP_FORWARD        146  'to 146'
            124_0  COME_FROM_EXCEPT    110  '110'
              124  DUP_TOP          
              126  LOAD_GLOBAL              StopAsyncIteration
              128  COMPARE_OP               exception-match
              130  POP_JUMP_IF_FALSE   144  'to 144'
              132  POP_TOP          
              134  POP_TOP          
              136  POP_TOP          
              138  POP_EXCEPT       
              140  POP_BLOCK        
              142  JUMP_ABSOLUTE       222  'to 222'
              144  END_FINALLY      
            146_0  COME_FROM           122  '122'

 L. 221       146  LOAD_FAST                'asserts'
              148  LOAD_ATTR                pop
              150  LOAD_CONST               0
              152  CALL_FUNCTION_1       1  ''
              154  STORE_FAST               'batch'

 L. 222       156  LOAD_DEREF               'self'
              158  LOAD_ATTR                assertEqual
              160  LOAD_GLOBAL              len
              162  LOAD_FAST                'es'
              164  CALL_FUNCTION_1       1  ''
              166  LOAD_GLOBAL              len
              168  LOAD_FAST                'batch'
              170  CALL_FUNCTION_1       1  ''
              172  CALL_FUNCTION_2       2  ''
              174  POP_TOP          

 L. 223       176  SETUP_LOOP          210  'to 210'
              178  LOAD_GLOBAL              zip
              180  LOAD_FAST                'es'
              182  LOAD_FAST                'batch'
              184  CALL_FUNCTION_2       2  ''
              186  GET_ITER         
              188  FOR_ITER            208  'to 208'
              190  UNPACK_SEQUENCE_2     2 
              192  STORE_FAST               'e'
              194  STORE_FAST               'a'

 L. 224       196  LOAD_DEREF               '_check_event'
              198  LOAD_FAST                'e'
              200  LOAD_FAST                'a'
              202  CALL_FUNCTION_2       2  ''
              204  POP_TOP          
              206  JUMP_BACK           188  'to 188'
              208  POP_BLOCK        
            210_0  COME_FROM_LOOP      176  '176'

 L. 225       210  LOAD_FAST                'asserts'
              212  POP_JUMP_IF_TRUE    110  'to 110'

 L. 226       214  BREAK_LOOP       
            216_0  COME_FROM           212  '212'
              216  JUMP_BACK           110  'to 110'
              218  POP_BLOCK        
              220  JUMP_ABSOLUTE       222  'to 222'
            222_0  COME_FROM_LOOP      100  '100'
              222  POP_BLOCK        
              224  LOAD_CONST               None
            226_0  COME_FROM_ASYNC_WITH    86  '86'
              226  WITH_CLEANUP_START
              228  GET_AWAITABLE    
              230  LOAD_CONST               None
              232  YIELD_FROM       
              234  WITH_CLEANUP_FINISH
              236  END_FINALLY      

Parse error at or near `JUMP_ABSOLUTE' instruction at offset 220

        t1 = asyncio.ensure_future(watch_1())
        t2 = asyncio.ensure_future(watch_2())
        await asyncio.wait_for(asyncio.wait([f1, f2]), 2)
        self.assertTrue((await self.client.txn([], [self.client.put.txn('/foo/1', '1'),
         self.client.put.txn('/foo/2', '2')], []))[0])
        await self.client.put('/foo/1', '2')
        await self.client.put('/foo/2', '3')
        self.assertTrue((await self.client.txn([], [self.client.delete.txn('/foo/1'),
         self.client.delete.txn('/foo/2')], []))[0])
        await asyncio.gather(t1, t2)

    @asynctest
    async def test_compact_revision(self):
        await self.client.put('/foo', '1')
        first_revision = self.client.last_response_info.revision
        await self.client.put('/foo', '2')
        await self.client.put('/foo', '3')
        await self.client.put('/foo', '4')
        await self.client.put('/foo', '5')
        compact_revision = self.client.last_response_info.revision
        await self.client.compact(compact_revision, True)

        async def watch_1--- This code section failed: ---

 L. 250         0  LOAD_DEREF               'self'
                2  LOAD_ATTR                client
                4  LOAD_ATTR                watch_scope
                6  LOAD_STR                 '/foo'
                8  LOAD_DEREF               'first_revision'
               10  LOAD_CONST               ('start_revision',)
               12  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
               14  BEFORE_ASYNC_WITH
               16  GET_AWAITABLE    
               18  LOAD_CONST               None
               20  YIELD_FROM       
               22  SETUP_ASYNC_WITH    128  'to 128'
               24  STORE_FAST               'response'

 L. 251        26  LOAD_DEREF               'self'
               28  LOAD_ATTR                assertRaises
               30  LOAD_GLOBAL              CompactRevisonException
               32  CALL_FUNCTION_1       1  ''
               34  SETUP_WITH          102  'to 102'
               36  STORE_FAST               'cm'

 L. 252        38  SETUP_LOOP           98  'to 98'
               40  LOAD_FAST                'response'
               42  GET_AITER        
               44  LOAD_CONST               None
               46  YIELD_FROM       
               48  SETUP_EXCEPT         62  'to 62'
               50  GET_ANEXT        
               52  LOAD_CONST               None
               54  YIELD_FROM       
               56  STORE_FAST               'e'
               58  POP_BLOCK        
               60  JUMP_FORWARD         84  'to 84'
             62_0  COME_FROM_EXCEPT     48  '48'
               62  DUP_TOP          
               64  LOAD_GLOBAL              StopAsyncIteration
               66  COMPARE_OP               exception-match
               68  POP_JUMP_IF_FALSE    82  'to 82'
               70  POP_TOP          
               72  POP_TOP          
               74  POP_TOP          
               76  POP_EXCEPT       
               78  POP_BLOCK        
               80  JUMP_ABSOLUTE        98  'to 98'
               82  END_FINALLY      
             84_0  COME_FROM            60  '60'

 L. 253        84  LOAD_GLOBAL              ValueError
               86  LOAD_STR                 'Not raised'
               88  CALL_FUNCTION_1       1  ''
               90  RAISE_VARARGS_1       1  ''
               92  JUMP_BACK            48  'to 48'
               94  POP_BLOCK        
               96  JUMP_ABSOLUTE        98  'to 98'
             98_0  COME_FROM_LOOP       38  '38'
               98  POP_BLOCK        
              100  LOAD_CONST               None
            102_0  COME_FROM_WITH       34  '34'
              102  WITH_CLEANUP_START
              104  WITH_CLEANUP_FINISH
              106  END_FINALLY      

 L. 254       108  LOAD_DEREF               'self'
              110  LOAD_ATTR                assertEqual
              112  LOAD_FAST                'cm'
              114  LOAD_ATTR                exception
              116  LOAD_ATTR                revision
              118  LOAD_DEREF               'compact_revision'
              120  CALL_FUNCTION_2       2  ''
              122  POP_TOP          
              124  POP_BLOCK        
              126  LOAD_CONST               None
            128_0  COME_FROM_ASYNC_WITH    22  '22'
              128  WITH_CLEANUP_START
              130  GET_AWAITABLE    
              132  LOAD_CONST               None
              134  YIELD_FROM       
              136  WITH_CLEANUP_FINISH
              138  END_FINALLY      

Parse error at or near `JUMP_ABSOLUTE' instruction at offset 96

        async def watch_2--- This code section failed: ---

 L. 257         0  LOAD_DEREF               'self'
                2  LOAD_ATTR                client
                4  LOAD_ATTR                watch_scope
                6  LOAD_STR                 '/foo'
                8  LOAD_CONST               True
               10  LOAD_DEREF               'first_revision'
               12  LOAD_CONST               ('ignore_compact', 'start_revision')
               14  CALL_FUNCTION_KW_3     3  '3 total positional and keyword args'
               16  BEFORE_ASYNC_WITH
               18  GET_AWAITABLE    
               20  LOAD_CONST               None
               22  YIELD_FROM       
               24  SETUP_ASYNC_WITH    142  'to 142'
               26  STORE_FAST               'responses'

 L. 258        28  SETUP_LOOP          138  'to 138'
               30  LOAD_FAST                'responses'
               32  GET_AITER        
               34  LOAD_CONST               None
               36  YIELD_FROM       
               38  SETUP_EXCEPT         52  'to 52'
               40  GET_ANEXT        
               42  LOAD_CONST               None
               44  YIELD_FROM       
               46  STORE_FAST               'e'
               48  POP_BLOCK        
               50  JUMP_FORWARD         74  'to 74'
             52_0  COME_FROM_EXCEPT     38  '38'
               52  DUP_TOP          
               54  LOAD_GLOBAL              StopAsyncIteration
               56  COMPARE_OP               exception-match
               58  POP_JUMP_IF_FALSE    72  'to 72'
               60  POP_TOP          
               62  POP_TOP          
               64  POP_TOP          
               66  POP_EXCEPT       
               68  POP_BLOCK        
               70  JUMP_ABSOLUTE       138  'to 138'
               72  END_FINALLY      
             74_0  COME_FROM            50  '50'

 L. 259        74  LOAD_DEREF               'self'
               76  LOAD_ATTR                assertEqual
               78  LOAD_FAST                'e'
               80  LOAD_ATTR                type
               82  LOAD_GLOBAL              EVENT_TYPE_MODIFY
               84  CALL_FUNCTION_2       2  ''
               86  POP_TOP          

 L. 260        88  LOAD_DEREF               'self'
               90  LOAD_ATTR                assertEqual
               92  LOAD_FAST                'e'
               94  LOAD_ATTR                key
               96  LOAD_STR                 '/foo'
               98  CALL_FUNCTION_2       2  ''
              100  POP_TOP          

 L. 261       102  LOAD_DEREF               'self'
              104  LOAD_ATTR                assertEqual
              106  LOAD_FAST                'e'
              108  LOAD_ATTR                value
              110  LOAD_STR                 '5'
              112  CALL_FUNCTION_2       2  ''
              114  POP_TOP          

 L. 262       116  LOAD_DEREF               'self'
              118  LOAD_ATTR                assertEqual
              120  LOAD_FAST                'e'
              122  LOAD_ATTR                revision
              124  LOAD_DEREF               'compact_revision'
              126  CALL_FUNCTION_2       2  ''
              128  POP_TOP          

 L. 263       130  BREAK_LOOP       
              132  JUMP_BACK            38  'to 38'
              134  POP_BLOCK        
              136  JUMP_ABSOLUTE       138  'to 138'
            138_0  COME_FROM_LOOP       28  '28'
              138  POP_BLOCK        
              140  LOAD_CONST               None
            142_0  COME_FROM_ASYNC_WITH    24  '24'
              142  WITH_CLEANUP_START
              144  GET_AWAITABLE    
              146  LOAD_CONST               None
              148  YIELD_FROM       
              150  WITH_CLEANUP_FINISH
              152  END_FINALLY      

Parse error at or near `JUMP_ABSOLUTE' instruction at offset 136

        await watch_1()
        await watch_2()

    @asynctest
    async def test_watch_exception(self):
        f1 = asyncio.get_event_loop().create_future()
        f2 = asyncio.get_event_loop().create_future()

        async def watch_1--- This code section failed: ---

 L. 272         0  LOAD_CONST               0
                2  STORE_FAST               'i'

 L. 273         4  LOAD_DEREF               'self'
                6  LOAD_ATTR                client
                8  LOAD_ATTR                watch_scope
               10  LOAD_STR                 '/foo'
               12  CALL_FUNCTION_1       1  ''
               14  BEFORE_ASYNC_WITH
               16  GET_AWAITABLE    
               18  LOAD_CONST               None
               20  YIELD_FROM       
               22  SETUP_ASYNC_WITH    200  'to 200'
               24  STORE_FAST               'response'

 L. 274        26  LOAD_DEREF               'f1'
               28  LOAD_ATTR                set_result
               30  LOAD_CONST               None
               32  CALL_FUNCTION_1       1  ''
               34  POP_TOP          

 L. 275        36  LOAD_DEREF               'self'
               38  LOAD_ATTR                assertRaises
               40  LOAD_GLOBAL              WatchException
               42  CALL_FUNCTION_1       1  ''
               44  SETUP_WITH          190  'to 190'
               46  POP_TOP          

 L. 276        48  SETUP_LOOP          186  'to 186'
               50  LOAD_FAST                'response'
               52  GET_AITER        
               54  LOAD_CONST               None
               56  YIELD_FROM       
               58  SETUP_EXCEPT         72  'to 72'
               60  GET_ANEXT        
               62  LOAD_CONST               None
               64  YIELD_FROM       
               66  STORE_FAST               'event'
               68  POP_BLOCK        
               70  JUMP_FORWARD         94  'to 94'
             72_0  COME_FROM_EXCEPT     58  '58'
               72  DUP_TOP          
               74  LOAD_GLOBAL              StopAsyncIteration
               76  COMPARE_OP               exception-match
               78  POP_JUMP_IF_FALSE    92  'to 92'
               80  POP_TOP          
               82  POP_TOP          
               84  POP_TOP          
               86  POP_EXCEPT       
               88  POP_BLOCK        
               90  JUMP_ABSOLUTE       186  'to 186'
               92  END_FINALLY      
             94_0  COME_FROM            70  '70'

 L. 277        94  LOAD_FAST                'i'
               96  LOAD_CONST               1
               98  BINARY_ADD       
              100  STORE_FAST               'i'

 L. 278       102  LOAD_FAST                'i'
              104  LOAD_CONST               1
              106  COMPARE_OP               ==
              108  POP_JUMP_IF_FALSE   164  'to 164'

 L. 279       110  LOAD_DEREF               'self'
              112  LOAD_ATTR                assertEqual
              114  LOAD_FAST                'event'
              116  LOAD_ATTR                type
              118  LOAD_GLOBAL              EVENT_TYPE_CREATE
              120  CALL_FUNCTION_2       2  ''
              122  POP_TOP          

 L. 280       124  LOAD_DEREF               'self'
              126  LOAD_ATTR                assertEqual
              128  LOAD_FAST                'event'
              130  LOAD_ATTR                key
              132  LOAD_STR                 '/foo'
              134  CALL_FUNCTION_2       2  ''
              136  POP_TOP          

 L. 281       138  LOAD_DEREF               'self'
              140  LOAD_ATTR                assertEqual
              142  LOAD_FAST                'event'
              144  LOAD_ATTR                value
              146  LOAD_STR                 'foo'
              148  CALL_FUNCTION_2       2  ''
              150  POP_TOP          

 L. 282       152  LOAD_DEREF               'f2'
              154  LOAD_ATTR                set_result
              156  LOAD_CONST               None
              158  CALL_FUNCTION_1       1  ''
              160  POP_TOP          
              162  JUMP_BACK            58  'to 58'
              164  ELSE                     '180'

 L. 283       164  LOAD_FAST                'i'
              166  LOAD_CONST               2
              168  COMPARE_OP               ==
              170  POP_JUMP_IF_FALSE    58  'to 58'

 L. 284       172  LOAD_GLOBAL              ValueError
              174  LOAD_STR                 'Not raised'
              176  CALL_FUNCTION_1       1  ''
              178  RAISE_VARARGS_1       1  ''
              180  JUMP_BACK            58  'to 58'
              182  POP_BLOCK        
              184  JUMP_ABSOLUTE       186  'to 186'
            186_0  COME_FROM_LOOP       48  '48'
              186  POP_BLOCK        
              188  LOAD_CONST               None
            190_0  COME_FROM_WITH       44  '44'
              190  WITH_CLEANUP_START
              192  WITH_CLEANUP_FINISH
              194  END_FINALLY      
              196  POP_BLOCK        
              198  LOAD_CONST               None
            200_0  COME_FROM_ASYNC_WITH    22  '22'
              200  WITH_CLEANUP_START
              202  GET_AWAITABLE    
              204  LOAD_CONST               None
              206  YIELD_FROM       
              208  WITH_CLEANUP_FINISH
              210  END_FINALLY      

Parse error at or near `JUMP_ABSOLUTE' instruction at offset 184

        f3 = asyncio.get_event_loop().create_future()
        f4 = asyncio.get_event_loop().create_future()

        async def watch_2--- This code section failed: ---

 L. 288         0  LOAD_CONST               0
                2  STORE_FAST               'i'

 L. 289         4  LOAD_DEREF               'self'
                6  LOAD_ATTR                client
                8  LOAD_ATTR                watch_scope
               10  LOAD_STR                 '/foo'
               12  LOAD_CONST               True
               14  LOAD_CONST               ('always_reconnect',)
               16  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
               18  BEFORE_ASYNC_WITH
               20  GET_AWAITABLE    
               22  LOAD_CONST               None
               24  YIELD_FROM       
               26  SETUP_ASYNC_WITH    256  'to 256'
               28  STORE_FAST               'response'

 L. 290        30  LOAD_DEREF               'f3'
               32  LOAD_ATTR                set_result
               34  LOAD_CONST               None
               36  CALL_FUNCTION_1       1  ''
               38  POP_TOP          

 L. 291        40  SETUP_LOOP          252  'to 252'
               42  LOAD_FAST                'response'
               44  GET_AITER        
               46  LOAD_CONST               None
               48  YIELD_FROM       
               50  SETUP_EXCEPT         64  'to 64'
               52  GET_ANEXT        
               54  LOAD_CONST               None
               56  YIELD_FROM       
               58  STORE_FAST               'event'
               60  POP_BLOCK        
               62  JUMP_FORWARD         86  'to 86'
             64_0  COME_FROM_EXCEPT     50  '50'
               64  DUP_TOP          
               66  LOAD_GLOBAL              StopAsyncIteration
               68  COMPARE_OP               exception-match
               70  POP_JUMP_IF_FALSE    84  'to 84'
               72  POP_TOP          
               74  POP_TOP          
               76  POP_TOP          
               78  POP_EXCEPT       
               80  POP_BLOCK        
               82  JUMP_ABSOLUTE       252  'to 252'
               84  END_FINALLY      
             86_0  COME_FROM            62  '62'

 L. 292        86  LOAD_FAST                'i'
               88  LOAD_CONST               1
               90  BINARY_ADD       
               92  STORE_FAST               'i'

 L. 293        94  LOAD_FAST                'i'
               96  LOAD_CONST               1
               98  COMPARE_OP               ==
              100  POP_JUMP_IF_FALSE   156  'to 156'

 L. 294       102  LOAD_DEREF               'self'
              104  LOAD_ATTR                assertEqual
              106  LOAD_FAST                'event'
              108  LOAD_ATTR                type
              110  LOAD_GLOBAL              EVENT_TYPE_CREATE
              112  CALL_FUNCTION_2       2  ''
              114  POP_TOP          

 L. 295       116  LOAD_DEREF               'self'
              118  LOAD_ATTR                assertEqual
              120  LOAD_FAST                'event'
              122  LOAD_ATTR                key
              124  LOAD_STR                 '/foo'
              126  CALL_FUNCTION_2       2  ''
              128  POP_TOP          

 L. 296       130  LOAD_DEREF               'self'
              132  LOAD_ATTR                assertEqual
              134  LOAD_FAST                'event'
              136  LOAD_ATTR                value
              138  LOAD_STR                 'foo'
              140  CALL_FUNCTION_2       2  ''
              142  POP_TOP          

 L. 297       144  LOAD_DEREF               'f4'
              146  LOAD_ATTR                set_result
              148  LOAD_CONST               None
              150  CALL_FUNCTION_1       1  ''
              152  POP_TOP          
              154  JUMP_BACK            50  'to 50'
              156  ELSE                     '246'

 L. 298       156  LOAD_FAST                'i'
              158  LOAD_CONST               2
              160  COMPARE_OP               ==
              162  POP_JUMP_IF_FALSE   208  'to 208'

 L. 299       164  LOAD_DEREF               'self'
              166  LOAD_ATTR                assertEqual
              168  LOAD_FAST                'event'
              170  LOAD_ATTR                type
              172  LOAD_GLOBAL              EVENT_TYPE_MODIFY
              174  CALL_FUNCTION_2       2  ''
              176  POP_TOP          

 L. 300       178  LOAD_DEREF               'self'
              180  LOAD_ATTR                assertEqual
              182  LOAD_FAST                'event'
              184  LOAD_ATTR                key
              186  LOAD_STR                 '/foo'
              188  CALL_FUNCTION_2       2  ''
              190  POP_TOP          

 L. 301       192  LOAD_DEREF               'self'
              194  LOAD_ATTR                assertEqual
              196  LOAD_FAST                'event'
              198  LOAD_ATTR                value
              200  LOAD_STR                 'foo1'
              202  CALL_FUNCTION_2       2  ''
              204  POP_TOP          
              206  JUMP_BACK            50  'to 50'
              208  ELSE                     '246'

 L. 302       208  LOAD_FAST                'i'
              210  LOAD_CONST               3
              212  COMPARE_OP               ==
              214  POP_JUMP_IF_FALSE    50  'to 50'

 L. 303       216  LOAD_DEREF               'self'
              218  LOAD_ATTR                assertEqual
              220  LOAD_FAST                'event'
              222  LOAD_ATTR                type
              224  LOAD_GLOBAL              EVENT_TYPE_DELETE
              226  CALL_FUNCTION_2       2  ''
              228  POP_TOP          

 L. 304       230  LOAD_DEREF               'self'
              232  LOAD_ATTR                assertEqual
              234  LOAD_FAST                'event'
              236  LOAD_ATTR                key
              238  LOAD_STR                 '/foo'
              240  CALL_FUNCTION_2       2  ''
              242  POP_TOP          

 L. 307       244  BREAK_LOOP       
            246_0  COME_FROM           214  '214'
              246  JUMP_BACK            50  'to 50'
              248  POP_BLOCK        
              250  JUMP_ABSOLUTE       252  'to 252'
            252_0  COME_FROM_LOOP       40  '40'
              252  POP_BLOCK        
              254  LOAD_CONST               None
            256_0  COME_FROM_ASYNC_WITH    26  '26'
              256  WITH_CLEANUP_START
              258  GET_AWAITABLE    
              260  LOAD_CONST               None
              262  YIELD_FROM       
              264  WITH_CLEANUP_FINISH
              266  END_FINALLY      

Parse error at or near `JUMP_ABSOLUTE' instruction at offset 250

        t1 = asyncio.ensure_future(watch_1())
        t2 = asyncio.ensure_future(watch_2())
        await f1
        await f3
        await self.client.put('/foo', 'foo')
        await f2
        await f4
        fake_endpoints = 'ipv4:///127.0.0.1:49999'
        self.client.update_server_list(fake_endpoints)
        await asyncio.sleep(2)
        self.client.update_server_list(self.endpoints)
        await self.client.put('/foo', 'foo1')
        await self.client.delete('/foo')
        await t1
        await t2

    @asynctest
    async def tearDown(self):
        await self.client.delete(range_all())


if __name__ == '__main__':
    unittest.main()