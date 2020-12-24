# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-x86_64/egg/db/queries/redshift.py
# Compiled at: 2016-10-28 17:19:46
queries = {'column': {'head': 'select {column} from {table} limit {n};', 
              'all': 'select {column} from {table};', 
              'unique': 'select distinct {column} from {table};', 
              'sample': 'select {column} from {table} order by random() limit {n};'}, 
   'table': {'select': 'select {columns} from {table};', 
             'head': 'select * from {table} limit {n};', 
             'all': 'select * from {table};', 
             'unique': 'select distinct {columns} from {table};', 
             'sample': 'select * from {table} order by random() limit {n};'}, 
   'system': {'schema_no_system': "\n                select\n                    table_name\n                    , column_name\n                    , udt_name\n                from\n                    information_schema.columns\n                where\n                    table_schema not in ('information_schema', 'pg_catalog');\n                ", 
              'schema_with_system': '\n                select\n                    table_name\n                    , column_name\n                    , udt_name\n                from\n                    information_schema.columns;\n                ', 
              'foreign_keys_for_table': "\n            SELECT\n                kcu.column_name\n                , ccu.table_name AS foreign_table_name\n                , ccu.column_name AS foreign_column_name\n            FROM\n                information_schema.table_constraints AS tc\n                JOIN information_schema.key_column_usage AS kcu\n                  ON tc.constraint_name = kcu.constraint_name\n                JOIN information_schema.constraint_column_usage AS ccu\n                  ON ccu.constraint_name = tc.constraint_name\n            WHERE constraint_type = 'FOREIGN KEY' AND tc.table_name='{table}';\n        ", 
              'foreign_keys_for_column': "\n            SELECT\n                kcu.column_name\n                , ccu.table_name AS foreign_table_name\n                , ccu.column_name AS foreign_column_name\n            FROM\n                information_schema.table_constraints AS tc\n                JOIN information_schema.key_column_usage AS kcu\n                  ON tc.constraint_name = kcu.constraint_name\n                JOIN information_schema.constraint_column_usage AS ccu\n                  ON ccu.constraint_name = tc.constraint_name\n            WHERE constraint_type = 'FOREIGN KEY' AND tc.table_name='{table}' and kcu.column_name = '{column}';\n        ", 
              'ref_keys_for_table': "\n            SELECT\n                ccu.column_name\n                , kcu.table_name AS foreign_table_name\n                , kcu.column_name AS foreign_column_name\n            FROM\n                information_schema.table_constraints AS tc\n                JOIN information_schema.key_column_usage AS kcu\n                  ON tc.constraint_name = kcu.constraint_name\n                JOIN information_schema.constraint_column_usage AS ccu\n                  ON ccu.constraint_name = tc.constraint_name\n            WHERE constraint_type = 'FOREIGN KEY' AND ccu.table_name='{table}';\n        "}}