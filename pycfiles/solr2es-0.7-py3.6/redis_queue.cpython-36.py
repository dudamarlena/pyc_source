# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/solr2es/redis_queue.py
# Compiled at: 2018-11-22 02:36:26
# Size of source mod 2**32: 655 bytes
from json import dumps

class RedisQueue(object):

    def __init__(self, redis) -> None:
        self.redis = redis

    def push_loop(self, producer):
        for results in producer():
            self.push(map(dumps, results))

    def push(self, value_list):
        (self.redis.lpush)(*('solr2es:queue', ), *value_list)


class RedisQueueAsync(object):

    def __init__(self, redis) -> None:
        self.redis = redis

    async def push_loop--- This code section failed: ---

 L.  21         0  SETUP_LOOP           76  'to 76'
                2  LOAD_FAST                'producer'
                4  CALL_FUNCTION_0       0  '0 positional arguments'
                6  GET_AITER        
                8  LOAD_CONST               None
               10  YIELD_FROM       
               12  SETUP_EXCEPT         26  'to 26'
               14  GET_ANEXT        
               16  LOAD_CONST               None
               18  YIELD_FROM       
               20  STORE_FAST               'results'
               22  POP_BLOCK        
               24  JUMP_FORWARD         36  'to 36'
             26_0  COME_FROM_EXCEPT     12  '12'
               26  DUP_TOP          
               28  LOAD_GLOBAL              StopAsyncIteration
               30  COMPARE_OP               exception-match
               32  POP_JUMP_IF_TRUE     64  'to 64'
               34  END_FINALLY      
             36_0  COME_FROM            24  '24'

 L.  22        36  LOAD_FAST                'self'
               38  LOAD_ATTR                push
               40  LOAD_GLOBAL              list
               42  LOAD_GLOBAL              map
               44  LOAD_GLOBAL              dumps
               46  LOAD_FAST                'results'
               48  CALL_FUNCTION_2       2  '2 positional arguments'
               50  CALL_FUNCTION_1       1  '1 positional argument'
               52  CALL_FUNCTION_1       1  '1 positional argument'
               54  GET_AWAITABLE    
               56  LOAD_CONST               None
               58  YIELD_FROM       
               60  POP_TOP          
               62  JUMP_BACK            12  'to 12'
             64_0  COME_FROM            32  '32'
               64  POP_TOP          
               66  POP_TOP          
               68  POP_TOP          
               70  POP_EXCEPT       
               72  POP_TOP          
               74  POP_BLOCK        
             76_0  COME_FROM_LOOP        0  '0'

Parse error at or near `None' instruction at offset -1

    async def push(self, value_list):
        await self.redis.lpush('solr2es:queue', value_list)