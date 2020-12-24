# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-x86_64/egg/db/queries/mysql.py
# Compiled at: 2016-10-29 16:11:50
queries = {'dbtype': 'mysql', 'column': {'head': 'select {column} from {schema}.{table} limit {n};', 
              'all': 'select {column} from {schema}.{table};', 
              'unique': 'select distinct {column} from {schema}.{table};', 
              'sample': 'select {column} from {schema}.{table} order by rand() limit {n};'}, 
   'table': {'select': 'select {columns} from {schema}.{table};', 
             'head': 'select * from {schema}.{table} limit {n};', 
             'all': 'select * from {schema}.{table};', 
             'unique': 'select distinct {columns} from {schema}.{table};', 
             'sample': 'select * from {schema}.{table} order by rand() limit {n};'}, 
   'system': {'schema_no_system': "\n                select table_schema\n                    , table_name\n                    , column_name\n                    , data_type\n                from\n                    information_schema.columns\n                where\n                    table_schema not in ('information_schema', 'performance_schema', 'mysql')\n                ", 
              'schema_with_system': '\n                select table_schema\n                    , table_name\n                    , column_name\n                    , data_type\n                from\n                    information_schema.columns;\n                ', 
              'schema_specified': '\n                select table_schema\n                    , table_name\n                    , column_name\n                    , udt_name\n                from\n                    information_schema.columns\n                where table_schema in (%s);\n                ', 
              'foreign_keys_for_table': "\n        select column_name\n            , referenced_table_schema\n            , referenced_table_name\n            , referenced_column_name\n        from\n            information_schema.key_column_usage\n        where\n            table_name = '{table}'\n            and referenced_column_name IS NOT NULL\n            and table_schema = '{table_schema}';\n        ", 
              'foreign_keys_for_column': "\n        select column_name\n            , referenced_table_schema\n            , referenced_table_name\n            , referenced_column_name\n        from\n            information_schema.key_column_usage\n        where\n            table_name = '{table}'\n            and column_name = '{column}'\n            and referenced_column_name IS NOT NULL\n            and table_schema = '{table_schema}';\n        ", 
              'ref_keys_for_table': "\n            select referenced_column_name\n                , table_schema\n                , table_name\n                , column_name\n            from\n                information_schema.key_column_usage\n            where\n                referenced_table_name = '{table}'\n                and referenced_column_name IS NOT NULL\n                and table_schema = '{table_schema}';\n        ", 
              'foreign_keys_for_db': '\n            select column_name\n                , referenced_table_schema\n                , referenced_table_name\n                , referenced_column_name\n            FROM\n                information_schema.key_column_usage\n            WHERE referenced_column_name IS NOT NULL;\n        ', 
              'ref_keys_for_db': '\n            SELECT referenced_column_name,\n                   table_schema,\n                   table_name,\n                   column_name\n            FROM\n                information_schema.key_column_usage\n            WHERE referenced_column_name IS NOT NULL;\n        '}}