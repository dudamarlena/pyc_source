# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/sqlalchemy_hawq/dialect.py
# Compiled at: 2019-10-07 13:43:57
# Size of source mod 2**32: 1816 bytes
""" Customizes the postgresql.psycopg2 dialect to work with Hawq. """
from sqlalchemy.dialects import postgresql
from sqlalchemy import schema
from sqlalchemy.ext.compiler import compiles
from sqlalchemy.sql.expression import Delete
from .ddl import HawqDDLCompiler

class HawqDialect(postgresql.psycopg2.PGDialect_psycopg2):
    __doc__ = '\n    Main dialect class. Used by the engine to compile sql\n    '
    construct_arguments = [
     (
      schema.Table,
      {'partition_by':None, 
       'inherits':None, 
       'distributed_by':None, 
       'bucketnum':None, 
       'appendonly':None, 
       'orientation':None, 
       'compresstype':None, 
       'compresslevel':None, 
       'on_commit':None, 
       'tablespace':None})]
    ddl_compiler = HawqDDLCompiler
    name = 'hawq'

    def initialize(self, connection):
        super().initialize(connection)
        self.implicit_returning = False

    @compiles(Delete, 'hawq')
    def visit_delete_statement(element, compiler, **kwargs):
        """
        Allows a version of the delete statement to get compiled - the version
        that is effectively the same as truncate.

        Any filters on the delete statement result in an Exception.
        """
        delete_stmt_table = (compiler.process)(element.table, asfrom=True, **kwargs)
        filters_tuple = element.get_children()
        if not filters_tuple:
            return 'TRUNCATE TABLE {}'.format(delete_stmt_table)
        raise NotImplementedError('Delete statement with filter clauses not implemented for Hawq')