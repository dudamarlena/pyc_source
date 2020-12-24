# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/mercury/rpc/jobs/monitor.py
# Compiled at: 2018-01-08 12:01:55
# Size of source mod 2**32: 2402 bytes
import asyncio, datetime, logging, time
from mercury.rpc.jobs.tasks import COMPLETED_STATUSES, complete_task
log = logging.getLogger(__name__)

class Monitor(object):
    __doc__ = '\n    Monitors the tasks collection for expired tasks. Timeout values should accompany tasks. If\n    a task does not contain a timeout, default_timeout will be used\n    '

    def __init__(self, jobs_collection, tasks_collection, loop, default_timeout=120, cycle_time=10):
        self.jobs_collection = jobs_collection
        self.tasks_collection = tasks_collection
        self.asyncio_loop = loop
        self.default_timeout = default_timeout
        self.cycle_time = cycle_time
        self.last_run = 0
        self._kill = False

    async def process--- This code section failed: ---

 L.  29         0  LOAD_GLOBAL              log
                2  LOAD_METHOD              debug
                4  LOAD_STR                 'Processing'
                6  CALL_METHOD_1         1  '1 positional argument'
                8  POP_TOP          

 L.  30        10  LOAD_GLOBAL              time
               12  LOAD_METHOD              time
               14  CALL_METHOD_0         0  '0 positional arguments'
               16  STORE_FAST               'now'

 L.  31        18  LOAD_FAST                'self'
               20  LOAD_ATTR                tasks_collection
               22  LOAD_METHOD              find
               24  LOAD_STR                 '$nin'
               26  LOAD_GLOBAL              COMPLETED_STATUSES
               28  BUILD_MAP_1           1 

 L.  32        30  LOAD_STR                 '$gt'
               32  LOAD_CONST               0
               34  BUILD_MAP_1           1 
               36  LOAD_CONST               ('status', 'timeout')
               38  BUILD_CONST_KEY_MAP_2     2 
               40  CALL_METHOD_1         1  '1 positional argument'
               42  STORE_FAST               'c'

 L.  34        44  LOAD_GLOBAL              log
               46  LOAD_METHOD              debug
               48  LOAD_STR                 'Matched {} active tasks'
               50  LOAD_METHOD              format
               52  LOAD_FAST                'c'
               54  LOAD_METHOD              count
               56  CALL_METHOD_0         0  '0 positional arguments'
               58  GET_AWAITABLE    
               60  LOAD_CONST               None
               62  YIELD_FROM       
               64  CALL_METHOD_1         1  '1 positional argument'
               66  CALL_METHOD_1         1  '1 positional argument'
               68  POP_TOP          

 L.  35        70  SETUP_LOOP          220  'to 220'
               72  LOAD_FAST                'c'
               74  GET_AITER        
             76_0  COME_FROM           118  '118'
               76  SETUP_EXCEPT         90  'to 90'
               78  GET_ANEXT        
               80  LOAD_CONST               None
               82  YIELD_FROM       
               84  STORE_FAST               'task'
               86  POP_BLOCK        
               88  JUMP_FORWARD        100  'to 100'
             90_0  COME_FROM_EXCEPT     76  '76'
               90  DUP_TOP          
               92  LOAD_GLOBAL              StopAsyncIteration
               94  COMPARE_OP               exception-match
               96  POP_JUMP_IF_TRUE    208  'to 208'
               98  END_FINALLY      
            100_0  COME_FROM            88  '88'

 L.  36       100  LOAD_FAST                'task'
              102  LOAD_STR                 'time_updated'
              104  BINARY_SUBSCR    
              106  LOAD_FAST                'now'
              108  LOAD_FAST                'task'
              110  LOAD_STR                 'timeout'
              112  BINARY_SUBSCR    
              114  BINARY_SUBTRACT  
              116  COMPARE_OP               <
              118  POP_JUMP_IF_FALSE    76  'to 76'

 L.  37       120  LOAD_GLOBAL              log
              122  LOAD_METHOD              error
              124  LOAD_STR                 'Timeout Error: Job: {job_id}, Task: {task_id}, Timeout: {timeout}'
              126  LOAD_ATTR                format
              128  BUILD_TUPLE_0         0 
              130  LOAD_FAST                'task'
              132  CALL_FUNCTION_EX_KW     1  'keyword and positional arguments'
              134  CALL_METHOD_1         1  '1 positional argument'
              136  POP_TOP          

 L.  39       138  LOAD_STR                 'TIMEOUT'

 L.  40       140  LOAD_FAST                'task'
              142  LOAD_STR                 'time_started'
              144  BINARY_SUBSCR    
              146  JUMP_IF_TRUE_OR_POP   150  'to 150'
              148  LOAD_CONST               0
            150_0  COME_FROM           146  '146'

 L.  41       150  LOAD_FAST                'now'

 L.  42       152  LOAD_FAST                'now'

 L.  43       154  LOAD_GLOBAL              datetime
              156  LOAD_ATTR                datetime
              158  LOAD_METHOD              utcfromtimestamp
              160  LOAD_FAST                'now'
              162  CALL_METHOD_1         1  '1 positional argument'

 L.  44       164  LOAD_CONST               None

 L.  45       166  LOAD_CONST               None

 L.  46       168  LOAD_STR                 'Task Timeout'
              170  LOAD_CONST               ('status', 'time_started', 'time_updated', 'time_completed', 'ttl_time_completed', 'message', 'traceback', 'action')
              172  BUILD_CONST_KEY_MAP_8     8 
              174  STORE_FAST               'update_data'

 L.  48       176  LOAD_GLOBAL              complete_task
              178  LOAD_FAST                'task'
              180  LOAD_STR                 'job_id'
              182  BINARY_SUBSCR    

 L.  49       184  LOAD_FAST                'task'
              186  LOAD_STR                 'task_id'
              188  BINARY_SUBSCR    

 L.  50       190  LOAD_FAST                'update_data'

 L.  51       192  LOAD_FAST                'self'
              194  LOAD_ATTR                jobs_collection

 L.  52       196  LOAD_FAST                'self'
              198  LOAD_ATTR                tasks_collection
              200  LOAD_CONST               ('jobs_collection', 'tasks_collection')
              202  CALL_FUNCTION_KW_5     5  '5 total positional and keyword args'
              204  POP_TOP          
              206  JUMP_BACK            76  'to 76'
            208_0  COME_FROM            96  '96'
              208  POP_TOP          
              210  POP_TOP          
              212  POP_TOP          
              214  POP_EXCEPT       
              216  POP_TOP          
              218  POP_BLOCK        
            220_0  COME_FROM_LOOP       70  '70'

Parse error at or near `COME_FROM' instruction at offset 76_0

    def kill(self):
        self._kill = True

    async def loop(self):
        while True:
            if self._kill:
                log.info('Kill signal received, shutting down')
                break
            if not self.asyncio_loop.is_running:
                print('loop is not running')
                break
            await self.process
            await asyncio.sleep(self.cycle_time)