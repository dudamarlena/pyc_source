# uncompyle6 version 3.6.7
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.6-intel/egg/bonobo_sqlalchemy/writers.py
# Compiled at: 2018-07-15 06:26:26
# Size of source mod 2**32: 7333 bytes
import datetime, logging, traceback
from queue import Queue
from sqlalchemy import MetaData, Table, and_
from sqlalchemy.exc import OperationalError
from sqlalchemy.sql import select
from bonobo.config import Configurable, ContextProcessor, Option, Service, use_context, use_raw_input
from bonobo.errors import UnrecoverableError
from bonobo_sqlalchemy.constants import INSERT, UPDATE
from bonobo_sqlalchemy.errors import ProhibitedOperationError
logger = logging.getLogger(__name__)

@use_context
@use_raw_input
class InsertOrUpdate(Configurable):
    """InsertOrUpdate"""
    table_name = Option(str, positional=True)
    fetch_columns = Option(tuple, required=False, default=())
    insert_only_fields = Option(tuple, required=False, default=())
    discriminant = Option(tuple, required=False, default=('id', ))
    created_at_field = Option(str, required=False, default='created_at')
    updated_at_field = Option(str, required=False, default='updated_at')
    allowed_operations = Option(tuple, required=False, default=(
     INSERT,
     UPDATE))
    buffer_size = Option(int, required=False, default=1000)
    engine = Service('sqlalchemy.engine')

    @ContextProcessor
    def create_connection(self, context, *, engine):
        """
        This context processor creates an sqlalchemy connection for use during the lifetime of this transformation's
        execution.
        
        :param engine: 
        """
        try:
            connection = engine.connect()
        except OperationalError as exc:
            raise UnrecoverableError('Could not create SQLAlchemy connection: {}.'.format(str(exc).replace('\n', ''))) from exc

        with connection:
            yield connection

    @ContextProcessor
    def create_table(self, context, connection, *, engine):
        """SQLAlchemy table object, using metadata autoloading from database to avoid the need of column definitions."""
        yield Table(self.table_name, MetaData(), autoload=True, autoload_with=engine)

    @ContextProcessor
    def create_buffer(self, context, connection, table, *, engine):
        """
        This context processor creates a "buffer" of yet to be persisted elements, and commits the remaining elements
        when the transformation ends.
        
        :param engine: 
        :param connection: 
        """
        buffer = yield Queue()
        try:
            for row in self.commit(table, connection, buffer, force=True):
                context.send(row)

        except Exception as exc:
            logger.exception('Flush fail')
            raise UnrecoverableError('Flushing query buffer failed.') from exc

    def __call__(self, connection, table, buffer, context, row, engine):
        """
        Main transformation method, pushing a row to the "yet to be processed elements" queue and commiting if necessary.
        
        :param engine: 
        :param connection: 
        :param buffer: 
        :param row: 
        """
        buffer.put(row)
        yield from self.commit(table, connection, buffer)

    def commit(self, table, connection, buffer, force=False):
        if force or buffer.qsize() >= self.buffer_size:
            with connection.begin():
                while buffer.qsize() > 0:
                    try:
                        yield self.insert_or_update(table, connection, buffer.get())
                    except Exception as exc:
                        yield exc

    def insert_or_update(self, table, connection, row):
        """ Actual database load transformation logic, without the buffering / transaction logic. 
        """
        dbrow = self.find(connection, table, row)
        now = datetime.datetime.now()
        column_names = table.columns.keys()
        if self.updated_at_field in column_names:
            row[self.updated_at_field] = now
        if dbrow:
            if UPDATE not in self.allowed_operations:
                raise ProhibitedOperationError('UPDATE operations are not allowed by this transformation.')
            query = table.update().values(**{col:row.get(col) for col in self.get_columns_for(column_names, row, dbrow)}).where(and_(*(getattr(table.c, col) == row.get(col) for col in self.discriminant)))
        elif INSERT not in self.allowed_operations:
            raise ProhibitedOperationError('INSERT operations are not allowed by this transformation.')
        if self.created_at_field in column_names:
            row[self.created_at_field] = now
        else:
            if self.created_at_field in row:
                del row[self.created_at_field]
            query = table.insert().values(**{col:row.get(col) for col in self.get_columns_for(column_names, row)})
        try:
            connection.execute(query)
        except Exception:
            logger.exception('Rollback...')
            connection.rollback()
            raise

        if self.fetch_columns and len(self.fetch_columns):
            if not dbrow:
                dbrow = self.find(row)
            if not dbrow:
                raise ValueError('Could not find matching row after load.')
            for alias, column in self.fetch_columns.items():
                row[alias] = dbrow[column]

        return row

    def find(self, connection, table, row):
        sql = select([table]).where(and_(*(getattr(table.c, col) == row.get(col) for col in self.discriminant))).limit(1)
        row = connection.execute(sql).fetchone()
        if row:
            return dict(row)

    def get_columns_for(self, column_names, row, dbrow=None):
        """Retrieve list of table column names for which we have a value in given hash.

        """
        if dbrow:
            candidates = filter(lambda col: col not in self.insert_only_fields, column_names)
        else:
            candidates = column_names
        try:
            fields = row._fields
        except AttributeError as exc:
            fields = list(row.keys())

        return set(candidates).intersection(fields)

    def add_fetch_columns(self, *columns, **aliased_columns):
        self.fetch_columns = {**(self.fetch_columns), **aliased_columns}
        for column in columns:
            self.fetch_columns[column] = column