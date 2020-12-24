# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /opt/work/lib/pyenv/versions/passport/lib/python3.6/site-packages/rest_framework/lib/orm/query.py
# Compiled at: 2018-08-22 22:04:47
# Size of source mod 2**32: 8481 bytes
import operator
from .peewee import SQL, Query, RawQuery, SelectQuery, NoopSelectQuery
from .peewee import CompoundSelect, DeleteQuery, UpdateQuery, InsertQuery
from .peewee import _WriteQuery
from .peewee import RESULTS_TUPLES, RESULTS_DICTS, RESULTS_NAIVE
from .utils import alist

class AsyncQuery(Query):

    async def execute(self):
        raise NotImplementedError

    async def _execute--- This code section failed: ---

 L.  16         0  LOAD_FAST                'self'
                2  LOAD_ATTR                sql
                4  CALL_FUNCTION_0       0  '0 positional arguments'
                6  UNPACK_SEQUENCE_2     2 
                8  STORE_FAST               'sql'
               10  STORE_FAST               'params'

 L.  17        12  LOAD_FAST                'self'
               14  LOAD_ATTR                database
               16  LOAD_ATTR                get_conn
               18  CALL_FUNCTION_0       0  '0 positional arguments'
               20  BEFORE_ASYNC_WITH
               22  GET_AWAITABLE    
               24  LOAD_CONST               None
               26  YIELD_FROM       
               28  SETUP_ASYNC_WITH     54  'to 54'
               30  STORE_FAST               'conn'

 L.  18        32  LOAD_FAST                'conn'
               34  LOAD_ATTR                execute_sql
               36  LOAD_FAST                'sql'
               38  LOAD_FAST                'params'
               40  LOAD_FAST                'self'
               42  LOAD_ATTR                require_commit
               44  CALL_FUNCTION_3       3  '3 positional arguments'
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

Parse error at or near `COME_FROM_ASYNC_WITH' instruction at offset 54_0

    async def scalar(self, as_tuple=False, convert=False):
        if convert:
            row = await self.tuples.first
        else:
            cursor = await self._execute
            row = await cursor.fetchone
        if row:
            if not as_tuple:
                return row[0]
        return row

    def __await__(self):
        return alist(self).__await__

    def __iter__(self):
        raise NotImplementedError

    async def __aiter__(self):
        qr = await self.execute
        return await qr.__aiter__


class AsyncRawQuery(AsyncQuery, RawQuery):

    def clone(self):
        query = AsyncRawQuery(self.model_class, self._sql, *self._params)
        query._tuples = self._tuples
        query._dicts = self._dicts
        return query

    async def execute(self):
        if self._qr is None:
            if self._tuples:
                qrw_cls = self.database.get_result_wrapper(RESULTS_TUPLES)
            else:
                if self._dicts:
                    qrw_cls = self.database.get_result_wrapper(RESULTS_DICTS)
                else:
                    qrw_cls = self.database.get_result_wrapper(RESULTS_NAIVE)
            self._qr = qrw_cls(self.model_class, await self._execute, None)
        return self._qr


class AsyncSelectQuery(AsyncQuery, SelectQuery):

    def compound_op(operator):

        def inner(self, other):
            supported_ops = self.model_class._meta.database.compound_operations
            if operator not in supported_ops:
                raise ValueError('Your database does not support %s' % operator)
            return AsyncCompoundSelect(self.model_class, self, operator, other)

        return inner

    async def aggregate(self, aggregation=None, convert=True):
        return await self._aggregate(aggregation).scalar(convert=convert)

    async def count(self, clear_limit=False):
        if self._distinct or self._group_by or self._limit or self._offset:
            return await self.wrapped_count(clear_limit=clear_limit)
        else:
            return await self.aggregate(convert=False) or 0

    async def wrapped_count(self, clear_limit=False):
        clone = self.order_by
        if clear_limit:
            clone._limit = clone._offset = None
        sql, params = clone.sql
        wrapped = 'SELECT COUNT(1) FROM (%s) AS wrapped_select' % sql
        rq = (self.model_class.raw)(wrapped, *params)
        return await rq.scalar or 0

    async def exists(self):
        clone = self.paginate(1, 1)
        clone._select = [SQL('1')]
        return bool(await clone.scalar)

    async def get(self):
        clone = self.paginate(1, 1)
        try:
            qr = await clone.execute
            return await qr.__anext__
        except StopAsyncIteration:
            raise self.model_class.DoesNotExist('Instance matching query does not exist:\nSQL: %s\nPARAMS: %s' % self.sql)

    async def peek(self, n=1):
        res = await self.execute
        await res.fill_cache(n)
        models = res._result_cache[:n]
        if models:
            if n == 1:
                return models[0]
            else:
                return models

    async def first(self, n=1):
        if self._limit != n:
            self._limit = n
            self._dirty = True
        return await self.peek(n=n)

    def sql(self):
        return self.compiler.generate_select(self)

    async def execute(self):
        if self._dirty or self._qr is None:
            model_class = self.model_class
            query_meta = self.get_query_meta
            result_wrapper_cls = self._get_result_wrapper
            cursor = await self._execute
            self._qr = result_wrapper_cls(model_class, cursor, query_meta)
            self._dirty = False
            return self._qr
        else:
            return self._qr

    async def iterator--- This code section failed: ---

 L. 136         0  LOAD_FAST                'self'
                2  LOAD_ATTR                execute
                4  CALL_FUNCTION_0       0  '0 positional arguments'
                6  GET_AWAITABLE    
                8  LOAD_CONST               None
               10  YIELD_FROM       
               12  STORE_FAST               'qr'

 L. 137        14  SETUP_LOOP           76  'to 76'
               16  LOAD_FAST                'qr'
               18  LOAD_ATTR                iterator
               20  CALL_FUNCTION_0       0  '0 positional arguments'
               22  GET_AITER        
               24  LOAD_CONST               None
               26  YIELD_FROM       
               28  SETUP_EXCEPT         42  'to 42'
               30  GET_ANEXT        
               32  LOAD_CONST               None
               34  YIELD_FROM       
               36  STORE_FAST               'row'
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
               60  JUMP_ABSOLUTE        76  'to 76'
               62  END_FINALLY      
             64_0  COME_FROM            40  '40'

 L. 138        64  LOAD_FAST                'row'
               66  YIELD_VALUE      
               68  POP_TOP          
               70  JUMP_BACK            28  'to 28'
               72  POP_BLOCK        
               74  JUMP_ABSOLUTE        76  'to 76'
             76_0  COME_FROM_LOOP       14  '14'

Parse error at or near `JUMP_ABSOLUTE' instruction at offset 74

    def __getitem__(self, value):
        raise NotImplementedError

    def __len__(self):
        raise NotImplementedError

    def __hash__(self):
        return id(self)


class AsyncNoopSelectQuery(AsyncSelectQuery, NoopSelectQuery):
    pass


class AsyncCompoundSelect(AsyncSelectQuery, CompoundSelect):
    _node_type = 'compound_select_query'

    async def count(self, clear_limit=False):
        return await self.wrapped_count(clear_limit=clear_limit)


class _AsyncWriteQuery(AsyncQuery, _WriteQuery):

    async def _execute_with_result_wrapper(self):
        result_wrapper_cls = self.get_result_wrapper
        meta = (self._returning, {self.model_class: []})
        self._qr = result_wrapper_cls(self.model_class, await self._execute, meta)
        return self._qr

    def __await__(self):
        return self.execute.__await__


class AsyncUpdateQuery(_AsyncWriteQuery, UpdateQuery):

    async def execute(self):
        if self._returning is not None:
            if self._qr is None:
                return await self._execute_with_result_wrapper
        if self._qr is not None:
            return self._qr
        else:
            return self.database.rows_affected(await self._execute)

    def __aiter__(self):
        if not self.model_class._meta.database.returning_clause:
            raise ValueError('UPDATE queries cannot be iterated over unless they specify a RETURNING clause, which is not supported by your database.')
        return self.execute


class AsyncInsertQuery(_AsyncWriteQuery, InsertQuery):

    async def _insert_with_loop(self):
        id_list = []
        last_id = None
        return_id_list = self._return_id_list
        for row in self._rows:
            last_id = await AsyncInsertQuery(self.model_class, row).upsert(self._upsert).execute
            if return_id_list:
                id_list.append(last_id)

        if return_id_list:
            return id_list
        else:
            return last_id

    async def execute(self):
        insert_with_loop = self._is_multi_row_insert and self._query is None and self._returning is None and not self.database.insert_many
        if insert_with_loop:
            return await self._insert_with_loop
        if self._returning is not None:
            if self._qr is None:
                return await self._execute_with_result_wrapper
        if self._qr is not None:
            return self._qr
        cursor = await self._execute
        if not self._is_multi_row_insert:
            if self.database.insert_returning:
                pk_row = await cursor.fetchone
                meta = self.model_class._meta
                clean_data = [field.python_value(column) for field, column in zip(meta.get_primary_key_fields, pk_row)]
                if self.model_class._meta.composite_key:
                    return clean_data
                else:
                    return clean_data[0]
            return self.database.last_insert_id(cursor, self.model_class)
        else:
            if self._return_id_list:
                return map(operator.itemgetter(0), await cursor.fetchall)
            return True


class AsyncDeleteQuery(_AsyncWriteQuery, DeleteQuery):

    async def execute(self):
        if self._returning is not None:
            if self._qr is None:
                return await self._execute_with_result_wrapper
        if self._qr is not None:
            return self._qr
        else:
            return self.database.rows_affected(await self._execute)


class AsyncEmptyQuery(AsyncSelectQuery):

    def __init__(self, *iterable):
        self._it = iter(iterable)

    async def __aiter__(self):
        return self

    async def __anext__(self):
        try:
            return next(self._it)
        except StopIteration as e:
            raise StopAsyncIteration from e