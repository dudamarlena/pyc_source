# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/asyncqlio/orm/session.py
# Compiled at: 2017-11-29 06:02:28
# Size of source mod 2**32: 16118 bytes
import enum, functools, logging, typing, warnings
from asyncqlio import db as md_db
from asyncqlio.backends.base import BaseTransaction
from asyncqlio.exc import DatabaseException
from asyncqlio.orm import inspection as md_inspection, query as md_query
from asyncqlio.orm.schema import table as md_table
from asyncqlio.sentinels import NO_DEFAULT, NO_VALUE
logger = logging.getLogger(__name__)

class SessionState(enum.Enum):
    NOT_READY = 0
    READY = 1
    CLOSED = 2


def enforce_open(func):

    @functools.wraps(func)
    def wrapper(self, *args, **kwargs):
        if self._state is not SessionState.READY:
            raise RuntimeError('Session is not ready or closed')
        else:
            return func(self, *args, **kwargs)

    return wrapper


class Session(object):
    __doc__ = '\n    Sessions act as a temporary window into the database. They are responsible for creating queries,\n    inserting and updating rows, etc.\n    \n    Sessions are bound to a :class:`.DatabaseInterface` instance which they use to get a transaction \n    and execute queries in.\n    \n    .. code-block:: python3\n\n        # get a session from our db interface\n        sess = db.get_session()\n    '

    def __init__(self, bind: 'md_db.DatabaseInterface'):
        """
        :param bind: The :class:`.DatabaseInterface` instance we are bound to. 
        """
        self.bind = bind
        self._state = SessionState.NOT_READY
        self.transaction = None

    async def __aenter__(self) -> 'Session':
        await self.start()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        try:
            if exc_type is None:
                await self.commit()
            else:
                if exc_type != DatabaseException:
                    await self.rollback()
        finally:
            await self.close()

        return False

    def __del__(self):
        if self._state == SessionState.READY:
            warnings.warn('Session was destroyed without being closed!', stacklevel=2)

    @property
    def select(self) -> 'md_query.SelectQuery':
        """
        Creates a new SELECT query that can be built upon.
        
        :return: A new :class:`.SelectQuery`.
        """
        q = md_query.SelectQuery(self)
        return q

    @property
    def insert(self) -> 'md_query.InsertQuery':
        """
        Creates a new INSERT INTO query that can be built upon.
        
        :return: A new :class:`.InsertQuery`. 
        """
        return md_query.InsertQuery(self)

    @property
    def update(self) -> 'md_query.BulkUpdateQuery':
        """
        Creates a new bulk UPDATE query that can be built upon.

        :return: A new :class:`.BulkUpdateQuery`.
        """
        return md_query.BulkUpdateQuery(self)

    @property
    def delete(self) -> 'md_query.BulkDeleteQuery':
        """
        Creates a new bulk DELETE query that can be built upon.

        :return: A new :class:`.BulkDeleteQuery`.
        """
        return md_query.BulkDeleteQuery(self)

    async def start(self) -> 'Session':
        """
        Starts the session, acquiring a transaction connection which will be used to modify the DB.

        This **must** be called before using the session.  
        
        .. code-block:: python3

            sess = db.get_session()
            await sess.start()
        
        .. note::
            When using ``async with``, this is automatically called.
        """
        if self._state is not SessionState.NOT_READY:
            raise RuntimeError('Session must not be ready or closed')
        logger.debug('Acquiring new transaction, and beginning')
        self.transaction = self.bind.get_transaction()
        await self.transaction.begin()
        self._state = SessionState.READY
        return self

    @enforce_open
    async def checkpoint(self, checkpoint_name: str):
        """
        Sets a new checkpoint.

        :param checkpoint_name: The name of the checkpoint to use.
        """
        if not self.bind.dialect.has_checkpoints:
            raise NotImplementedError('The {} dialect has no checkpoints'.format(self.bind.dialect.__class__.__name__))
        return await self.transaction.create_savepoint(checkpoint_name)

    @enforce_open
    async def uncheckpoint(self, checkpoint_name: str):
        """
        Releases a checkpoint.

        :param checkpoint_name: The name of the checkpoint to release.
        """
        if not self.bind.dialect.has_checkpoints:
            raise NotImplementedError('The {} dialect has no checkpoints'.format(self.bind.dialect.__class__.__name__))
        return await self.transaction.release_savepoint(checkpoint_name)

    @enforce_open
    async def commit(self):
        """
        Commits the current session, running inserts/updates/deletes.
         
        This will **not** close the session; it can be re-used after a commit.
        """
        logger.debug('Committing transaction')
        await self.transaction.commit()
        return self

    @enforce_open
    async def rollback(self, checkpoint: str=None):
        """
        Rolls the current session back.  
        This is useful if an error occurs inside your code.
        
        :param checkpoint: The checkpoint to roll back to, if applicable. 
        """
        logger.debug('Rolling back session to checkpoint {}'.format(checkpoint))
        await self.transaction.rollback(checkpoint=checkpoint)
        return self

    @enforce_open
    async def close(self):
        """
        Closes the current session.
        
        .. warning::

            This will **NOT COMMIT ANY DATA**. Old data will die.
        """
        await self.transaction.close()
        self._state = SessionState.CLOSED
        del self.transaction

    @enforce_open
    async def fetch(self, sql: str, params=None):
        """
        Fetches a single row.
        """
        cur = await self.transaction.cursor(sql, params)
        next = await cur.fetch_row()
        await cur.close()
        return next

    @enforce_open
    async def execute(self, sql: str, params: typing.Union[(typing.Mapping[(str, typing.Any)], typing.Iterable[typing.Any])]=None):
        """
        Executes SQL inside the current session.
        
        This is part of the **low-level API.**
        
        :param sql: The SQL to execute.
        :param params: The parameters to use inside the query.
        """
        return await self.transaction.execute(sql, params)

    @enforce_open
    async def cursor(self, sql: str, params: typing.Union[(typing.Mapping[(str, typing.Any)], typing.Iterable[typing.Any])]=None):
        """
        Executes SQL inside the current session, and returns a new :class:`.BaseResultSet.`
        
        :param sql: The SQL to execute.
        :param params: The parameters to use inside the query.
        """
        return await self.transaction.cursor(sql, params)

    @enforce_open
    async def insert_now(self, row: 'md_table.Table') -> typing.Any:
        """
        Inserts a row NOW. 
        
        .. warning::
            This will only generate the INSERT statement for the row now.
            Only :meth:`.Session.commit` will actually commit the row to storage.
            
            Also, tables with auto-incrementing fields will only have their first field filled in
            outside of Postgres databases.
        
        :param row: The :class:`.Table` instance to insert.
        :return: The row, with primary key included.
        """
        q = md_query.InsertQuery(self)
        q.add_row(row)
        result = await self.run_insert_query(q)
        try:
            return result[0]
        except IndexError:
            return

    @enforce_open
    async def update_now(self, row: 'md_table.Table') -> 'md_table.Table':
        """
        Updates a row NOW. 

        .. warning::
            This will only generate the UPDATE statement for the row now.
            Only :meth:`.Session.commit` will actually commit the row to storage.

        :param row: The :class:`.Table` instance to update.
        :return: The :class:`.Table` instance that was updated.
        """
        q = md_query.RowUpdateQuery(self)
        q.add_row(row)
        await self.run_update_query(q)
        return row

    @enforce_open
    async def delete_now(self, row: 'md_table.Table') -> 'md_table.Table':
        """
        Deletes a row NOW.
        """
        q = md_query.RowDeleteQuery(self)
        q.add_row(row)
        await self.run_delete_query(q)
        return row

    async def run_select_query(self, query: 'md_query.SelectQuery'):
        """
        Executes a select query.
        
        .. warning::
            Unlike the other `run_*_query` methods, this method should not be used without a good
            reason; it creates a special class that is used for the query.
            
            Use :class:`.SelectQuery.first` or :class:`.SelectQuery.all`.
        
        :param query: The :class:`.SelectQuery` to use.
        :return: A :class:`._ResultGenerator` for this query.
        """
        gen = md_query.ResultGenerator(query)
        sql, params = query.generate_sql()
        cursor = await self.cursor(sql, params)
        gen._results = cursor
        return gen

    async def run_insert_query(self, query: 'md_query.InsertQuery'):
        """
        Executes an insert query.
        
        :param query: The :class:`.InsertQuery` to use.
        :return: The list of rows that were inserted.
        """
        queries = query.generate_sql()
        results = []
        for row, (sql, params) in zip(query.rows_to_insert, queries):
            if md_inspection._get_mangled(row, 'deleted'):
                raise RuntimeError("Row '{}' is marked as deleted".format(row))
            cur = await self.cursor(sql, params)
            returned_row = await cur.fetch_row()
            if self.bind.dialect.has_returns:
                for colname, value in returned_row.items():
                    column = row.table.get_column(colname)
                    if column is None:
                        pass
                    else:
                        row.store_column_value(column, value, track_history=False)
                    await cur.close()

            else:
                if sum(1 for x in row.table.iter_columns() if x.autoincrement) == 1:
                    lquery = 'SELECT {};'.format(self.bind.dialect.lastval_method)
                    cursor = await self.cursor(lquery)
                    async with cursor:
                        lval_row = await cursor.fetch_row()
                        value = list(lval_row.values())[0]
                    column = next(filter(lambda x: x.auto_increment, row.table.iter_columns()), None)
                    row.store_column_value(column, value)
                for column in row.table.iter_columns():
                    if column.default is not NO_DEFAULT and row.get_column_value(column, return_default=False) is NO_VALUE:
                        row.store_column_value(column, column.default)

                await cur.close()
            md_inspection._set_mangled(row, 'deleted', False)
            md_inspection._set_mangled(row, 'existed', True)
            results.append(row)

        return results

    async def run_update_query(self, query: 'md_query.BaseQuery'):
        """
        Executes an update query.
        
        :param query: The :class:`.RowUpdateQuery` or :class:`.BulkUpdateQuery` to execute. 
        """
        if isinstance(query, md_query.RowUpdateQuery):
            for row, (sql, params) in zip(query.rows_to_update, query.generate_sql()):
                if md_inspection._get_mangled(row, 'deleted'):
                    raise RuntimeError("Row '{}' is marked as deleted".format(row))
                if sql is None:
                    if params is None:
                        continue
                await self.execute(sql, params)
                row._previous_values = row._values

        else:
            if isinstance(query, md_query.BulkUpdateQuery):
                sql, params = query.generate_sql()
                await self.execute(sql, params)
            else:
                raise TypeError('Type {0.__class__.__name__} is not an update query'.format(query))
        return query

    async def run_delete_query(self, query: 'md_query.RowDeleteQuery'):
        """
        Executes a delete query.
        
        :param query: The :class:`.RowDeleteQuery` or :class:`.BulkDeleteQuery` to execute.  
        """
        if isinstance(query, md_query.RowDeleteQuery):
            for row, (sql, params) in zip(query.rows_to_delete, query.generate_sql()):
                if md_inspection._get_mangled(row, 'deleted'):
                    raise RuntimeError("Row '{}' is already marked as deleted".format(row))
                if sql is None:
                    if params is None:
                        continue
                await self.execute(sql, params)
                md_inspection._set_mangled(row, 'deleted', True)

        else:
            if isinstance(query, md_query.BulkDeleteQuery):
                sql, params = query.generate_sql()
                await self.execute(sql, params)
            else:
                raise TypeError('Type {0.__class__.__name__} is not a delete query'.format(query))
        return query

    async def add(self, row: 'md_table.Table') -> 'md_table.Table':
        """
        Adds a row to the current transaction. This will emit SQL that will generate an INSERT or 
        UPDATE statement, and then update the primary key of this row.
        
        .. warning::

            This will only generate the INSERT statement for the row now. Only
            :meth:`.Session.commit` will actually commit the row to storage.
    
        :param row: The :class:`.Table` instance object to add to the transaction.
        :return: The :class:`.Table` instance with primary key filled in, if applicable.
        """
        if md_inspection._get_mangled(row, 'existed'):
            return await self.update_now(row)
        else:
            return await self.insert_now(row)

    async def merge(self, row: 'md_table.Table') -> 'md_table.Table':
        """
        Merges a row with a row that already exists in the database.
        
        This should be used for rows that have a primary key, but were not returned from 
        :meth:`.Session.select`.
        
        :param row: The :class:`.Table` instance to merge. 
        :return: The :class:`.Table` instance once updated.
        """
        return await self.update_now(row)

    async def remove(self, row: 'md_table.Table') -> 'md_table.Table':
        """
        Removes a row from the database.

        :param row: The :class:`.Table` instance to remove.
        """
        return await self.delete_now(row)