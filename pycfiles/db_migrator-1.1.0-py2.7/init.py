# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/dbmigrator/commands/init.py
# Compiled at: 2017-10-27 09:34:32
"""Initialize schema migrations table."""
from .. import logger, utils
__all__ = ('cli_loader', )

@utils.with_cursor
def cli_command(cursor, migrations_directory='', version=None, **kwargs):
    cursor.execute("        SELECT 1 FROM information_schema.tables\n        WHERE table_name = 'schema_migrations'")
    table_exists = cursor.fetchone()
    if table_exists:
        logger.info('Schema migrations already initialized.')
        return
    else:
        cursor.execute('        CREATE TABLE schema_migrations (\n            version TEXT NOT NULL,\n            applied TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP\n        )')
        versions = []
        if version is None:
            timestamp = utils.timestamp()
        else:
            timestamp = str(version)
        for version, name in utils.get_migrations(migrations_directory):
            if version <= timestamp:
                versions.append((version,))

        cursor.executemany('        INSERT INTO schema_migrations VALUES (%s)\n        ', versions)
        logger.info('Schema migrations initialized.')
        return


def cli_loader(parser):
    parser.add_argument('--version', type=int, help='Set the schema version to VERSION, default current timestamp')
    return cli_command