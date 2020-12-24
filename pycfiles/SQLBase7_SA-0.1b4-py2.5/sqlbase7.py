# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\sqlbase7_sa\sqlbase7.py
# Compiled at: 2010-07-31 21:07:03
from sqlalchemy.engine.default import DefaultDialect
from sqlalchemy import types, and_
from sqlalchemy.sql.expression import Join
from sqlalchemy.sql import visitors, operators, ClauseElement
import sqlalchemy
from pkg_resources import parse_version
if parse_version(sqlalchemy.__version__) <= parse_version('0.5.99'):
    from sqlalchemy.sql.compiler import DefaultCompiler as CompilerBase
else:
    from sqlalchemy.sql.compiler import SQLCompiler as CompilerBase

class LimitClauseNotSupported(Exception):

    def __init__(self, limit, offset):
        self.limit = limit
        self.offset = offset

    def __str__(self):
        return "Centura SQLBase 7.5.1 doesn't support a LIMIT clause for the SELECT statement (received: limit = %u, offset = %u)" % (self.limit, self.offset)


class SQLBase7Compiler(CompilerBase):

    def visit_join(self, join, **kwargs):
        kwargs['asfrom'] = True
        return self.process(join.left, **kwargs) + ', ' + self.process(join.right, **kwargs)

    def visit_select(self, select, **kwargs):
        if self.stack and 'from' in self.stack[(-1)]:
            existingfroms = self.stack[(-1)]['from']
        else:
            existingfroms = None
        froms = select._get_display_froms(existingfroms)
        whereclause = self._get_join_whereclause(froms)
        if whereclause is not None:
            select = select.where(whereclause)
        if select._limit is not None or select._offset is not None:
            raise LimitClauseNotSupported(select._limit, select._offset)
        kwargs['iswrapper'] = getattr(select, '_is_wrapper', False)
        return super(SQLBase7Compiler, self).visit_select(select, **kwargs)

    def _get_join_whereclause(self, froms):
        clauses = []

        def visit_join(join):
            if join.isouter:

                def visit_binary(binary):
                    if binary.operator == operators.eq:
                        if binary.left.table is join.right:
                            binary.left = _OuterJoinColumn(binary.left)
                        elif binary.right.table is join.right:
                            binary.right = _OuterJoinColumn(binary.right)

                clauses.append(visitors.cloned_traverse(join.onclause, {}, {'binary': visit_binary}))
            else:
                clauses.append(join.onclause)
            for j in (join.left, join.right):
                if isinstance(j, Join):
                    visit_join(j)

        for f in froms:
            if isinstance(f, Join):
                visit_join(f)

        if clauses:
            return and_(*clauses)
        return

    def visit_outer_join_column(self, vc):
        return self.process(vc.column) + '(+)'


class _OuterJoinColumn(ClauseElement):
    __visit_name__ = 'outer_join_column'

    def __init__(self, column):
        self.column = column


class SQLBase7Dialect(DefaultDialect):
    name = 'sqlbase7'
    statement_compiler = SQLBase7Compiler
    max_identifier_length = 18
    _type_map = {'CHAR': types.CHAR, 
       'DATE': types.DATE, 
       'DECIMAL': types.DECIMAL, 
       'FLOAT': types.FLOAT, 
       'SMALLINT': types.SMALLINT, 
       'TIME': types.TIME, 
       'TIMESTMP': types.TIMESTAMP, 
       'VARCHAR': types.VARCHAR}

    def create_connect_args(self, url):
        connection_string = (';').join((
         'DRIVER={Centura SQLBase 3.5 32-bit Driver -NT & Win95}',
         'SERVER=%s' % url.host,
         'DATABASE=%s' % url.database,
         'UID=%s' % url.username,
         'PWD=%s' % url.password))
        return (
         [
          connection_string], {})

    def get_default_schema_name(self, connection):
        return 'SYSADM'

    def do_execute(self, cursor, statement, parameters, context=None):
        parameters = list(parameters)
        for (i, parameter) in enumerate(parameters):
            if isinstance(parameter, unicode):
                parameters[i] = str(parameter)
            elif isinstance(parameter, long):
                parameters[i] = int(parameter)

        super(SQLBase7Dialect, self).do_execute(cursor, statement, tuple(parameters), context)