# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/mishmash/alembic/env.py
# Compiled at: 2019-12-04 00:39:14
# Size of source mod 2**32: 1950 bytes
from alembic import context
from sqlalchemy import engine_from_config, pool
import mishmash.orm
config = context.config
target_metadata = mishmash.orm.Base.metadata

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
    connectable = engine_from_config((config.get_section(config.config_ini_section)),
      prefix='sqlalchemy.',
      poolclass=(pool.NullPool))
    with connectable.connect() as (connection):
        context.configure(connection=connection,
          target_metadata=target_metadata,
          render_as_batch=True)
        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()