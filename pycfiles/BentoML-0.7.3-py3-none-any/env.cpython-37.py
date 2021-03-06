# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/chaoyuyang/workspace/BentoML/bentoml/migrations/env.py
# Compiled at: 2019-10-24 18:17:34
# Size of source mod 2**32: 1854 bytes
from sqlalchemy import engine_from_config
from sqlalchemy import pool
from alembic import context
config = context.config
target_metadata = None

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
      literal_binds=True,
      dialect_opts={'paramstyle': 'named'})
    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online():
    """Run migrations in 'online' mode.

    In this scenario we need to create an Engine
    and associate a connection with the context.

    """
    connectable = engine_from_config((config.get_section(config.config_ini_section)),
      prefix='sqlalchemy.',
      poolclass=(pool.NullPool))
    with connectable.connect() as (connection):
        context.configure(connection=connection, target_metadata=target_metadata)
        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()