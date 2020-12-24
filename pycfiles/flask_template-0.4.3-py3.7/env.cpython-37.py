# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.13-x86_64/egg/flask_template/templates/simple/migrations/env.py
# Compiled at: 2020-03-11 03:42:34
# Size of source mod 2**32: 3826 bytes
from __future__ import with_statement
from alembic import context
from sqlalchemy import engine_from_config, pool
from logging.config import fileConfig
import logging
from flask import current_app
config = context.config
fileConfig(config.config_file_name)
logger = logging.getLogger('alembic.env')
config.set_main_option('sqlalchemy.url', current_app.config.get('SQLALCHEMY_DATABASE_URI'))
target_metadata = current_app.extensions['migrate'].db.metadata

def exclude_tables_from_config(config_):
    tables_ = config_.get('tables', None)
    if tables_ is not None:
        return tables_.split(',')


exclude_tables = exclude_tables_from_config(config.get_section('alembic:exclude'))

def include_tables_from_config(config_):
    tables_ = config_.get('tables', None)
    if tables_ is not None:
        return tables_.split(',')


include_tables = include_tables_from_config(config.get_section('alembic:include'))

def include_object(object, name, type_, reflected, compare_to):
    if type_ == 'table':
        if exclude_tables is not None:
            if name in exclude_tables:
                return False
        if include_tables is None:
            return True
        if name not in include_tables:
            return False
        return True
    return True


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
    context.configure(url=url, include_object=include_object)
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

    engine = engine_from_config((config.get_section(config.config_ini_section)), prefix='sqlalchemy.',
      poolclass=(pool.NullPool))
    connection = engine.connect()
    (context.configure)(connection=connection, target_metadata=target_metadata, 
     process_revision_directives=process_revision_directives, 
     include_object=include_object, **current_app.extensions['migrate'].configure_args)
    try:
        with context.begin_transaction():
            context.run_migrations()
    finally:
        connection.close()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()