# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\AsyncSpider\core\spider.py
# Compiled at: 2018-03-10 13:44:21
# Size of source mod 2**32: 2732 bytes
from .base import AioThreadExecutor, ControllerShortcutMixin
from .item import Item
from .fetsav import Fetcher, Saver
from .reqrep import Response
from asyncio import Queue as AsyncQueue
from asyncio import wrap_future
from collections import AsyncGenerator
__all__ = ['Spider']

class Spider(AioThreadExecutor, ControllerShortcutMixin):

    def __init__(self, controller):
        ControllerShortcutMixin.__init__(self, controller)
        AioThreadExecutor.__init__(self)
        self.concurrency = self.settings['concurrency']
        assert self.concurrency >= 1
        self.stop_when_empty = self.settings.get('stop_when_empty', True)
        self._action_queue = AsyncQueue(loop=(self._loop))
        self._working_num = 0
        self.call_on_start(self._action_queue.put_nowait, self.start_action())
        for _ in range(self.concurrency):
            self.call_on_start(self.run_coro, self._worker())

    @property
    def fetcher(self) -> Fetcher:
        return self._controller.fetcher

    @property
    def saver(self) -> Saver:
        return self._controller.saver

    async def add_action(self, action):
        assert isinstance(action, AsyncGenerator)
        await self._action_queue.put(action)

    async def fetch(self, method, url, **kwargs) -> Response:
        fut = self.fetcher.run_coro_threadsafe((self.fetcher.fetch)(method, url, **kwargs))
        fut = wrap_future(fut, loop=(self._loop))
        return await fut

    async def save(self, item, wait=False):
        fut = self.saver.run_coro_threadsafe(self.saver.save(item))
        if wait:
            fut = wrap_future(fut, loop=(self._loop))
            await fut

    async def _worker(self):
        while True:
            act = await self._action_queue.get()
            self._working_num += 1
            try:
                try:
                    await self._drive(act)
                except Exception:
                    self.logger.exception('Action {} failed.'.format(act))

            finally:
                self._working_num -= 1
                self._action_queue.task_done()
                if self.stop_when_empty:
                    if self._working_num == 0:
                        if self._action_queue.empty():
                            self._loop.stop()

    async def _drive--- This code section failed: ---

 L.  68         0  SETUP_LOOP          142  'to 142'
                2  LOAD_FAST                'action'
                4  GET_AITER        
                6  LOAD_CONST               None
                8  YIELD_FROM       
               10  SETUP_EXCEPT         24  'to 24'
               12  GET_ANEXT        
               14  LOAD_CONST               None
               16  YIELD_FROM       
               18  STORE_FAST               'obj'
               20  POP_BLOCK        
               22  JUMP_FORWARD         46  'to 46'
             24_0  COME_FROM_EXCEPT     10  '10'
               24  DUP_TOP          
               26  LOAD_GLOBAL              StopAsyncIteration
               28  COMPARE_OP               exception-match
               30  POP_JUMP_IF_FALSE    44  'to 44'
               32  POP_TOP          
               34  POP_TOP          
               36  POP_TOP          
               38  POP_EXCEPT       
               40  POP_BLOCK        
               42  JUMP_ABSOLUTE       142  'to 142'
               44  END_FINALLY      
             46_0  COME_FROM            22  '22'

 L.  69        46  LOAD_FAST                'obj'
               48  LOAD_CONST               None
               50  COMPARE_OP               is
               52  POP_JUMP_IF_FALSE    56  'to 56'

 L.  70        54  CONTINUE             10  'to 10'
               56  ELSE                     '136'

 L.  71        56  LOAD_GLOBAL              isinstance
               58  LOAD_FAST                'obj'
               60  LOAD_GLOBAL              AsyncGenerator
               62  CALL_FUNCTION_2       2  '2 positional arguments'
               64  POP_JUMP_IF_FALSE    84  'to 84'

 L.  72        66  LOAD_FAST                'self'
               68  LOAD_ATTR                add_action
               70  LOAD_FAST                'obj'
               72  CALL_FUNCTION_1       1  '1 positional argument'
               74  GET_AWAITABLE    
               76  LOAD_CONST               None
               78  YIELD_FROM       
               80  POP_TOP          
               82  JUMP_BACK            10  'to 10'
               84  ELSE                     '136'

 L.  73        84  LOAD_GLOBAL              isinstance
               86  LOAD_FAST                'obj'
               88  LOAD_GLOBAL              Item
               90  CALL_FUNCTION_2       2  '2 positional arguments'
               92  POP_JUMP_IF_FALSE   116  'to 116'

 L.  74        94  LOAD_FAST                'self'
               96  LOAD_ATTR                save
               98  LOAD_FAST                'obj'
              100  LOAD_CONST               False
              102  LOAD_CONST               ('wait',)
              104  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              106  GET_AWAITABLE    
              108  LOAD_CONST               None
              110  YIELD_FROM       
              112  POP_TOP          
              114  JUMP_BACK            10  'to 10'
              116  ELSE                     '136'

 L.  76       116  LOAD_FAST                'self'
              118  LOAD_ATTR                logger
              120  LOAD_ATTR                warning
              122  LOAD_STR                 '{} yield an unexpected object: {}'
              124  LOAD_ATTR                format
              126  LOAD_FAST                'action'
              128  LOAD_FAST                'obj'
              130  CALL_FUNCTION_2       2  '2 positional arguments'
              132  CALL_FUNCTION_1       1  '1 positional argument'
              134  POP_TOP          
              136  JUMP_BACK            10  'to 10'
              138  POP_BLOCK        
              140  JUMP_ABSOLUTE       142  'to 142'
            142_0  COME_FROM_LOOP        0  '0'

Parse error at or near `JUMP_ABSOLUTE' instruction at offset 140

    async def start_action(self):
        yield