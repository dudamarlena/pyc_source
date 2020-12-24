# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /opt/work/lib/pyenv/versions/3.6.1/envs/maestro/lib/python3.6/site-packages/rest_framework/lib/orm/database.py
# Compiled at: 2018-10-12 04:41:52
# Size of source mod 2**32: 11018 bytes
import asyncio
from .peewee import Database, ExceptionWrapper
from .peewee import sort_models_topologically, merge_dict
from .peewee import OperationalError
from .peewee import RESULTS_NAIVE, RESULTS_TUPLES, RESULTS_DICTS, RESULTS_AGGREGATE_MODELS, RESULTS_MODELS
from .peewee import SQL, R, Clause, fn, binary_construct
from .peewee import logger
from .context import Atomic, Transaction, SavePoint
from rest_framework.lib.orm.result import AsyncModelQueryResultWrapper
from rest_framework.lib.orm.result import AsyncTuplesQueryResultWrapper
from rest_framework.lib.orm.result import AsyncDictQueryResultWrapper
from rest_framework.lib.orm.result import AsyncNaiveQueryResultWrapper
from rest_framework.lib.orm.result import AsyncAggregateQueryResultWrapper

class AsyncConnection:

    def __init__(self, db, exception_wrapper, autocommit=None, autorollback=None):
        self.autocommit = autocommit
        self.autorollback = autorollback
        self.db = db
        self.acquirer = None
        self.conn = None
        self.context_stack = []
        self.transactions = []
        self.exception_wrapper = exception_wrapper

    def transaction_depth(self):
        return len(self.transactions)

    def push_transaction(self, transaction):
        self.transactions.append(transaction)

    def pop_transaction(self):
        return self.transactions.pop()

    async def execute_sql(self, sql, params=None, require_commit=True):
        logger.debug((sql, params))
        with self.exception_wrapper:
            cursor = await self.conn.cursor()
            try:
                await cursor.execute(sql, params or ())
            except Exception:
                if self.autorollback:
                    if self.autocommit:
                        await self.rollback()
                raise
            else:
                if require_commit:
                    if self.autocommit:
                        await self.commit()
                return cursor

    async def __aenter__(self):
        if self.acquirer is None:
            await self.db.connect()
            self.acquirer = self.db.pool.acquire()
        self.conn = await self.acquirer.__aenter__()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.acquirer.__aexit__(exc_type, exc_val, exc_tb)

    async def begin(self):
        pass

    def commit(self):
        with self.exception_wrapper:
            return self.conn.commit()

    def rollback(self):
        with self.exception_wrapper:
            return self.conn.rollback()

    def transaction(self, transaction_type=None):
        return Transaction(self, transaction_type)

    commit_on_success = property(transaction)

    def savepoint(self, sid=None):
        if not self.savepoints:
            raise NotImplementedError
        return SavePoint(self, sid)


class AsyncDatabase(Database):

    def _connect(self, database, **kwargs):
        raise NotImplementedError

    def begin(self):
        raise NotImplementedError

    def commit(self):
        raise NotImplementedError

    def rollback(self):
        raise NotImplementedError

    def get_cursor(self):
        raise NotImplementedError

    def get_tables(self, schema=None):
        raise NotImplementedError

    def get_indexes(self, table, schema=None):
        raise NotImplementedError

    def get_columns(self, table, schema=None):
        raise NotImplementedError

    def get_primary_keys(self, table, schema=None):
        raise NotImplementedError

    def get_foreign_keys(self, table, schema=None):
        raise NotImplementedError

    def sequence_exists(self, seq):
        raise NotImplementedError

    def transaction_depth(self):
        raise NotImplementedError

    def __init__(self, database, autocommit=True, fields=None, ops=None, autorollback=False, loop=None, **connect_kwargs):
        self.connect_kwargs = {}
        self.closed = True
        (self.init)(database, **connect_kwargs)
        self.pool = None
        self.autocommit = autocommit
        self.autorollback = autorollback
        self.use_speedups = False
        self.field_overrides = merge_dict(self.field_overrides, fields or {})
        self.op_overrides = merge_dict(self.op_overrides, ops or {})
        self.exception_wrapper = ExceptionWrapper(self.exceptions)
        self._loop = loop
        self._auto_task = None

    @property
    def loop(self):
        if self._loop is None:
            self._loop = asyncio.get_event_loop()
        return self._loop

    def is_closed(self):
        return self.closed

    def get_conn(self):
        return AsyncConnection(db=self,
          autocommit=(self.autocommit),
          autorollback=(self.autorollback),
          exception_wrapper=(self.exception_wrapper))

    async def close(self):
        if self.deferred:
            raise Exception('Error, database not properly initialized before closing connection')
        with self.exception_wrapper:
            if not self.closed:
                if self.pool:
                    await self.close_engine()
                    self.pool.close()
                    self.closed = True
                    await self.pool.wait_closed()

    async def connect(self, safe=True):
        if self.deferred:
            raise OperationalError('Database has not been initialized')
        if not self.closed:
            if safe:
                return
            raise OperationalError('Connection already open')
        with self.exception_wrapper:
            self.pool = await (self._connect)((self.database), **self.connect_kwargs)
            self.closed = False
            await self.init_engine()

    async def init_engine(self):
        self._auto_task = self.loop.create_task(self.keep_engine())

    async def close_engine(self):
        self._auto_task.cancel()

    async def keep_engine(self):
        while True:
            async with self.pool.acquire() as conn:
                await conn.ping()
            await asyncio.sleep(60)

    def get_result_wrapper(self, wrapper_type):
        if wrapper_type == RESULTS_NAIVE:
            return AsyncNaiveQueryResultWrapper
        else:
            if wrapper_type == RESULTS_MODELS:
                return AsyncModelQueryResultWrapper
            else:
                if wrapper_type == RESULTS_TUPLES:
                    return AsyncTuplesQueryResultWrapper
                if wrapper_type == RESULTS_DICTS:
                    return AsyncDictQueryResultWrapper
                if wrapper_type == RESULTS_AGGREGATE_MODELS:
                    return AsyncAggregateQueryResultWrapper
            return AsyncNaiveQueryResultWrapper

    def atomic(self, transaction_type=None):
        return Atomic(self.get_conn(), transaction_type)

    def transaction(self, transaction_type=None):
        return Transaction(self.get_conn(), transaction_type)

    commit_on_success = property(transaction)

    async def create_table--- This code section failed: ---

 L. 225         0  LOAD_FAST                'self'
                2  LOAD_ATTR                compiler
                4  CALL_FUNCTION_0       0  '0 positional arguments'
                6  STORE_FAST               'qc'

 L. 226         8  LOAD_FAST                'self'
               10  LOAD_ATTR                get_conn
               12  CALL_FUNCTION_0       0  '0 positional arguments'
               14  BEFORE_ASYNC_WITH
               16  GET_AWAITABLE    
               18  LOAD_CONST               None
               20  YIELD_FROM       
               22  SETUP_ASYNC_WITH     54  'to 54'
               24  STORE_FAST               'conn'

 L. 227        26  LOAD_FAST                'qc'
               28  LOAD_ATTR                create_table
               30  LOAD_FAST                'model_class'
               32  LOAD_FAST                'safe'
               34  CALL_FUNCTION_2       2  '2 positional arguments'
               36  STORE_FAST               'args'

 L. 228        38  LOAD_FAST                'conn'
               40  LOAD_ATTR                execute_sql
               42  LOAD_FAST                'args'
               44  CALL_FUNCTION_EX      0  'positional arguments only'
               46  GET_AWAITABLE    
               48  LOAD_CONST               None
               50  YIELD_FROM       
               52  RETURN_VALUE     
             54_0  COME_FROM_ASYNC_WITH    22  '22'
               54  WITH_CLEANUP_START
               56  GET_AWAITABLE    
               58  LOAD_CONST               None
               60  YIELD_FROM       
               62  WITH_CLEANUP_FINISH
               64  END_FINALLY      

Parse error at or near `COME_FROM_ASYNC_WITH' instruction at offset 54_0

    async def create_tables(self, models, safe=False):
        await create_model_tables(models, fail_silently=safe)

    async def create_index--- This code section failed: ---

 L. 234         0  LOAD_FAST                'self'
                2  LOAD_ATTR                compiler
                4  CALL_FUNCTION_0       0  '0 positional arguments'
                6  STORE_FAST               'qc'

 L. 235         8  LOAD_GLOBAL              isinstance
               10  LOAD_FAST                'fields'
               12  LOAD_GLOBAL              list
               14  LOAD_GLOBAL              tuple
               16  BUILD_TUPLE_2         2 
               18  CALL_FUNCTION_2       2  '2 positional arguments'
               20  POP_JUMP_IF_TRUE     34  'to 34'

 L. 236        22  LOAD_GLOBAL              ValueError
               24  LOAD_STR                 'Fields passed to "create_index" must be a list or tuple: "%s"'
               26  LOAD_FAST                'fields'
               28  BINARY_MODULO    
               30  CALL_FUNCTION_1       1  '1 positional argument'
               32  RAISE_VARARGS_1       1  'exception'
             34_0  COME_FROM            20  '20'

 L. 238        34  LOAD_CLOSURE             'model_class'
               36  BUILD_TUPLE_1         1 
               38  LOAD_LISTCOMP            '<code_object <listcomp>>'
               40  LOAD_STR                 'AsyncDatabase.create_index.<locals>.<listcomp>'
               42  MAKE_FUNCTION_8          'closure'
               44  LOAD_FAST                'fields'
               46  GET_ITER         
               48  CALL_FUNCTION_1       1  '1 positional argument'
               50  STORE_FAST               'fobjs'

 L. 239        52  LOAD_FAST                'self'
               54  LOAD_ATTR                get_conn
               56  CALL_FUNCTION_0       0  '0 positional arguments'
               58  BEFORE_ASYNC_WITH
               60  GET_AWAITABLE    
               62  LOAD_CONST               None
               64  YIELD_FROM       
               66  SETUP_ASYNC_WITH    100  'to 100'
               68  STORE_FAST               'conn'

 L. 240        70  LOAD_FAST                'qc'
               72  LOAD_ATTR                create_index
               74  LOAD_DEREF               'model_class'
               76  LOAD_FAST                'fobjs'
               78  LOAD_FAST                'unique'
               80  CALL_FUNCTION_3       3  '3 positional arguments'
               82  STORE_FAST               'args'

 L. 241        84  LOAD_FAST                'conn'
               86  LOAD_ATTR                execute_sql
               88  LOAD_FAST                'args'
               90  CALL_FUNCTION_EX      0  'positional arguments only'
               92  GET_AWAITABLE    
               94  LOAD_CONST               None
               96  YIELD_FROM       
               98  RETURN_VALUE     
            100_0  COME_FROM_ASYNC_WITH    66  '66'
              100  WITH_CLEANUP_START
              102  GET_AWAITABLE    
              104  LOAD_CONST               None
              106  YIELD_FROM       
              108  WITH_CLEANUP_FINISH
              110  END_FINALLY      

Parse error at or near `COME_FROM_ASYNC_WITH' instruction at offset 100_0

    async def drop_index--- This code section failed: ---

 L. 244         0  LOAD_FAST                'self'
                2  LOAD_ATTR                compiler
                4  CALL_FUNCTION_0       0  '0 positional arguments'
                6  STORE_FAST               'qc'

 L. 245         8  LOAD_GLOBAL              isinstance
               10  LOAD_FAST                'fields'
               12  LOAD_GLOBAL              list
               14  LOAD_GLOBAL              tuple
               16  BUILD_TUPLE_2         2 
               18  CALL_FUNCTION_2       2  '2 positional arguments'
               20  POP_JUMP_IF_TRUE     34  'to 34'

 L. 246        22  LOAD_GLOBAL              ValueError
               24  LOAD_STR                 'Fields passed to "drop_index" must be a list or tuple: "%s"'
               26  LOAD_FAST                'fields'
               28  BINARY_MODULO    
               30  CALL_FUNCTION_1       1  '1 positional argument'
               32  RAISE_VARARGS_1       1  'exception'
             34_0  COME_FROM            20  '20'

 L. 248        34  LOAD_CLOSURE             'model_class'
               36  BUILD_TUPLE_1         1 
               38  LOAD_LISTCOMP            '<code_object <listcomp>>'
               40  LOAD_STR                 'AsyncDatabase.drop_index.<locals>.<listcomp>'
               42  MAKE_FUNCTION_8          'closure'
               44  LOAD_FAST                'fields'
               46  GET_ITER         
               48  CALL_FUNCTION_1       1  '1 positional argument'
               50  STORE_FAST               'fobjs'

 L. 249        52  LOAD_FAST                'self'
               54  LOAD_ATTR                get_conn
               56  CALL_FUNCTION_0       0  '0 positional arguments'
               58  BEFORE_ASYNC_WITH
               60  GET_AWAITABLE    
               62  LOAD_CONST               None
               64  YIELD_FROM       
               66  SETUP_ASYNC_WITH    100  'to 100'
               68  STORE_FAST               'conn'

 L. 250        70  LOAD_FAST                'qc'
               72  LOAD_ATTR                drop_index
               74  LOAD_DEREF               'model_class'
               76  LOAD_FAST                'fobjs'
               78  LOAD_FAST                'safe'
               80  CALL_FUNCTION_3       3  '3 positional arguments'
               82  STORE_FAST               'args'

 L. 251        84  LOAD_FAST                'conn'
               86  LOAD_ATTR                execute_sql
               88  LOAD_FAST                'args'
               90  CALL_FUNCTION_EX      0  'positional arguments only'
               92  GET_AWAITABLE    
               94  LOAD_CONST               None
               96  YIELD_FROM       
               98  RETURN_VALUE     
            100_0  COME_FROM_ASYNC_WITH    66  '66'
              100  WITH_CLEANUP_START
              102  GET_AWAITABLE    
              104  LOAD_CONST               None
              106  YIELD_FROM       
              108  WITH_CLEANUP_FINISH
              110  END_FINALLY      

Parse error at or near `COME_FROM_ASYNC_WITH' instruction at offset 100_0

    async def create_foreign_key--- This code section failed: ---

 L. 254         0  LOAD_FAST                'self'
                2  LOAD_ATTR                compiler
                4  CALL_FUNCTION_0       0  '0 positional arguments'
                6  STORE_FAST               'qc'

 L. 255         8  LOAD_FAST                'self'
               10  LOAD_ATTR                get_conn
               12  CALL_FUNCTION_0       0  '0 positional arguments'
               14  BEFORE_ASYNC_WITH
               16  GET_AWAITABLE    
               18  LOAD_CONST               None
               20  YIELD_FROM       
               22  SETUP_ASYNC_WITH     56  'to 56'
               24  STORE_FAST               'conn'

 L. 256        26  LOAD_FAST                'qc'
               28  LOAD_ATTR                create_foreign_key
               30  LOAD_FAST                'model_class'
               32  LOAD_FAST                'field'
               34  LOAD_FAST                'constraint'
               36  CALL_FUNCTION_3       3  '3 positional arguments'
               38  STORE_FAST               'args'

 L. 257        40  LOAD_FAST                'conn'
               42  LOAD_ATTR                execute_sql
               44  LOAD_FAST                'args'
               46  CALL_FUNCTION_EX      0  'positional arguments only'
               48  GET_AWAITABLE    
               50  LOAD_CONST               None
               52  YIELD_FROM       
               54  RETURN_VALUE     
             56_0  COME_FROM_ASYNC_WITH    22  '22'
               56  WITH_CLEANUP_START
               58  GET_AWAITABLE    
               60  LOAD_CONST               None
               62  YIELD_FROM       
               64  WITH_CLEANUP_FINISH
               66  END_FINALLY      

Parse error at or near `COME_FROM_ASYNC_WITH' instruction at offset 56_0

    async def create_sequence--- This code section failed: ---

 L. 260         0  LOAD_FAST                'self'
                2  LOAD_ATTR                sequences
                4  POP_JUMP_IF_FALSE    66  'to 66'

 L. 261         6  LOAD_FAST                'self'
                8  LOAD_ATTR                compiler
               10  CALL_FUNCTION_0       0  '0 positional arguments'
               12  STORE_FAST               'qc'

 L. 262        14  LOAD_FAST                'self'
               16  LOAD_ATTR                get_conn
               18  CALL_FUNCTION_0       0  '0 positional arguments'
               20  BEFORE_ASYNC_WITH
               22  GET_AWAITABLE    
               24  LOAD_CONST               None
               26  YIELD_FROM       
               28  SETUP_ASYNC_WITH     54  'to 54'
               30  STORE_FAST               'conn'

 L. 263        32  LOAD_FAST                'conn'
               34  LOAD_ATTR                execute_sql
               36  LOAD_FAST                'qc'
               38  LOAD_ATTR                create_sequence
               40  LOAD_FAST                'seq'
               42  CALL_FUNCTION_1       1  '1 positional argument'
               44  CALL_FUNCTION_EX      0  'positional arguments only'
               46  GET_AWAITABLE    
               48  LOAD_CONST               None
               50  YIELD_FROM       
               52  RETURN_VALUE     
             54_0  COME_FROM_ASYNC_WITH    28  '28'
               54  WITH_CLEANUP_START
               56  GET_AWAITABLE    
               58  LOAD_CONST               None
               60  YIELD_FROM       
               62  WITH_CLEANUP_FINISH
               64  END_FINALLY      
             66_0  COME_FROM             4  '4'

Parse error at or near `COME_FROM_ASYNC_WITH' instruction at offset 54_0

    async def drop_table--- This code section failed: ---

 L. 266         0  LOAD_FAST                'self'
                2  LOAD_ATTR                compiler
                4  CALL_FUNCTION_0       0  '0 positional arguments'
                6  STORE_FAST               'qc'

 L. 267         8  LOAD_FAST                'cascade'
               10  POP_JUMP_IF_FALSE    28  'to 28'
               12  LOAD_FAST                'self'
               14  LOAD_ATTR                drop_cascade
               16  UNARY_NOT        
               18  POP_JUMP_IF_FALSE    28  'to 28'

 L. 268        20  LOAD_GLOBAL              ValueError
               22  LOAD_STR                 'Database does not support DROP TABLE..CASCADE.'
               24  CALL_FUNCTION_1       1  '1 positional argument'
               26  RAISE_VARARGS_1       1  'exception'
             28_0  COME_FROM            18  '18'
             28_1  COME_FROM            10  '10'

 L. 270        28  LOAD_FAST                'self'
               30  LOAD_ATTR                get_conn
               32  CALL_FUNCTION_0       0  '0 positional arguments'
               34  BEFORE_ASYNC_WITH
               36  GET_AWAITABLE    
               38  LOAD_CONST               None
               40  YIELD_FROM       
               42  SETUP_ASYNC_WITH     76  'to 76'
               44  STORE_FAST               'conn'

 L. 271        46  LOAD_FAST                'qc'
               48  LOAD_ATTR                drop_table
               50  LOAD_FAST                'model_class'
               52  LOAD_FAST                'fail_silently'
               54  LOAD_FAST                'cascade'
               56  CALL_FUNCTION_3       3  '3 positional arguments'
               58  STORE_FAST               'args'

 L. 272        60  LOAD_FAST                'conn'
               62  LOAD_ATTR                execute_sql
               64  LOAD_FAST                'args'
               66  CALL_FUNCTION_EX      0  'positional arguments only'
               68  GET_AWAITABLE    
               70  LOAD_CONST               None
               72  YIELD_FROM       
               74  RETURN_VALUE     
             76_0  COME_FROM_ASYNC_WITH    42  '42'
               76  WITH_CLEANUP_START
               78  GET_AWAITABLE    
               80  LOAD_CONST               None
               82  YIELD_FROM       
               84  WITH_CLEANUP_FINISH
               86  END_FINALLY      

Parse error at or near `COME_FROM_ASYNC_WITH' instruction at offset 76_0

    async def drop_tables(self, models, safe=False, cascade=False):
        await drop_model_tables(models, fail_silently=safe, cascade=cascade)

    async def truncate_table--- This code section failed: ---

 L. 278         0  LOAD_FAST                'self'
                2  LOAD_ATTR                compiler
                4  CALL_FUNCTION_0       0  '0 positional arguments'
                6  STORE_FAST               'qc'

 L. 279         8  LOAD_FAST                'self'
               10  LOAD_ATTR                get_conn
               12  CALL_FUNCTION_0       0  '0 positional arguments'
               14  BEFORE_ASYNC_WITH
               16  GET_AWAITABLE    
               18  LOAD_CONST               None
               20  YIELD_FROM       
               22  SETUP_ASYNC_WITH     56  'to 56'
               24  STORE_FAST               'conn'

 L. 280        26  LOAD_FAST                'qc'
               28  LOAD_ATTR                truncate_table
               30  LOAD_FAST                'model_class'
               32  LOAD_FAST                'restart_identity'
               34  LOAD_FAST                'cascade'
               36  CALL_FUNCTION_3       3  '3 positional arguments'
               38  STORE_FAST               'args'

 L. 281        40  LOAD_FAST                'conn'
               42  LOAD_ATTR                execute_sql
               44  LOAD_FAST                'args'
               46  CALL_FUNCTION_EX      0  'positional arguments only'
               48  GET_AWAITABLE    
               50  LOAD_CONST               None
               52  YIELD_FROM       
               54  RETURN_VALUE     
             56_0  COME_FROM_ASYNC_WITH    22  '22'
               56  WITH_CLEANUP_START
               58  GET_AWAITABLE    
               60  LOAD_CONST               None
               62  YIELD_FROM       
               64  WITH_CLEANUP_FINISH
               66  END_FINALLY      

Parse error at or near `COME_FROM_ASYNC_WITH' instruction at offset 56_0

    async def truncate_tables(self, models, restart_identity=False, cascade=False):
        for model in reversed(sort_models_topologically(models)):
            await model.truncate_table(restart_identity, cascade)

    async def drop_sequence--- This code section failed: ---

 L. 288         0  LOAD_FAST                'self'
                2  LOAD_ATTR                sequences
                4  POP_JUMP_IF_FALSE    66  'to 66'

 L. 289         6  LOAD_FAST                'self'
                8  LOAD_ATTR                compiler
               10  CALL_FUNCTION_0       0  '0 positional arguments'
               12  STORE_FAST               'qc'

 L. 290        14  LOAD_FAST                'self'
               16  LOAD_ATTR                get_conn
               18  CALL_FUNCTION_0       0  '0 positional arguments'
               20  BEFORE_ASYNC_WITH
               22  GET_AWAITABLE    
               24  LOAD_CONST               None
               26  YIELD_FROM       
               28  SETUP_ASYNC_WITH     54  'to 54'
               30  STORE_FAST               'conn'

 L. 291        32  LOAD_FAST                'conn'
               34  LOAD_ATTR                execute_sql
               36  LOAD_FAST                'qc'
               38  LOAD_ATTR                drop_sequence
               40  LOAD_FAST                'seq'
               42  CALL_FUNCTION_1       1  '1 positional argument'
               44  CALL_FUNCTION_EX      0  'positional arguments only'
               46  GET_AWAITABLE    
               48  LOAD_CONST               None
               50  YIELD_FROM       
               52  RETURN_VALUE     
             54_0  COME_FROM_ASYNC_WITH    28  '28'
               54  WITH_CLEANUP_START
               56  GET_AWAITABLE    
               58  LOAD_CONST               None
               60  YIELD_FROM       
               62  WITH_CLEANUP_FINISH
               64  END_FINALLY      
             66_0  COME_FROM             4  '4'

Parse error at or near `COME_FROM_ASYNC_WITH' instruction at offset 54_0

    async def execute_sql--- This code section failed: ---

 L. 294         0  LOAD_FAST                'self'
                2  LOAD_ATTR                get_conn
                4  CALL_FUNCTION_0       0  '0 positional arguments'
                6  BEFORE_ASYNC_WITH
                8  GET_AWAITABLE    
               10  LOAD_CONST               None
               12  YIELD_FROM       
               14  SETUP_ASYNC_WITH     40  'to 40'
               16  STORE_FAST               'conn'

 L. 295        18  LOAD_FAST                'conn'
               20  LOAD_ATTR                execute_sql
               22  LOAD_FAST                'sql'
               24  LOAD_FAST                'params'
               26  LOAD_FAST                'require_commit'
               28  LOAD_CONST               ('require_commit',)
               30  CALL_FUNCTION_KW_3     3  '3 total positional and keyword args'
               32  GET_AWAITABLE    
               34  LOAD_CONST               None
               36  YIELD_FROM       
               38  RETURN_VALUE     
             40_0  COME_FROM_ASYNC_WITH    14  '14'
               40  WITH_CLEANUP_START
               42  GET_AWAITABLE    
               44  LOAD_CONST               None
               46  YIELD_FROM       
               48  WITH_CLEANUP_FINISH
               50  END_FINALLY      

Parse error at or near `COME_FROM_ASYNC_WITH' instruction at offset 40_0

    def extract_date(self, date_part, date_field):
        return fn.EXTRACT(Clause(date_part, R('FROM'), date_field))

    def truncate_date(self, date_part, date_field):
        return fn.DATE_TRUNC(date_part, date_field)

    def default_insert_clause(self, model_class):
        return SQL('DEFAULT VALUES')

    def get_noop_sql(self):
        return 'SELECT 0 WHERE 0'

    def get_binary_type(self):
        return binary_construct


async def create_model_tables(models, **create_table_kwargs):
    for m in sort_models_topologically(models):
        await (m.create_table)(**create_table_kwargs)


async def drop_model_tables(models, **drop_table_kwargs):
    for m in reversed(sort_models_topologically(models)):
        await (m.drop_table)(**drop_table_kwargs)