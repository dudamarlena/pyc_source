# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/travis/build/universalcore/unicore.ask/unicore/ask/service/tests/../alembic/env.py
# Compiled at: 2015-03-13 10:41:44
from __future__ import with_statement
import os
from alembic import context
from alembic.config import Config
from sqlalchemy import engine_from_config, pool
from logging.config import fileConfig
config = context.config
pyramid_config_file = os.environ.get('PYRAMID_CONFIG_FILE', config.get_main_option('pyramid_config_file'))
pyramid_config = Config(pyramid_config_file)
fileConfig(config.config_file_name)
from unicore.ask.service.models import Base
target_metadata = Base.metadata

def run_migrations_offline():
    """Run migrations in 'offline' mode.

    This configures the context with just a URL
    and not an Engine, though an Engine is acceptable
    here as well.  By skipping the Engine creation
    we don't even need a DBAPI to be available.

    Calls to context.execute() here emit the given string to the
    script output.

    """
    url = pyramid_config.get_main_option('sqlalchemy.url')
    context.configure(url=url, target_metadata=target_metadata)
    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online():
    """Run migrations in 'online' mode.

    In this scenario we need to create an Engine
    and associate a connection with the context.

    """
    engine = engine_from_config(pyramid_config.get_section('app:unicore.ask.service'), prefix='sqlalchemy.', poolclass=pool.NullPool)
    connection = engine.connect()
    context.configure(connection=connection, target_metadata=target_metadata)
    try:
        with context.begin_transaction():
            context.run_migrations()
    finally:
        connection.close()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()