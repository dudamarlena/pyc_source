# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3412)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.9-x86_64/egg/limiter/limiter.py
# Compiled at: 2019-08-16 23:18:53
# Size of source mod 2**32: 3663 bytes
from contextlib import contextmanager, asynccontextmanager, AbstractContextManager, AbstractAsyncContextManager
from typing import Callable, AsyncContextManager, Any, ContextManager, Awaitable
from asyncio import sleep as aiosleep
from inspect import iscoroutinefunction
from dataclasses import dataclass
from functools import wraps
from time import sleep
from random import random
import logging
from token_bucket import Limiter, MemoryStorage
DEFAULT_BUCKET = b'default'
CONSUME_TOKENS = 1
RATE = 2
CAPACITY = 3

def get_limiter(rate: float=RATE, capacity: float=CAPACITY) -> Limiter:
    """
    Returns Limiter object that implements a token-bucket algorithm.
    
    """
    return Limiter(rate, capacity, MemoryStorage())


@dataclass
class limit(AbstractContextManager, AbstractAsyncContextManager):
    __doc__ = '\n    Rate-limiting synchronous/asynchronous context manager.\n    '
    limiter: Limiter
    bucket = DEFAULT_BUCKET
    bucket: bytes
    consume = CONSUME_TOKENS
    consume: float

    def __call__(self, func):
        wrapper = limit_calls(self.limiter, self.bucket, self.consume)
        return wrapper(func)

    def __enter__--- This code section failed: ---

 L.  44         0  LOAD_GLOBAL              limit_rate
                2  LOAD_FAST                'self'
                4  LOAD_ATTR                limiter
                6  LOAD_FAST                'self'
                8  LOAD_ATTR                bucket
               10  LOAD_FAST                'self'
               12  LOAD_ATTR                consume
               14  CALL_FUNCTION_3       3  ''
               16  SETUP_WITH           36  'to 36'
               18  STORE_FAST               'limiter'

 L.  45        20  LOAD_FAST                'limiter'
               22  POP_BLOCK        
               24  ROT_TWO          
               26  BEGIN_FINALLY    
               28  WITH_CLEANUP_START
               30  WITH_CLEANUP_FINISH
               32  POP_FINALLY           0  ''
               34  RETURN_VALUE     
             36_0  COME_FROM_WITH       16  '16'
               36  WITH_CLEANUP_START
               38  WITH_CLEANUP_FINISH
               40  END_FINALLY      

Parse error at or near `ROT_TWO' instruction at offset 24

    def __exit__(self, *args):
        pass

    async def __aenter__--- This code section failed: ---

 L.  51         0  LOAD_GLOBAL              async_limit_rate
                2  LOAD_FAST                'self'
                4  LOAD_ATTR                limiter
                6  LOAD_FAST                'self'
                8  LOAD_ATTR                bucket
               10  LOAD_FAST                'self'
               12  LOAD_ATTR                consume
               14  CALL_FUNCTION_3       3  ''
               16  BEFORE_ASYNC_WITH
               18  GET_AWAITABLE    
               20  LOAD_CONST               None
               22  YIELD_FROM       
               24  SETUP_ASYNC_WITH     50  'to 50'
               26  STORE_FAST               'limiter'

 L.  52        28  LOAD_FAST                'limiter'
               30  POP_BLOCK        
               32  ROT_TWO          
               34  BEGIN_FINALLY    
               36  WITH_CLEANUP_START
               38  GET_AWAITABLE    
               40  LOAD_CONST               None
               42  YIELD_FROM       
               44  WITH_CLEANUP_FINISH
               46  POP_FINALLY           0  ''
               48  RETURN_VALUE     
             50_0  COME_FROM_ASYNC_WITH    24  '24'
               50  WITH_CLEANUP_START
               52  GET_AWAITABLE    
               54  LOAD_CONST               None
               56  YIELD_FROM       
               58  WITH_CLEANUP_FINISH
               60  END_FINALLY      

Parse error at or near `ROT_TWO' instruction at offset 32

    async def __aexit__(self, *args):
        pass


def limit_calls(limiter: Limiter, bucket: bytes=DEFAULT_BUCKET, consume: float=CONSUME_TOKENS) -> Callable[([Callable], Callable)]:
    """
    Rate-limiting decorator for synchronous callables and asynchronous coroutines. 
    
    """

    def wrapper(func):
        if iscoroutinefunction(func):

            @wraps(func)
            async def new_coroutine--- This code section failed: ---

 L.  69         0  LOAD_GLOBAL              async_limit_rate
                2  LOAD_DEREF               'limiter'
                4  LOAD_DEREF               'bucket'
                6  LOAD_DEREF               'consume'
                8  CALL_FUNCTION_3       3  ''
               10  BEFORE_ASYNC_WITH
               12  GET_AWAITABLE    
               14  LOAD_CONST               None
               16  YIELD_FROM       
               18  SETUP_ASYNC_WITH     56  'to 56'
               20  POP_TOP          

 L.  70        22  LOAD_DEREF               'func'
               24  LOAD_FAST                'a'
               26  LOAD_FAST                'kw'
               28  CALL_FUNCTION_EX_KW     1  'keyword and positional arguments'
               30  GET_AWAITABLE    
               32  LOAD_CONST               None
               34  YIELD_FROM       
               36  POP_BLOCK        
               38  ROT_TWO          
               40  BEGIN_FINALLY    
               42  WITH_CLEANUP_START
               44  GET_AWAITABLE    
               46  LOAD_CONST               None
               48  YIELD_FROM       
               50  WITH_CLEANUP_FINISH
               52  POP_FINALLY           0  ''
               54  RETURN_VALUE     
             56_0  COME_FROM_ASYNC_WITH    18  '18'
               56  WITH_CLEANUP_START
               58  GET_AWAITABLE    
               60  LOAD_CONST               None
               62  YIELD_FROM       
               64  WITH_CLEANUP_FINISH
               66  END_FINALLY      

Parse error at or near `ROT_TWO' instruction at offset 38

            return new_coroutine
        if callable(func):

            @wraps(func)
            def new_func--- This code section failed: ---

 L.  76         0  LOAD_GLOBAL              limit_rate
                2  LOAD_DEREF               'limiter'
                4  LOAD_DEREF               'bucket'
                6  LOAD_DEREF               'consume'
                8  CALL_FUNCTION_3       3  ''
               10  SETUP_WITH           36  'to 36'
               12  POP_TOP          

 L.  77        14  LOAD_DEREF               'func'
               16  LOAD_FAST                'a'
               18  LOAD_FAST                'kw'
               20  CALL_FUNCTION_EX_KW     1  'keyword and positional arguments'
               22  POP_BLOCK        
               24  ROT_TWO          
               26  BEGIN_FINALLY    
               28  WITH_CLEANUP_START
               30  WITH_CLEANUP_FINISH
               32  POP_FINALLY           0  ''
               34  RETURN_VALUE     
             36_0  COME_FROM_WITH       10  '10'
               36  WITH_CLEANUP_START
               38  WITH_CLEANUP_FINISH
               40  END_FINALLY      

Parse error at or near `ROT_TWO' instruction at offset 24

            return new_func
        raise ValueError('Can only decorate callables and coroutines.')

    return wrapper


@asynccontextmanager
async def async_limit_rate(limiter: Limiter, bucket: bytes=DEFAULT_BUCKET, consume: float=CONSUME_TOKENS) -> AsyncContextManager[Limiter]:
    """
    Rate-limiting asynchronous context manager.
    
    """
    while not limiter.consume(bucket, consume):
        tokens = limiter._storage.get_token_count(bucket)
        sleep_for = (consume - tokens) / limiter._rate
        sleep_for = random() * sleep_for
        if sleep_for < 0:
            break
        logging.debug(f"Rate limit reached. Sleeping for {sleep_for}s.")
        await aiosleep(sleep_for)

    (yield limiter)


@contextmanager
def limit_rate(limiter: Limiter, bucket: bytes=DEFAULT_BUCKET, consume: float=CONSUME_TOKENS) -> ContextManager[Limiter]:
    """
    Thread-safe rate-limiting context manager.
    
    """
    while not limiter.consume(bucket, consume):
        tokens = limiter._storage.get_token_count(bucket)
        sleep_for = (consume - tokens) / limiter._rate
        sleep_for = random() * sleep_for
        if sleep_for < 0:
            break
        logging.debug(f"Rate limit reached. Sleeping for {sleep_for}s.")
        sleep(sleep_for)

    (yield limiter)