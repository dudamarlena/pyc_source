# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-x86_64/egg/db/queries/sqlite.py
# Compiled at: 2016-10-29 16:11:55
queries = {'dbtype': 'sqlite', 'column': {'head': 'select {column} from {table} limit {n};', 
              'all': 'select {column} from {table};', 
              'unique': 'select distinct {column} from {table};', 
              'sample': 'select {column} from {table} order by random() limit {n};'}, 
   'table': {'select': 'select {columns} from {table};', 
             'head': 'select * from {table} limit {n};', 
             'all': 'select * from {table};', 
             'unique': 'select distinct {columns} from {table};', 
             'sample': 'select * from {table} order by random() limit {n};'}, 
   'system': {'schema_no_system': "select 'public', table_name, column_name, data_type from tmp_dbpy_schema;", 
              'schema_with_system': "select 'public', table_name, column_name, data_type from tmp_dbpy_schema;", 
              'foreign_keys_for_table': "\n            select\n                column_name\n                , 'public' as foreign_table_schema\n                , foreign_table as foreign_table_name\n                , foreign_column as foreign_column_name\n            from\n                tmp_dbpy_foreign_keys\n            where\n                table_name = '{table}';\n        ", 
              'foreign_keys_for_column': "\n            select\n                column_name\n                , 'public' as ref_table_schema\n                , foreign_table as foreign_table_name\n                , foreign_column as foreign_column_name\n            from\n                tmp_dbpy_foreign_keys\n            where\n                table_name = '{table}' and column_name = '{column}';\n        ", 
              'ref_keys_for_table': "\n            select\n                 foreign_column\n                 , 'schema' as schema\n                 , table_name\n                 , column_name\n            from\n                tmp_dbpy_foreign_keys\n            where\n                foreign_table = '{table}';\n        "}}