# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/rkeilty/git/sql-data-dependency/sql_data_dependency/sqldd.py
# Compiled at: 2017-02-06 23:43:01
from __future__ import print_function
import os, shlex, subprocess, sys
from collections import defaultdict, namedtuple
from sqlalchemy import create_engine, inspect
from six import iteritems

class SqlDatabaseDependencyManager(object):

    def __init__(self, server=None, database=None, username=None, password=None, port=None):
        self._server = server
        self._database = database
        self._username = username
        self._password = password
        self._port = port
        self.engine = create_engine(('mysql://{username}:{password}@{server}:{port}/{database}').format(username=self._username, password=self._password, server=self._server, port=self._port, database=self._database))
        self.inspector = inspect(self.engine)

    def get_database_dependencies(self, table_column_roots, already_explored=defaultdict(lambda : [])):
        dependencies = defaultdict(lambda : [])
        for table, primary_keys in iteritems(table_column_roots):
            for primary_key in primary_keys:
                if primary_key in already_explored[table]:
                    continue
                already_explored[table].append(primary_key)
                row_depdencies = self.get_row_dependencies(table, primary_key, already_explored=already_explored)
                for row_dependency_table, row_dependency_primary_keys in iteritems(row_depdencies):
                    current_row_dependency_primary_keys = dependencies[row_dependency_table]
                    dependencies[row_dependency_table] = current_row_dependency_primary_keys + list(set(row_dependency_primary_keys) - set(current_row_dependency_primary_keys))

        return dependencies

    def get_row_dependencies(self, table, primary_key, already_explored=defaultdict(lambda : [])):
        foreign_keys = self.inspector.get_foreign_keys(table)
        if not foreign_keys:
            return {}
        else:
            ForeignKey = namedtuple('ForeignKey', ['table', 'column'])
            column_foreign_key_map = {}
            for foreign_key in foreign_keys:
                if len(foreign_key['constrained_columns']) != 1 or len(foreign_key['referred_columns']) != 1:
                    raise Exception('Too many columns referenced in foreign key')
                referenced_pk = self.inspector.get_pk_constraint(foreign_key['referred_table'])
                if set(referenced_pk['constrained_columns']) != set(foreign_key['referred_columns']):
                    raise Exception('Primary key doesnt match foreign key constraint')
                column_foreign_key_map[foreign_key['constrained_columns'][0]] = ForeignKey(table=foreign_key['referred_table'], column=foreign_key['referred_columns'][0])

            primary_key_column = self.inspector.get_pk_constraint(table)['constrained_columns'][0]
            try:
                int(primary_key)
            except:
                primary_key = ('"{}"').format(primary_key)

            table_results = self.engine.execute(('select {columns} from {table} where {primary_key_column}={primary_key}').format(columns=(',').join(column_foreign_key_map.keys()), table=table, primary_key_column=primary_key_column, primary_key=primary_key))
            table_result = None
            try:
                for row in table_results:
                    table_result = row
                    break

            finally:
                table_results.close()

            if table_result is None:
                print(('No result for table PK "{}": {}').format(table, primary_key))
                sys.exit(1)
            dependencies = defaultdict(lambda : [])
            for column, foreign_key in iteritems(column_foreign_key_map):
                if table_result[column] is not None:
                    dependencies[foreign_key.table].append(table_result[column])

            downstream_dependencies = self.get_database_dependencies(dependencies, already_explored=already_explored)
            for downstream_dep_table, downstream_dep_keys in iteritems(downstream_dependencies):
                dependencies[downstream_dep_table].extend(downstream_dep_keys)
                dependencies[downstream_dep_table] = list(set(dependencies[downstream_dep_table]))

            return dependencies

    def mysqldump_statements(self, table_key_map, server, username, password, port, database):
        mysqldump_statements = []
        for table, primary_keys in iteritems(table_key_map):
            primary_key_column = self.inspector.get_pk_constraint(table)['constrained_columns'][0]
            mysqldump_where = ('{primary_key_column} in ({primary_key})').format(primary_key_column=primary_key_column, primary_key=(',').join([ (isinstance(pk, str) or str)(pk) if 1 else ("'{}'").format(pk) for pk in primary_keys ]))
            mysqldump_statements.append(('mysqldump -h {server} -u {username} --port {port} --single-transaction {database} {table} --where="{where}"').format(username=username, password=password, server=server, port=port, database=database, table=table, where=mysqldump_where))

        return mysqldump_statements

    def create_mysqldump(self, table_rows, dump_all_table_definitions=False):
        statements = self.mysqldump_statements(table_rows, self._server, self._username, self._password, self._port, self._database)
        try:
            with open(os.devnull, 'w') as (devnull):
                subprocess.check_call(['mysqldump', '--help'], stdout=devnull)
        except Exception:
            print('mysqldump not installed', file=sys.stderr)
            sys.exit(1)

        cmd_env = os.environ.copy()
        cmd_env['MYSQL_PWD'] = self._password
        dump = ''
        if dump_all_table_definitions:
            dump += subprocess.check_output(shlex.split(('mysqldump -h {server} -u {username} --port {port} --single-transaction --no-data {database}').format(server=self._server, username=self._username, port=self._port, database=self._database)), env=cmd_env)
            dump += os.linesep
        for statement in statements:
            dump += subprocess.check_output(shlex.split(statement), env=cmd_env)
            dump += os.linesep

        return dump