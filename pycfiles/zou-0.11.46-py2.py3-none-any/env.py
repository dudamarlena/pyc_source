# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: zou/migrations/env.py
# Compiled at: 2018-06-05 05:58:44
from __future__ import with_statement
import sqlalchemy_utils
from alembic import context
from sqlalchemy import engine_from_config, pool
from logging.config import fileConfig
from flask import current_app
import sqlalchemy_utils, logging
config = context.config
fileConfig(config.config_file_name)
logger = logging.getLogger('alembic.env')
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
    context.configure(url=url)
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

    engine = engine_from_config(config.get_section(config.config_ini_section), prefix='sqlalchemy.', poolclass=pool.NullPool)
    connection = engine.connect()
    context.configure(connection=connection, target_metadata=target_metadata, process_revision_directives=process_revision_directives, render_item=render_item, **current_app.extensions['migrate'].configure_args)
    try:
        with context.begin_transaction():
            context.run_migrations()
    finally:
        connection.close()


def render_item(type_, obj, autogen_context):
    """Apply custom rendering for selected items."""
    if type_ == 'type' and isinstance(obj, sqlalchemy_utils.UUIDType):
        autogen_context.imports.add('import sqlalchemy_utils')
        autogen_context.imports.add('import uuid')
        return 'sqlalchemy_utils.UUIDType(binary=False), default=uuid.uuid4'
    return False


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()