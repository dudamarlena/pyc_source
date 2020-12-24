# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/airflow/migrations/env.py
# Compiled at: 2019-09-11 03:47:34
# Size of source mod 2**32: 2811 bytes
from __future__ import with_statement
from alembic import context
from logging.config import fileConfig
from airflow import settings
from airflow import models
config = context.config
fileConfig((config.config_file_name), disable_existing_loggers=False)
target_metadata = models.base.Base.metadata
COMPARE_TYPE = False

def run_migrations_offline():
    """Run migrations in 'offline' mode.

    This configures the context with just a URL
    and not an Engine, though an Engine is acceptable
    here as well.  By skipping the Engine creation
    we don't even need a DBAPI to be available.

    Calls to context.execute() here emit the given string to the
    script output.

    """
    context.configure(url=(settings.SQL_ALCHEMY_CONN),
      target_metadata=target_metadata,
      literal_binds=True,
      compare_type=COMPARE_TYPE)
    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online():
    """Run migrations in 'online' mode.

    In this scenario we need to create an Engine
    and associate a connection with the context.

    """
    connectable = settings.engine
    with connectable.connect() as (connection):
        context.configure(connection=connection,
          target_metadata=target_metadata,
          compare_type=COMPARE_TYPE)
        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()