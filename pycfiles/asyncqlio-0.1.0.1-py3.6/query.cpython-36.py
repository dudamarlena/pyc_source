# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/asyncqlio/orm/query.py
# Compiled at: 2017-11-29 06:02:28
# Size of source mod 2**32: 25219 bytes
"""
Classes for query objects.
"""
import abc, collections, itertools, typing
from asyncqlio.backends.base import BaseResultSet
from asyncqlio.meta import AsyncABC
from asyncqlio.orm import inspection as md_inspection, operators as md_operators, session as md_session
from asyncqlio.orm.schema import column as md_column, relationship as md_relationship, table as md_table
from asyncqlio.sentinels import NO_VALUE

class BaseQuery(AsyncABC):
    __doc__ = '\n    A base query object.\n    '

    def __init__(self, sess: 'md_session.Session'):
        """
        :param sess: The :class:`.Session` associated with this query.
        """
        self.session = sess

    @abc.abstractmethod
    def generate_sql(self) -> typing.Tuple[(str, typing.Mapping[(str, typing.Any)])]:
        """
        Generates the SQL for this query.
        :return: A two item tuple, the SQL to use and a mapping of params to pass.
        """
        pass

    @abc.abstractmethod
    async def run(self):
        """
        Runs this query.
        """
        pass


class ResultGenerator(collections.AsyncIterator):
    __doc__ = '\n    A helper class that will generate new results from a query when iterated over.\n    '

    def __init__(self, q: 'SelectQuery'):
        """
        :param q: The :class:`.SelectQuery` to use. 
        """
        self.query = q
        self._results = None
        self._result_deque = collections.deque()

    async def _fill(self):
        try:
            first = self._result_deque[0]
        except IndexError:
            last_pkey = None
            rows_filled = 0
        else:
            last_pkey = tuple(first[col.alias_name(quoted=False)] for col in self.query.table.primary_key.columns)
            rows_filled = 1
        while True:
            row = await self._results.fetch_row()
            if row is None:
                break
            self._result_deque.append(row)
            pkey = tuple(row[col.alias_name(quoted=False)] for col in self.query.table.primary_key.columns)
            if last_pkey is None:
                last_pkey = pkey
                rows_filled += 1
                continue
            else:
                if pkey == last_pkey:
                    rows_filled += 1
                    continue
                else:
                    break

        return rows_filled

    async def __anext__(self):
        if self._results is None:
            self._results = await (self.query.session.cursor)(*self.query.generate_sql())
        filled = await self._fill()
        if filled == 0:
            raise StopAsyncIteration
        rows = [self._result_deque.popleft() for x in range(0, filled)]
        if len(rows) == 1:
            return self.query.map_columns(rows[0])
        else:
            return (self.query.map_many)(*rows)

    async def next(self):
        try:
            return await self.__anext__()
        except StopAsyncIteration:
            return

    async def flatten--- This code section failed: ---

 L. 129         0  BUILD_LIST_0          0 
                2  STORE_FAST               'l'

 L. 130         4  SETUP_LOOP           66  'to 66'
                6  LOAD_FAST                'self'
                8  GET_AITER        
               10  LOAD_CONST               None
               12  YIELD_FROM       
               14  SETUP_EXCEPT         28  'to 28'
               16  GET_ANEXT        
               18  LOAD_CONST               None
               20  YIELD_FROM       
               22  STORE_FAST               'result'
               24  POP_BLOCK        
               26  JUMP_FORWARD         50  'to 50'
             28_0  COME_FROM_EXCEPT     14  '14'
               28  DUP_TOP          
               30  LOAD_GLOBAL              StopAsyncIteration
               32  COMPARE_OP               exception-match
               34  POP_JUMP_IF_FALSE    48  'to 48'
               36  POP_TOP          
               38  POP_TOP          
               40  POP_TOP          
               42  POP_EXCEPT       
               44  POP_BLOCK        
               46  JUMP_ABSOLUTE        66  'to 66'
               48  END_FINALLY      
             50_0  COME_FROM            26  '26'

 L. 131        50  LOAD_FAST                'l'
               52  LOAD_ATTR                append
               54  LOAD_FAST                'result'
               56  CALL_FUNCTION_1       1  '1 positional argument'
               58  POP_TOP          
               60  JUMP_BACK            14  'to 14'
               62  POP_BLOCK        
               64  JUMP_ABSOLUTE        66  'to 66'
             66_0  COME_FROM_LOOP        4  '4'

 L. 133        66  LOAD_FAST                'l'
               68  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `JUMP_ABSOLUTE' instruction at offset 64


class SelectQuery(BaseQuery):
    __doc__ = '\n    Represents a SELECT query, which fetches data from the database.\n    \n    This is not normally created by user code directly, but rather as a result of a \n    :meth:`.Session.select` call.\n    \n    .. code-block:: python3\n\n        sess = db.get_session()\n        async with sess:\n            query = sess.select.from_(User)  # query is instance of SelectQuery\n            # alternatively, but not recommended\n            query = sess.select(User)\n            \n    However, it is possible to create this class manually:\n    \n    .. code-block:: python3\n\n        query = SelectQuery(db.get_session()\n        query.set_table(User)\n        query.add_condition(User.id == 2)\n        user = await query.first()\n        \n    '

    def __init__(self, session):
        super().__init__(session)
        self.table = None
        self.conditions = []
        self.row_limit = None
        self.row_offset = None
        self.orderer = None

    def __call__(self, table):
        return self.from_(table)

    def __aiter__(self):
        return ResultGenerator(q=self)

    def _get_joins_for_table(self, parent: 'md_relationship.Relationship', table: 'md_table.Table', seen: list=None):
        """
        Gets the foreign joins for a table.
        """
        if seen is None:
            seen = [
             table]
        foreign_tables = []
        joins = []
        for relationship in table.iter_relationships():
            if relationship.load_type != 'joined':
                pass
            else:
                if relationship.foreign_table in seen:
                    pass
                else:
                    foreign_table = relationship.foreign_table
                    foreign_tables.append(foreign_table)
                    joins.append(relationship._get_join_query(parent))

        return (
         foreign_tables, joins)

    def _recursive_get_table_joins(self, parent: 'md_relationship.Relationship', table: 'md_table.Table', seen: list=None):
        """
        Recursively loads the joins for a table.

        :param parent: The parent relationship this table is being loaded from, or None if it was             loaded directly.
        :param table: The table to get joins for.
        :param seen: A list of tables that have already been seen and should not be re-joined.
        """
        if seen is None:
            seen = [
             table]
        else:
            if table in seen:
                return ([], [])
        foreign_tables, joins = self._get_joins_for_table(parent, table, seen=seen)
        for relationship in table.iter_relationships():
            if relationship.load_type != 'joined':
                pass
            else:
                if relationship.foreign_table in seen:
                    pass
                else:
                    f, j = self._recursive_get_table_joins(relationship, (relationship.foreign_table),
                      seen=seen)
                    seen.append(relationship.foreign_table)
                    (foreign_tables.extend(f), joins.extend(j))

        return (
         foreign_tables, joins)

    def get_required_join_paths(self):
        """
        Gets the required join paths for this query.
        """
        return self._recursive_get_table_joins(None, (self.table), seen=None)

    def generate_sql(self) -> typing.Tuple[(str, dict)]:
        """
        Generates the SQL for this query. 
        """
        counter = itertools.count()
        foreign_tables, joins = self.get_required_join_paths()
        selected_columns = self.table.iter_columns()
        column_names = []
        for table in itertools.chain([self.table], foreign_tables):
            for column in table.iter_columns():
                a = column.alias_name(table=table, quoted=True)
                column_names.append('{} AS {}'.format(column.quoted_fullname_with_table(table), a))

        fmt = 'SELECT {} FROM {} '.format(', '.join(column_names), self.table.__quoted_name__)
        del selected_columns
        params = {}
        c_sql = []
        for condition in self.conditions:
            response = condition.generate_sql(self.session.bind.emit_param, counter)
            params.update(response.parameters)
            c_sql.append(response.sql)

        fmt += ' '.join(joins)
        if c_sql:
            fmt += ' WHERE {}'.format(' AND '.join(c_sql))
        if self.orderer is not None:
            res = self.orderer.generate_sql(self.session.bind.emit_param, counter)
            fmt += ' ORDER BY {}'.format(res.sql)
        if self.row_limit is not None:
            fmt += ' LIMIT {}'.format(self.row_limit)
        if self.row_offset is not None:
            fmt += ' OFFSET {}'.format(self.row_offset)
        return (fmt, params)

    async def first(self) -> 'md_table.Table':
        """
        Gets the first result that matches from this query.
        
        :return: A :class:`.Table` instance representing the first item, or None if no item matched.
        """
        gen = await self.session.run_select_query(self)
        row = await gen.next()
        if row is not None:
            return row

    async def all(self) -> 'ResultGenerator':
        """
        Gets all results that match from this query.
        
        :return: A :class:`.ResultGenerator` that can be iterated over.
        """
        return await self.session.run_select_query(self)

    async def run(self):
        return await self.all()

    def map_columns(self, results: typing.Mapping[(str, typing.Any)]) -> 'md_table.Table':
        """
        Maps columns in a result row to a :class:`.Table` instance object.
        
        :param results: A single row of results from the query cursor.
        :return: A new :class:`.Table` instance that represents the row returned.
        """
        mapping = {column.alias_name((self.table), quoted=False):column for column in self.table.iter_columns()}
        row_expando = {}
        relation_data = {}
        for colname in results.keys():
            if colname in mapping:
                column = mapping[colname]
                row_expando[column.name] = results[colname]
            else:
                relation_data[colname] = results[colname]

        row = self.table._internal_from_row(row_expando, existed=True)
        for column in self.table.iter_columns():
            val = row.get_column_value(column, return_default=False)
            if val is not NO_VALUE:
                row._previous_values[column] = val

        md_inspection._set_mangled(row, 'existed', True)
        row._session = self.session
        row._update_relationships(relation_data)
        return row

    def map_many(self, *rows: typing.Mapping[(str, typing.Any)]):
        """
        Maps many records to one row.
        
        This will group the records by the primary key of the main query table, then add additional
        columns as appropriate.
        """
        first_row = rows[0]
        tbl_row = self.map_columns(first_row)
        for runon_row in rows[1:]:
            tbl_row._update_relationships(runon_row)

        return tbl_row

    def from_(self, tbl) -> 'SelectQuery':
        """
        Sets the table this query is selecting from.
        
        :param tbl: The :class:`.Table` object to select. 
        :return: This query.
        """
        self.set_table(tbl)
        return self

    def where(self, *conditions: 'md_operators.BaseOperator') -> 'SelectQuery':
        """
        Adds a WHERE clause to the query. This is a shortcut for :meth:`.SelectQuery.add_condition`.
        
        .. code-block:: python3

            sess.select.from_(User).where(User.id == 1)
        
        :param conditions: The conditions to use for this WHERE clause.
        :return: This query.
        """
        for condition in conditions:
            self.add_condition(condition)

        return self

    def limit(self, row_limit: int) -> 'SelectQuery':
        """
        Sets a limit of the number of rows that can be returned from this query.
        
        :param row_limit: The maximum number of rows to return. 
        :return: This query.
        """
        self.row_limit = row_limit
        return self

    def offset(self, offset: int) -> 'SelectQuery':
        """
        Sets the offset of rows to start returning results from/
        
        :param offset: The row offset. 
        :return: This query.
        """
        self.row_offset = offset
        return self

    def order_by(self, *col: 'typing.Union[md_column.Column, md_operators.Sorter]', sort_order: str='asc'):
        """
        Sets the order by clause for this query.
        
        The argument provided can either be a :class:`.Column`, or a :class:`.Sorter` which is 
        provided by :meth:`.Column.asc` / :meth:`.Column.desc`. By default, ``asc`` is used when
        passing a column. 
        """
        if not col:
            raise TypeError('Must provide at least one item to order with')
        elif len(col) == 1:
            if isinstance(col[0], md_operators.Sorter):
                self.orderer = col[0]
        else:
            if sort_order == 'asc':
                self.orderer = (md_operators.AscSorter)(*col)
            else:
                if sort_order == 'desc':
                    self.orderer = (md_operators.DescSorter)(*col)
                else:
                    raise TypeError('Unknown sort order {}'.format(sort_order))
        return self

    def set_table(self, tbl) -> 'SelectQuery':
        """
        Sets the table to query on.
        
        :param tbl: The :class:`.Table` object to set. 
        :return: This query.
        """
        self.table = tbl
        return self

    def add_condition(self, condition: 'md_operators.BaseOperator') -> 'SelectQuery':
        """
        Adds a condition to the query/
        
        :param condition: The :class:`.BaseOperator` to add.
        :return: This query.
        """
        self.conditions.append(condition)
        return self


class InsertQuery(BaseQuery):
    __doc__ = '\n    Represents an INSERT query.\n    '

    def __init__(self, sess):
        super().__init__(sess)
        self.rows_to_insert = []

    def __await__(self):
        return self.run().__await__()

    async def run(self) -> 'typing.List[md_table.Table]':
        """
        Runs this query.
        
        :return: A list of inserted :class:`.md_table.Table`.
        """
        return await self.session.run_insert_query(self)

    def rows(self, *rows: 'md_table.Table') -> 'InsertQuery':
        """
        Adds a set of rows to the query.
        
        :param rows: The rows to insert. 
        :return: This query.
        """
        for row in rows:
            self.add_row(row)

        return self

    def add_row(self, row: 'md_table.Table') -> 'InsertQuery':
        """
        Adds a row to this query, allowing it to be executed later.
        
        :param row: The :class:`.Table` instance to use for this query.
        :return: This query.
        """
        self.rows_to_insert.append(row)
        return self

    def generate_sql(self) -> typing.List[typing.Tuple[(str, tuple)]]:
        """
        Generates the SQL statements for this insert query.
        
        This will return a list of two-item tuples to execute: 
            - The SQL query+params to emit to actually insert the row
        """
        queries = []
        counter = itertools.count()

        def emit():
            return 'param_{}'.format(next(counter))

        for row in self.rows_to_insert:
            query, params = row._get_insert_sql(emit, self.session)
            queries.append((query, params))

        return queries


class BulkQuery(BaseQuery, metaclass=abc.ABCMeta):
    __doc__ = '\n    Represents a **bulk query**.\n\n    This allows adding conditionals to the query.\n    '

    def __init__(self, sess):
        super().__init__(sess)
        self._table = None
        self.conditions = []

    def __call__(self, *args, **kwargs):
        return (self.table)(*args, **kwargs)

    def __await__(self):
        return self.run().__await__()

    def table(self, table: 'typing.Type[md_table.Table]'):
        """
        Sets the table for this query.
        """
        self._table = table
        return self

    def where(self, *conditions: 'md_operators.ComparisonOp'):
        """
        Sets the conditions for this query.
        """
        self.conditions.extend(conditions)
        return self

    def set_table(self, table: 'typing.Type[md_table.Table]'):
        """
        Sets a table on this query.
        """
        self._table = table

    def add_condition(self, condition: 'md_operators.BaseOperator'):
        """
        Adds a condition to this query.
        """
        self.conditions.append(condition)


class BulkUpdateQuery(BulkQuery):
    __doc__ = '\n    Represents a **bulk update query**. This updates many rows based on certain criteria.\n\n    .. code-block:: python3\n\n        query = BulkUpdateQuery(session)\n\n        # style 1: manual\n        query.set_table(User)\n        query.add_condition(User.xp < 300)\n        # add on a value\n        query.set_update(User.xp + 100)\n        # or set a value\n        query.set_update(User.xp.set(300))\n        await query.run()\n\n        # style 2: builder\n        await query.table(User).where(User.xp < 300).set(User.xp + 100).run()\n        await query.table(User).where(User.xp < 300).set(User.xp, 300).run()\n\n    '

    def __init__(self, sess):
        super().__init__(sess)
        self.setting = None

    def set(self, setter, value: typing.Any=None):
        """
        Sets a column in this query.
        """
        if value is not None:
            setter = md_operators.ValueSetter(setter, value)
        self.setting = setter
        return self

    def set_update(self, update):
        """
        Sets the update for this query.
        """
        self.setting = update

    def generate_sql(self):
        """
        Generates the SQL for this query.
        """
        query = 'UPDATE {} SET '.format(self._table.__quoted_name__)
        counter = itertools.count()
        params = {}
        response = self.setting.generate_sql(self.session.bind.emit_param, counter)
        params.update(response.parameters)
        query += response.sql
        c_sql = []
        for condition in self.conditions:
            res = condition.generate_sql(self.session.bind.emit_param, counter)
            params.update(res.parameters)
            c_sql.append(res.sql)

        query += ' WHERE ' + ' AND '.join(c_sql)
        return (
         query, params)

    async def run(self):
        return await self.session.run_update_query(self)


class BulkDeleteQuery(BulkQuery):
    __doc__ = '\n    Represents a **bulk delete query**. This deletes many rows based on criteria.\n\n    .. code-block:: python3\n\n        query = BulkDeleteQuery(session)\n\n        # style 1: manual\n        query.set_table(User)\n        query.add_condition(User.xp < 300)\n        await query.run()\n\n        # style 2: builder\n        await query.table(User).where(User.xp < 300).run()\n        await query.table(User).where(User.xp < 300).run()\n    '

    def generate_sql(self):
        query = 'DELETE FROM {} '.format(self._table.__quoted_name__)
        counter = itertools.count()
        params = {}
        c_sql = []
        for condition in self.conditions:
            res = condition.generate_sql(self.session.bind.emit_param, counter)
            params.update(res.parameters)
            c_sql.append(res.sql)

        query += ' WHERE ' + ' AND '.join(c_sql)
        return (query, params)

    async def run(self):
        return await self.session.run_delete_query(self)


class RowUpdateQuery(BaseQuery):
    __doc__ = '\n    Represents a **row update query**. This is **NOT** a bulk update query - it is used for updating\n    specific rows.\n    '

    def __init__(self, sess):
        super().__init__(sess)
        self.rows_to_update = []

    def __await__(self):
        return self.run().__await__()

    async def run(self):
        """
        Executes this query.
        """
        return await self.session.run_update_query(self)

    def rows(self, *rows: 'md_table.Table') -> 'RowUpdateQuery':
        """
        Adds a set of rows to the query.

        :param rows: The rows to insert. 
        :return: This query.
        """
        for row in rows:
            self.add_row(row)

        return self

    def add_row(self, row: 'md_table.Table') -> 'RowUpdateQuery':
        """
        Adds a row to this query, allowing it to be executed later.

        :param row: The :class:`.Table` instance to use for this query.
        :return: This query.
        """
        self.rows_to_update.append(row)
        return self

    def generate_sql(self) -> typing.List[typing.Tuple[(str, tuple)]]:
        """
        Generates the SQL statements for this row update query.
        
        This will return a list of two-item tuples to execute: 
        
            - The SQL query+params to emit to actually insert the row
        """
        queries = []
        counter = itertools.count()

        def emit():
            return 'param_{}'.format(next(counter))

        for row in self.rows_to_update:
            queries.append(row._get_update_sql(emit, self.session))

        return queries


class RowDeleteQuery(BaseQuery):
    __doc__ = '\n    Represents a row deletion query. This is **NOT** a bulk delete query - it is used for deleting\n    specific rows.\n    '

    def __init__(self, sess):
        super().__init__(sess)
        self.rows_to_delete = []

    def rows(self, *rows: 'md_table.Table') -> 'RowDeleteQuery':
        """
        Adds a set of rows to the query.

        :param rows: The rows to insert. 
        :return: This query.
        """
        for row in rows:
            self.add_row(row)

        return self

    def add_row(self, row: 'md_table.Table'):
        """
        Adds a row to this query.
        
        :param row: The :class:`.Table` instance  
        :return: 
        """
        self.rows_to_delete.append(row)

    def generate_sql(self) -> typing.List[typing.Tuple[(str, tuple)]]:
        """
        Generates the SQL statements for this row delete query.

        This will return a list of two-item tuples to execute: 
        
            - The SQL query+params to emit to actually insert the row
        """
        queries = []
        counter = itertools.count()

        def emit():
            return 'param_{}'.format(next(counter))

        for row in self.rows_to_delete:
            queries.append(row._get_delete_sql(emit, self.session))

        return queries

    async def run(self):
        return await self.session.run_delete_query(self)