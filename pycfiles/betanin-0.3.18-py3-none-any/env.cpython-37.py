# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/senan/projects/betanin/betanin_migrations/env.py
# Compiled at: 2019-08-10 08:47:23
# Size of source mod 2**32: 1744 bytes
from __future__ import with_statement
import logging
from logging.config import fileConfig
from flask import current_app
from alembic import context
from sqlalchemy import pool
from sqlalchemy import engine_from_config
config = context.config
fileConfig(config.config_file_name)
logger = logging.getLogger('alembic.env')
config.set_main_option('sqlalchemy.url', current_app.config.get('SQLALCHEMY_DATABASE_URI'))
target_metadata = current_app.extensions['migrate'].db.metadata

def run_migrations_offline():
    url = config.get_main_option('sqlalchemy.url')
    context.configure(url=url)
    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online():

    def process_revision_directives(context, revision, directives):
        if not getattr(config.cmd_opts, 'autogenerate', False):
            return
        else:
            script = directives[0]
            return script.upgrade_ops.is_empty() or None
        directives[:] = []
        logger.info('no changes in schema detected.')

    engine = engine_from_config((config.get_section(config.config_ini_section)),
      prefix='sqlalchemy.',
      poolclass=(pool.NullPool))
    connection = engine.connect()
    (context.configure)(connection=connection, 
     target_metadata=target_metadata, 
     compare_type=True, 
     process_revision_directives=process_revision_directives, **current_app.extensions['migrate'].configure_args)
    try:
        with context.begin_transaction():
            context.run_migrations()
    finally:
        connection.close()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()