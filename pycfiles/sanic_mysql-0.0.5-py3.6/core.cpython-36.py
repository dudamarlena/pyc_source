# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\sanic_mysql\core.py
# Compiled at: 2017-07-30 23:17:10
# Size of source mod 2**32: 1511 bytes
from sanic.log import log
from aiomysql import create_pool
import os

class SanicMysql:

    def __init__(self, app, mysql_config=None):
        self.app = app
        self.config = mysql_config
        if app:
            self.init_app(app=app)

    async def start(self, _app, loop):
        _k = dict(loop=loop)
        if self.config:
            config = self.config
        else:
            config = _app.config.get('MYSQL')
        _k.update(config)
        _mysql = await create_pool(**_k)
        log.info('opening mysql connection for [pid:{}]'.format(os.getpid()))

        async def _query--- This code section failed: ---

 L.  27         0  LOAD_DEREF               '_mysql'
                2  LOAD_ATTR                acquire
                4  CALL_FUNCTION_0       0  '0 positional arguments'
                6  BEFORE_ASYNC_WITH
                8  GET_AWAITABLE    
               10  LOAD_CONST               None
               12  YIELD_FROM       
               14  SETUP_ASYNC_WITH    114  'to 114'
               16  STORE_FAST               'conn'

 L.  28        18  LOAD_FAST                'conn'
               20  LOAD_ATTR                cursor
               22  CALL_FUNCTION_0       0  '0 positional arguments'
               24  BEFORE_ASYNC_WITH
               26  GET_AWAITABLE    
               28  LOAD_CONST               None
               30  YIELD_FROM       
               32  SETUP_ASYNC_WITH     98  'to 98'
               34  STORE_FAST               'cur'

 L.  29        36  LOAD_FAST                'cur'
               38  LOAD_ATTR                mogrify
               40  LOAD_FAST                'sqlstr'
               42  LOAD_FAST                'args'
               44  CALL_FUNCTION_2       2  '2 positional arguments'
               46  STORE_FAST               'final_str'

 L.  30        48  LOAD_GLOBAL              log
               50  LOAD_ATTR                info
               52  LOAD_STR                 'mysql query [{}]'
               54  LOAD_ATTR                format
               56  LOAD_FAST                'final_str'
               58  CALL_FUNCTION_1       1  '1 positional argument'
               60  CALL_FUNCTION_1       1  '1 positional argument'
               62  POP_TOP          

 L.  31        64  LOAD_FAST                'cur'
               66  LOAD_ATTR                execute
               68  LOAD_FAST                'final_str'
               70  CALL_FUNCTION_1       1  '1 positional argument'
               72  GET_AWAITABLE    
               74  LOAD_CONST               None
               76  YIELD_FROM       
               78  POP_TOP          

 L.  32        80  LOAD_FAST                'cur'
               82  LOAD_ATTR                fetchall
               84  CALL_FUNCTION_0       0  '0 positional arguments'
               86  GET_AWAITABLE    
               88  LOAD_CONST               None
               90  YIELD_FROM       
               92  STORE_FAST               'value'

 L.  33        94  LOAD_FAST                'value'
               96  RETURN_VALUE     
             98_0  COME_FROM_ASYNC_WITH    32  '32'
               98  WITH_CLEANUP_START
              100  GET_AWAITABLE    
              102  LOAD_CONST               None
              104  YIELD_FROM       
              106  WITH_CLEANUP_FINISH
              108  END_FINALLY      
              110  POP_BLOCK        
              112  LOAD_CONST               None
            114_0  COME_FROM_ASYNC_WITH    14  '14'
              114  WITH_CLEANUP_START
              116  GET_AWAITABLE    
              118  LOAD_CONST               None
              120  YIELD_FROM       
              122  WITH_CLEANUP_FINISH
              124  END_FINALLY      

Parse error at or near `WITH_CLEANUP_FINISH' instruction at offset 122

        setattr(_mysql, 'query', _query)
        _app.mysql = _mysql

    def init_app(self, app):

        @app.listener('before_server_start')
        async def aio_mysql_configure(_app, loop):
            await self.start(_app, loop)

        @app.listener('after_server_stop')
        async def close_mysql(_app, loop):
            _app.mysql.close()
            log.info('closing mysql connection for [pid:{}]'.format(os.getpid()))
            await _app.mysql.wait_closed()