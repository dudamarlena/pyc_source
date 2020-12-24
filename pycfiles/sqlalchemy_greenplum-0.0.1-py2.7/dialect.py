# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\sqlalchemy_greenplum\dialect.py
# Compiled at: 2018-03-21 21:36:38
import sqlalchemy
from sqlalchemy.dialects.postgresql.base import PGDialect, PGDDLCompiler
from sqlalchemy.dialects.postgresql.psycopg2 import PGDialect_psycopg2

class GreenPlumDDLCompiler(PGDDLCompiler):

    def post_create_table(self, table):
        table_opts = []
        gp_opts = table.dialect_options['greenplum']
        inherits = gp_opts.get('inherits')
        if inherits is not None:
            if not isinstance(inherits, (list, tuple)):
                inherits = (
                 inherits,)
            table_opts.append('\n INHERITS ( ' + (', ').join(self.preparer.quote(name) for name in inherits) + ' )')
        if gp_opts['storage_params']:
            table_opts.append(('\n WITH ({0})').format(gp_opts['storage_params']).upper())
        if gp_opts['on_commit']:
            on_commit_options = gp_opts['on_commit'].replace('_', ' ').upper()
            table_opts.append('\n ON COMMIT %s' % on_commit_options)
        if gp_opts['tablespace']:
            tablespace_name = gp_opts['tablespace']
            table_opts.append('\n TABLESPACE %s' % self.preparer.quote(tablespace_name))
        if gp_opts['distributed_by']:
            if gp_opts['distributed_by'].upper() == 'RANDOM':
                table_opts.append('\n DISTRIBUTED RANDOMLY')
            else:
                table_opts.append(('\n DISTRIBUTED BY ({0})').format(gp_opts['distributed_by']))
        return ('').join(table_opts)


class GreenPlumDialect(PGDialect_psycopg2):
    name = 'greenplum'
    ddl_compiler = GreenPlumDDLCompiler
    construct_arguments = [
     (
      sqlalchemy.schema.Index,
      {'using': False, 
         'where': None, 
         'ops': {}, 'concurrently': False, 
         'with': {}, 'tablespace': None}),
     (
      sqlalchemy.schema.Table,
      {'ignore_search_path': False, 
         'tablespace': None, 
         'storage_params': None, 
         'on_commit': None, 
         'inherits': None, 
         'distributed_by': None})]

    def __init__(self, *args, **kw):
        super(GreenPlumDialect, self).__init__(*args, **kw)