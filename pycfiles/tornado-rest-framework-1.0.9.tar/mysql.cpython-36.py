# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /opt/work/lib/pyenv/versions/3.6.1/envs/maestro/lib/python3.6/site-packages/rest_framework/lib/orm/mysql.py
# Compiled at: 2018-05-06 21:04:31
# Size of source mod 2**32: 3031 bytes
try:
    import aiomysql
except ImportError:
    aiomysql = None

from .peewee import mysql, ImproperlyConfigured
from .peewee import MySQLDatabase, IndexMetadata, ColumnMetadata, ForeignKeyMetadata
from .database import AsyncDatabase

class AsyncMySQLDatabase(AsyncDatabase, MySQLDatabase):

    async def _connect(self, database, **kwargs):
        if not aiomysql:
            raise ImproperlyConfigured('aiomysql must be installed.')
        conn_kwargs = {'charset':'utf8',  'use_unicode':True}
        conn_kwargs.update(kwargs)
        return await (aiomysql.create_pool)(db=database, **conn_kwargs)

    async def get_tables--- This code section failed: ---

 L.  30         0  LOAD_FAST                'self'
                2  LOAD_ATTR                get_conn
                4  CALL_FUNCTION_0       0  '0 positional arguments'
                6  BEFORE_ASYNC_WITH
                8  GET_AWAITABLE    
               10  LOAD_CONST               None
               12  YIELD_FROM       
               14  SETUP_ASYNC_WITH     58  'to 58'
               16  STORE_FAST               'conn'

 L.  31        18  LOAD_FAST                'conn'
               20  LOAD_ATTR                execute_sql
               22  LOAD_STR                 'SHOW TABLES'
               24  CALL_FUNCTION_1       1  '1 positional argument'
               26  GET_AWAITABLE    
               28  LOAD_CONST               None
               30  YIELD_FROM       
               32  STORE_FAST               'cursor'

 L.  32        34  LOAD_LISTCOMP            '<code_object <listcomp>>'
               36  LOAD_STR                 'AsyncMySQLDatabase.get_tables.<locals>.<listcomp>'
               38  MAKE_FUNCTION_0          'Neither defaults, keyword-only args, annotations, nor closures'
               40  LOAD_FAST                'cursor'
               42  LOAD_ATTR                fetchall
               44  CALL_FUNCTION_0       0  '0 positional arguments'
               46  GET_AWAITABLE    
               48  LOAD_CONST               None
               50  YIELD_FROM       
               52  GET_ITER         
               54  CALL_FUNCTION_1       1  '1 positional argument'
               56  RETURN_VALUE     
             58_0  COME_FROM_ASYNC_WITH    14  '14'
               58  WITH_CLEANUP_START
               60  GET_AWAITABLE    
               62  LOAD_CONST               None
               64  YIELD_FROM       
               66  WITH_CLEANUP_FINISH
               68  END_FINALLY      

Parse error at or near `COME_FROM_ASYNC_WITH' instruction at offset 58_0

    async def get_indexes(self, table, schema=None):
        unique = set
        indexes = {}
        async with self.get_conn as conn:
            sql = 'SHOW INDEX FROM `%s`' % table
            cursor = await conn.execute_sql(sql)
            for row in cursor.fetchall:
                if not row[1]:
                    unique.add(row[2])
                indexes.setdefault(row[2], [])
                indexes[row[2]].append(row[4])

        return [IndexMetadata(name, None, indexes[name], name in unique, table) for name in indexes]

    async def get_columns(self, table, schema=None):
        sql = '\n            SELECT column_name, is_nullable, data_type\n            FROM information_schema.columns\n            WHERE table_name = %s AND table_schema = DATABASE()'
        async with self.get_conn as conn:
            cursor = await conn.execute_sql(sql, (table,))
            rows = await cursor.fetchall
        pks = set(self.get_primary_keys(table))
        return [ColumnMetadata(name, dt, null == 'YES', name in pks, table) for name, null, dt in rows]

    async def get_primary_keys(self, table, schema=None):
        async with self.get_conn as conn:
            sql = 'SHOW INDEX FROM `%s`' % table
            cursor = await conn.execute_sql(sql)
            rows = await cursor.fetchall
        return [row[4] for row in rows if row[2] == 'PRIMARY']

    async def get_foreign_keys(self, table, schema=None):
        query = '\n            SELECT column_name, referenced_table_name, referenced_column_name\n            FROM information_schema.key_column_usage\n            WHERE table_name = %s\n                AND table_schema = DATABASE()\n                AND referenced_table_name IS NOT NULL\n                AND referenced_column_name IS NOT NULL'
        async with self.get_conn as conn:
            cursor = await conn.execute_sql(query, (table,))
            rows = await cursor.fetchall
        return [ForeignKeyMetadata(column, dest_table, dest_column, table) for column, dest_table, dest_column in rows]

    def get_binary_type(self):
        return mysql.Binary