# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/asyncpg_migrate/engine/downgrade.py
# Compiled at: 2020-01-13 09:51:39
# Size of source mod 2**32: 3379 bytes
import asyncio, typing as t, asyncpg
from loguru import logger
from asyncpg_migrate import loader
from asyncpg_migrate import model
from asyncpg_migrate.engine import migration

async def run(config: model.Config, target_revision: t.Union[(str, int)], connection: asyncpg.Connection) -> t.Optional[model.Revision]:
    logger.info('Downgrading to revision {target_revision} has been triggered',
      target_revision=target_revision)
    await migration.create_table(connection)
    migrations = loader.load_migrations(config)
    if not migrations:
        logger.info('There are no migrations scripts, skipping')
        return
    elif str(target_revision).lower() == 'head':
        raise ValueError('Cannot downgrade using "head"')
    else:
        to_revision = 1 if str(target_revision).lower() == 'base' else int(target_revision)
    maybe_db_revision = await migration.latest_revision(connection)
    if maybe_db_revision is None:
        logger.debug('No migration has ever happened, skipping...')
        return
    if maybe_db_revision == 0:
        logger.debug('Dowgraded everything there could have been migrated, skipping...')
        return
    db_revision = maybe_db_revision
    to_revision = 1 if abs(to_revision) == 0 else to_revision
    if to_revision > 0:
        if to_revision > len(migrations):
            logger.error('Cannot downgrade further than I know scripts for')
            return
        else:
            previous_db_revision = db_revision - (abs(to_revision) - 1)
            if previous_db_revision <= 0:
                to_revision = 1
            else:
                to_revision = previous_db_revision
    elif db_revision == 1:
        migrations_to_apply = migrations.slice(start=1, end=1)
    else:
        migrations_to_apply = migrations.slice(start=to_revision, end=db_revision)
    logger.debug(f"Applying migrations {sorted((migrations_to_apply.keys()), reverse=True)}")
    async with connection.transaction():
        try:
            for mig in migrations_to_apply.downgrade_iterator():
                logger.debug(f"Applying {mig.revision}/{mig.label}")
                await mig.downgrade(connection)
                await migration.save(migration=mig,
                  direction=(model.MigrationDir.DOWN),
                  connection=connection)
                await asyncio.sleep(1)
                last_completed_revision = mig.revision - 1

            logger.info('Upgraded did manage to finish at {last_completed_revision} revision',
              last_completed_revision=last_completed_revision)
            return model.Revision(last_completed_revision)
        except Exception as ex:
            try:
                logger.exception('Failed to downgrade...')
                raise RuntimeError(str(ex))
            finally:
                ex = None
                del ex