# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-x86_64/egg/db/queries/mssql.py
# Compiled at: 2016-10-29 16:12:01
queries = {'dbtype': 'mssql', 'column': {'head': 'select top {n} {column} from {table};', 
              'all': 'select {column} from {table};', 
              'unique': 'select distinct {column} from {table};', 
              'sample': 'select top {n} {column} from {table} order by rand();'}, 
   'table': {'select': 'select {columns} from {table};', 
             'head': 'select top {n} * from {table};', 
             'all': 'select * from {table};', 
             'unique': 'select distinct {columns} from {table};', 
             'sample': 'select top {n} * from {table} order by rand();'}, 
   'system': {'schema_no_system': "\n                select\n                    table_name\n                    , column_name\n                    , data_type\n                from\n                    information_schema.columns\n                where\n                    table_schema not in ('information_schema', 'sys')\n                ", 
              'schema_with_system': '\n                select\n                    table_name\n                    , column_name\n                    , data_type\n                from\n                    information_schema.columns;\n                ', 
              'schema_specified': '\n                select\n                    table_name\n                    , column_name\n                    , data_type\n                from\n                    information_schema.columns\n                where table_schema in (%s);\n                ', 
              'foreign_keys_for_table': "\n            SELECT\n                parent_col.name AS foreign_key,\n                object_name(referenced_object_id) AS referenced_table,\n                col.name AS referenced_column\n            FROM sys.foreign_key_columns\n            INNER JOIN sys.columns col\n                ON col.column_id = referenced_column_id\n                    AND col.object_id = referenced_object_id\n            INNER JOIN sys.columns parent_col\n                ON parent_col.column_id = parent_column_id\n                   AND parent_col.object_id = parent_object_id\n            WHERE parent_object_id = object_id('%s');\n        ", 
              'foreign_keys_for_column': "\n            SELECT\n                object_name(constraint_object_id) AS foreign_key,\n                object_name(referenced_object_id) AS referenced_table,\n                col.name AS referenced_column\n            FROM sys.foreign_key_columns\n            INNER JOIN sys.columns col\n                ON col.column_id = referenced_column_id\n                    AND col.object_id = referenced_object_id\n            WHERE parent_object_id = object_id('%s')\n                AND constraint_object_id = object_id('%s');\n        ", 
              'ref_keys_for_table': "\n            SELECT\n                ref_col.name,\n                object_name(parent_object_id),\n                col.name as column_name\n            FROM sys.foreign_key_columns\n            INNER JOIN sys.columns col\n               ON col.column_id = parent_column_id\n                   AND col.object_id = parent_object_id\n            INNER JOIN sys.columns ref_col\n                ON ref_col.column_id = referenced_column_id\n                   AND ref_col.object_id = referenced_object_id\n            WHERE referenced_object_id = object_id('%s');\n        "}}