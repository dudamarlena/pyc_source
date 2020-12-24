# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/meatpuppet/code/lspace/lspace/migrations/env.py
# Compiled at: 2019-06-11 18:56:47
# Size of source mod 2**32: 2833 bytes
from __future__ import with_statement
import logging
from sqlalchemy import engine_from_config
from sqlalchemy import pool
from alembic import context
config = context.config
logger = logging.getLogger('alembic.env')
from flask import current_app
config.set_main_option('sqlalchemy.url', current_app.config.get('SQLALCHEMY_DATABASE_URI'))
target_metadata = current_app.extensions['migrate'].db.metadata

def run_migrations_offline():
    """Run migrations in 'offline' mode.

    This configures the context with just a URL
    and not an Engine, though an Engine is acceptable
    here as well.  By skipping the Engine creation
    we don't even need a DBAPI to be available.

    Calls to context.execute() here emit the given string to the
    script output.

    """
    url = config.get_main_option('sqlalchemy.url')
    context.configure(url=url,
      target_metadata=target_metadata,
      literal_binds=True)
    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online():
    """Run migrations in 'online' mode.

    In this scenario we need to create an Engine
    and associate a connection with the context.

    """

    def process_revision_directives(context, revision, directives):
        if getattr(config.cmd_opts, 'autogenerate', False):
            script = directives[0]
            if script.upgrade_ops.is_empty():
                directives[:] = []
                logger.info('No changes in schema detected.')

    connectable = engine_from_config((config.get_section(config.config_ini_section)),
      prefix='sqlalchemy.',
      poolclass=(pool.NullPool))
    with connectable.connect() as (connection):
        (context.configure)(connection=connection, 
         target_metadata=target_metadata, 
         process_revision_directives=process_revision_directives, **current_app.extensions['migrate'].configure_args)
        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()