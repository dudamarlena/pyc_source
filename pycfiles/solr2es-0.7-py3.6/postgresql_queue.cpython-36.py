# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/solr2es/postgresql_queue.py
# Compiled at: 2018-11-28 06:14:23
# Size of source mod 2**32: 3620 bytes
from asyncio import ensure_future, wait_for, futures
from json import dumps, loads
import sqlalchemy as sa
from psycopg2.extras import execute_values
from sqlalchemy.dialects.postgresql import insert
POP_DOCS_SQL = "UPDATE solr2es_queue SET done = 't' WHERE uid IN (SELECT uid FROM solr2es_queue WHERE done = 'f' ORDER BY uid FOR UPDATE SKIP LOCKED LIMIT 10) RETURNING json"
CREATE_TABLE_SQL = 'CREATE TABLE IF NOT EXISTS "solr2es_queue" (uid serial primary key,id varchar(64) not null UNIQUE,json text not null,done boolean default false )'
INSERT_SQL = 'INSERT INTO solr2es_queue (id, json) VALUES %s'
SIZE_SQL = "SELECT COUNT(*) FROM solr2es_queue WHERE done = 'f'"
metadata = sa.MetaData()
queue_table = sa.Table('solr2es_queue', metadata, sa.Column('uid', (sa.Integer), primary_key=True), sa.Column('id', sa.String(64)), sa.Column('json', sa.Text()))

class PostgresqlQueue(object):

    def __init__(self, connection, unique_id='id') -> None:
        self.unique_id = unique_id
        self.connection = connection
        self.connection.set_isolation_level(0)

    def push_loop(self, producer):
        self.create_table_if_not_exists()
        for results in producer():
            self.push(results)

    def push(self, value_list):
        cursor = self.connection.cursor()
        values = ((r[self.unique_id], dumps(r)) for r in value_list)
        execute_values(cursor, INSERT_SQL, values)
        cursor.close()

    def create_table_if_not_exists(self):
        cursor = self.connection.cursor()
        cursor.execute(CREATE_TABLE_SQL)
        cursor.close()


class PostgresqlQueueAsync(object):

    def __init__(self, postgresql, unique_id='id') -> None:
        self.unique_id = unique_id
        self.postgresql = postgresql

    @classmethod
    async def create(cls, postgresql, unique_id='id'):
        self = cls(postgresql, unique_id=unique_id)
        await self.create_table_if_not_exists()
        return self

    async def push_loop--- This code section failed: ---

 L.  63         0  SETUP_LOOP           66  'to 66'
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
               32  POP_JUMP_IF_TRUE     54  'to 54'
               34  END_FINALLY      
             36_0  COME_FROM            24  '24'

 L.  64        36  LOAD_FAST                'self'
               38  LOAD_ATTR                push
               40  LOAD_FAST                'results'
               42  CALL_FUNCTION_1       1  '1 positional argument'
               44  GET_AWAITABLE    
               46  LOAD_CONST               None
               48  YIELD_FROM       
               50  POP_TOP          
               52  JUMP_BACK            12  'to 12'
             54_0  COME_FROM            32  '32'
               54  POP_TOP          
               56  POP_TOP          
               58  POP_TOP          
               60  POP_EXCEPT       
               62  POP_TOP          
               64  POP_BLOCK        
             66_0  COME_FROM_LOOP        0  '0'

Parse error at or near `None' instruction at offset -1

    async def push(self, value_list) -> None:
        async with self.postgresql.acquire() as conn:
            values = list({'id':r[self.unique_id],  'json':dumps(r)} for r in value_list)
            await conn.execute(insert(queue_table).values(values).on_conflict_do_nothing(index_elements=['id']))
            await conn.execute("NOTIFY solr2es, 'notify'")

    async def create_table_if_not_exists(self):
        async with self.postgresql.acquire() as conn:
            await conn.execute(CREATE_TABLE_SQL)

    async def pop(self, timeout=1) -> list:
        async with self.postgresql.acquire() as conn:
            await conn.execute('LISTEN solr2es')
            while True:
                async with conn.begin():
                    result_proxy = await conn.execute(POP_DOCS_SQL)
                    if result_proxy.rowcount:
                        return list(map(lambda row: loads(row[0]), await result_proxy.fetchall()))
                notification = ensure_future(conn.connection.notifies.get())
                try:
                    await wait_for(notification, timeout)
                except futures.TimeoutError:
                    return []

    async def size--- This code section failed: ---

 L.  91         0  LOAD_FAST                'self'
                2  LOAD_ATTR                postgresql
                4  LOAD_ATTR                acquire
                6  CALL_FUNCTION_0       0  '0 positional arguments'
                8  BEFORE_ASYNC_WITH
               10  GET_AWAITABLE    
               12  LOAD_CONST               None
               14  YIELD_FROM       
               16  SETUP_ASYNC_WITH     50  'to 50'
               18  STORE_FAST               'conn'

 L.  92        20  LOAD_FAST                'conn'
               22  LOAD_ATTR                execute
               24  LOAD_GLOBAL              SIZE_SQL
               26  CALL_FUNCTION_1       1  '1 positional argument'
               28  GET_AWAITABLE    
               30  LOAD_CONST               None
               32  YIELD_FROM       
               34  STORE_FAST               'result_proxy'

 L.  93        36  LOAD_FAST                'result_proxy'
               38  LOAD_ATTR                scalar
               40  CALL_FUNCTION_0       0  '0 positional arguments'
               42  GET_AWAITABLE    
               44  LOAD_CONST               None
               46  YIELD_FROM       
               48  RETURN_VALUE     
             50_0  COME_FROM_ASYNC_WITH    16  '16'
               50  WITH_CLEANUP_START
               52  GET_AWAITABLE    
               54  LOAD_CONST               None
               56  YIELD_FROM       
               58  WITH_CLEANUP_FINISH
               60  END_FINALLY      

Parse error at or near `COME_FROM_ASYNC_WITH' instruction at offset 50_0