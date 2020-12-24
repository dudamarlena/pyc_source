# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\AsyncSpider\core\fetsav.py
# Compiled at: 2018-03-10 15:03:57
# Size of source mod 2**32: 2461 bytes
from .base import AioThreadExecutor, SuperProcessorMixin, ControllerShortcutMixin
from .reqrep import Request, Response
import asyncio, aiohttp
__all__ = [
 'Fetcher', 'Saver']

def active_all(sp):
    for p in sp.processors:
        sp.call_on_start(p.on_start)
        sp.call_on_stop(p.on_stop)


class Fetcher(AioThreadExecutor, SuperProcessorMixin, ControllerShortcutMixin):

    def add_processor(self, request_processor):
        assert self.is_initial
        SuperProcessorMixin.add_processor(self, request_processor)

    def remove_processor(self, request_processor):
        assert self.is_initial
        SuperProcessorMixin.remove_processor(self, request_processor)

    def __init__(self, controller):
        ControllerShortcutMixin.__init__(self, controller)
        SuperProcessorMixin.__init__(self)
        AioThreadExecutor.__init__(self)
        self._session = None

        def set_session():
            self._session = aiohttp.ClientSession(loop=(self._loop))

        def close_session():
            self._loop.run_until_complete(self._session.close())

        self.call_on_start(set_session)
        self.call_on_stop(close_session)
        self.call_on_start(active_all, self)

    async def fetch--- This code section failed: ---

 L.  41         0  LOAD_GLOBAL              Request
                2  LOAD_FAST                'method'
                4  LOAD_FAST                'url'
                6  BUILD_TUPLE_2         2 
                8  LOAD_FAST                'kwargs'
               10  CALL_FUNCTION_EX_KW     1  'keyword and positional arguments'
               12  STORE_FAST               'req'

 L.  42        14  SETUP_LOOP           46  'to 46'
               16  LOAD_FAST                'self'
               18  LOAD_ATTR                _processors
               20  GET_ITER         
               22  FOR_ITER             44  'to 44'
               24  STORE_FAST               'p'

 L.  43        26  LOAD_FAST                'p'
               28  LOAD_ATTR                process
               30  LOAD_FAST                'req'
               32  CALL_FUNCTION_1       1  '1 positional argument'
               34  GET_AWAITABLE    
               36  LOAD_CONST               None
               38  YIELD_FROM       
               40  POP_TOP          
               42  JUMP_BACK            22  'to 22'
               44  POP_BLOCK        
             46_0  COME_FROM_LOOP       14  '14'

 L.  44        46  LOAD_FAST                'self'
               48  LOAD_ATTR                _session
               50  LOAD_ATTR                request
               52  LOAD_FAST                'method'
               54  LOAD_FAST                'url'
               56  BUILD_TUPLE_2         2 
               58  LOAD_FAST                'kwargs'
               60  CALL_FUNCTION_EX_KW     1  'keyword and positional arguments'
               62  BEFORE_ASYNC_WITH
               64  GET_AWAITABLE    
               66  LOAD_CONST               None
               68  YIELD_FROM       
               70  SETUP_ASYNC_WITH     90  'to 90'
               72  STORE_FAST               'resp'

 L.  45        74  LOAD_GLOBAL              Response
               76  LOAD_ATTR                from_client_response
               78  LOAD_FAST                'resp'
               80  CALL_FUNCTION_1       1  '1 positional argument'
               82  GET_AWAITABLE    
               84  LOAD_CONST               None
               86  YIELD_FROM       
               88  RETURN_VALUE     
             90_0  COME_FROM_ASYNC_WITH    70  '70'
               90  WITH_CLEANUP_START
               92  GET_AWAITABLE    
               94  LOAD_CONST               None
               96  YIELD_FROM       
               98  WITH_CLEANUP_FINISH
              100  END_FINALLY      

Parse error at or near `COME_FROM_ASYNC_WITH' instruction at offset 90_0


class Saver(AioThreadExecutor, SuperProcessorMixin, ControllerShortcutMixin):

    def add_processor(self, item_processor):
        assert self.is_initial
        SuperProcessorMixin.add_processor(self, item_processor)

    def remove_processor(self, item_processor):
        assert self.is_initial
        SuperProcessorMixin.remove_processor(self, item_processor)

    def _clean_loop(self):
        tasks = asyncio.Task.all_tasks(loop=(self._loop))
        if tasks:
            self._loop.run_until_complete(asyncio.wait(tasks))

    def __init__(self, controller):
        ControllerShortcutMixin.__init__(self, controller)
        SuperProcessorMixin.__init__(self)
        AioThreadExecutor.__init__(self)
        self.call_on_start(active_all, self)

    async def save(self, item):
        for p in self._processors:
            await p.process(item)