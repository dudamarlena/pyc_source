# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/asyncpg_migrate/engine/upgrade.py
# Compiled at: 2020-01-13 09:51:39
# Size of source mod 2**32: 3248 bytes
import asyncio, typing as t, asyncpg
from loguru import logger
from asyncpg_migrate import loader
from asyncpg_migrate import model
from asyncpg_migrate.engine import migration

async def run(config: model.Config, target_revision: t.Union[(str, int)], connection: asyncpg.Connection) -> t.Optional[model.Revision]:
    """Executes the UP migration.

    Algorithm:
    1. Check if everything is on order
    2. Ensure that migration table is created
    3. Get latest migration that has been applied from DB
    4. Compute the next migration from which to start new one
    5. Be happy :)
    """
    logger.info('Upgrade to revision {target_revision} has been triggered',
      target_revision=target_revision)
    await migration.create_table(connection)
    migrations = loader.load_migrations(config)
    if not migrations:
        logger.info('There are no migrations scripts, skipping')
        return
    if str(target_revision).lower() == 'base':
        raise ValueError('Cannot upgrade using "base"')
    else:
        logger.debug('Loaded {count} migrations scripts', count=(len(migrations)))
        to_revision = model.Revision.decode(target_revision, migrations.revisions())
        logger.debug('Decoded target revision is {rev}', rev=to_revision)
    maybe_db_revision = await migration.latest_revision(connection)
    if maybe_db_revision is None:
        start_from_db_revision = 1
        logger.debug('Looks like we will run migration for first time')
    else:
        if maybe_db_revision == to_revision:
            logger.debug(f"Already at {to_revision} (latest), skipping...")
            return
        start_from_db_revision = maybe_db_revision + 1
        if start_from_db_revision > to_revision:
            logger.error(f"Current revision is {maybe_db_revision} and you want to migrate to {to_revision}. Cannot go backward when you want me to go UP, sorry :(")
            return
    migrations_to_apply = migrations.slice(start=start_from_db_revision,
      end=to_revision)
    logger.debug(f"Applying migrations {migrations_to_apply.revisions()}")
    last_completed_revision = None
    async with connection.transaction():
        try:
            for mig in migrations_to_apply.upgrade_iterator():
                logger.debug(f"Applying {mig.revision}/{mig.label}")
                await mig.upgrade(connection)
                await migration.save(migration=mig,
                  direction=(model.MigrationDir.UP),
                  connection=connection)
                await asyncio.sleep(1)
                last_completed_revision = mig.revision

        except Exception as ex:
            try:
                logger.trace('Failed to upgrade...')
                raise RuntimeError(str(ex))
            finally:
                ex = None
                del ex

    logger.info('Upgraded did manage to finish at {last_completed_revision} revision',
      last_completed_revision=last_completed_revision)
    return last_completed_revision