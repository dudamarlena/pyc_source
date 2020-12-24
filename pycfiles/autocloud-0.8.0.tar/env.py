# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: alembic/env.py
# Compiled at: 2016-06-27 09:41:23
from __future__ import with_statement
from alembic import context
from sqlalchemy import engine_from_config, pool
from logging.config import fileConfig
import os, sys
sys.path.append(os.getcwd())
config = context.config
fileConfig(config.config_file_name)
from autocloud.models import Base
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
    from autoclould import SQLALCHEMY_URI
    url = SQLALCHEMY_URI
    context.configure(url=url, target_metadata=target_metadata, literal_binds=True)
    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online():
    """Run migrations in 'online' mode.

    In this scenario we need to create an Engine
    and associate a connection with the context.

    """
    alembic_config = config.get_section(config.config_ini_section)
    from autocloud import SQLALCHEMY_URI
    alembic_config['sqlalchemy.url'] = SQLALCHEMY_URI
    alembic_config['include_schemas'] = True
    connectable = engine_from_config(alembic_config, prefix='sqlalchemy.', poolclass=pool.NullPool)
    with connectable.connect() as (connection):
        context.configure(connection=connection, target_metadata=target_metadata)
        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()