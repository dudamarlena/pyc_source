# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/dbmigrator/commands/generate.py
# Compiled at: 2017-10-27 09:34:32
"""Generate a migration script in the migrations directory."""
import os
from ..utils import timestamp
from .. import logger
__all__ = ('cli_loader', )

def cli_command(migration_name='', **kwargs):
    filename = ('{}_{}.py').format(timestamp(), migration_name)
    directory = kwargs['migrations_directory']
    if not directory:
        raise Exception('migrations directory undefined')
    if len(directory) > 1:
        raise Exception('more than one migrations directory specified')
    directory = directory[0]
    path = os.path.join(directory, filename)
    if not os.path.isdir(directory):
        os.makedirs(directory)
    with open(path, 'w') as (f):
        f.write('# -*- coding: utf-8 -*-\n\n\n# Uncomment should_run if this is a repeat migration\n# def should_run(cursor):\n#     # TODO return True if migration should run\n\n\ndef up(cursor):\n    # TODO migration code\n    pass\n\n    # if a super user database connection is needed\n    # from dbmigrator import super_user\n    # with super_user() as super_cursor:\n    #     pass\n\n\ndef down(cursor):\n    # TODO rollback code\n    pass\n')
    logger.info(('Generated migration script "{}"').format(path))


def cli_loader(parser):
    parser.add_argument('migration_name')
    return cli_command