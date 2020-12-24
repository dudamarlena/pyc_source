# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/asyncpg_migrate/engine/migration.py
# Compiled at: 2020-01-13 09:51:39
# Size of source mod 2**32: 4727 bytes
import datetime as dt, functools, typing as t, asyncpg, asyncpg.exceptions
from loguru import logger
from asyncpg_migrate import constants
from asyncpg_migrate import model
MT = t.TypeVar('MT')
A_T = t.TypeVar('A_T')
K_T = t.TypeVar('K_T')

class MigrationTableMissing(Exception):
    pass


class MigrationProcessingError(Exception):
    pass


def error_trap(func: t.Callable[(..., t.Coroutine[(t.Any, t.Any, MT)])], *args: A_T, **kwargs: K_T) -> t.Callable[(..., t.Coroutine[(t.Any, t.Any, MT)])]:

    @functools.wraps(func)
    async def wrapper(*args, **kwargs):
        try:
            return await func(*args, **kwargs)
        except asyncpg.exceptions.UndefinedTableError as ex:
            try:
                logger.exception('Migration table is gone, you need to run migrations first')
                raise MigrationTableMissing() from ex
            finally:
                ex = None
                del ex

        except Exception as ex:
            try:
                logger.exception('Unknown error occurred')
                raise MigrationProcessingError() from ex
            finally:
                ex = None
                del ex

    return wrapper


@error_trap
async def latest_revision(connection: asyncpg.Connection, table_schema: str=constants.MIGRATIONS_SCHEMA, table_name: str=constants.MIGRATIONS_TABLE) -> t.Optional[model.Revision]:
    await connection.reload_schema_state()
    val = await connection.fetchval('\n            select revision from {table_schema}.{table_name} order\n            by timestamp desc limit 1;\n        '.format(table_schema=table_schema,
      table_name=table_name))
    if val is not None:
        return model.Revision(val)


async def create_table(connection: asyncpg.Connection, table_schema: str=constants.MIGRATIONS_SCHEMA, table_name: str=constants.MIGRATIONS_TABLE) -> None:
    logger.opt(lazy=True).debug('Creating migrations table {table_schema}.{table_name}',
      table_name=(lambda : table_name),
      table_schema=(lambda : table_schema))
    await connection.reload_schema_state()
    async with connection.transaction():
        await connection.execute("\n            do $$ begin\n                create type {table_schema}.{table_name}_direction as enum (\n                    '{migration_up}',\n                    '{migration_down}'\n                );\n            exception\n                when duplicate_object then null;\n            end $$;\n\n            create table if not exists {table_schema}.{table_name} (\n                revision integer not null,\n                label text not null,\n                timestamp timestamp not null,\n                direction {table_schema}.{table_name}_direction not null,\n\n                check(revision >= 0)\n            );\n            ".format(table_schema=table_schema,
          table_name=table_name,
          migration_up=(model.MigrationDir.UP),
          migration_down=(model.MigrationDir.DOWN)))


@error_trap
async def save(migration: model.Migration, direction: model.MigrationDir, connection: asyncpg.Connection, table_schema: str=constants.MIGRATIONS_SCHEMA, table_name: str=constants.MIGRATIONS_TABLE) -> None:
    await connection.execute(f"insert into {table_schema}.{table_name} (revision, label, timestamp, direction) values ($1, $2, $3, $4)", migration.revision if direction == model.MigrationDir.UP else migration.revision - 1, migration.label, dt.datetime.today(), direction)


@error_trap
async def list(connection: asyncpg.Connection, table_schema: str=constants.MIGRATIONS_SCHEMA, table_name: str=constants.MIGRATIONS_TABLE) -> model.MigrationHistory:
    logger.debug('Getting a history of migrations')
    history = model.MigrationHistory()
    await connection.reload_schema_state()
    async with connection.transaction():
        async for record in connection.cursor('\n                select revision, label, timestamp, direction from\n                    {table_schema}.{table_name}\n                    order by timestamp asc;\n                '.format(table_schema=table_schema,
          table_name=table_name)):
            history.append(model.MigrationHistoryEntry(revision=(model.Revision(record['revision'])),
              label=(record['label']),
              timestamp=(record['timestamp']),
              direction=(model.MigrationDir(record['direction']))))

    return history