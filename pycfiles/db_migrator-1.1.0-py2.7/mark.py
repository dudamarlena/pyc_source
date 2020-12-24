# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/dbmigrator/commands/mark.py
# Compiled at: 2018-01-03 12:06:07
"""Mark a migration as completed or not completed."""
from .. import logger, utils
__all__ = ('cli_loader', )

@utils.with_cursor
def cli_command(cursor, migrations_directory='', migration_timestamps=None, completed=None, **kwargs):
    if completed is None:
        raise Exception('-t, -f or -d must be supplied.')
    migrations = {version:migration for version, _, migration in utils.get_migrations(migrations_directory, import_modules=True)}
    for migration_timestamp in migration_timestamps:
        migration = migrations.get(migration_timestamp)
        if migration is None:
            raise SystemExit(('Migration {} not found').format(migration_timestamp))
        utils.mark_migration(cursor, migration_timestamp, completed)
        if not completed:
            message = 'not been run and not deferred'
        elif completed == 'deferred':
            message = 'deferred'
        else:
            message = 'completed'
        logger.info(('Migration {} marked as {}').format(migration_timestamp, message))

    return


def cli_loader(parser):
    parser.add_argument('migration_timestamps', nargs='+')
    parser.add_argument('-t', action='store_const', const=True, dest='completed', default=None, help='Mark the migration as completed')
    parser.add_argument('-f', action='store_const', const=False, dest='completed', default=None, help='Mark the migration as not been run')
    parser.add_argument('-d', action='store_const', const='deferred', dest='completed', default=None, help='Mark the migration as deferred')
    return cli_command