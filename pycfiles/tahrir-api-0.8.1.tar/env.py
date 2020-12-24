# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: alembic/env.py
# Compiled at: 2016-04-21 17:38:50
from __future__ import with_statement
from alembic import context
from sqlalchemy import engine_from_config, pool
from logging.config import fileConfig
import sqlalchemy as sa
config = context.config
fileConfig(config.config_file_name)
from tahrir_api import model
target_metadata = model.DeclarativeBase.metadata

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
    engine = engine_from_config(config.get_section(config.config_ini_section), prefix='sqlalchemy.', poolclass=pool.NullPool)
    connection = engine.connect()
    context.configure(connection=connection, target_metadata=target_metadata)
    trans = connection.begin()
    try:
        try:
            with context.begin_transaction():
                context.run_migrations()
                trans.commit()
        except sa.exc.OperationalError as e:
            print 'SQLite does not allow one of these operations. Rolling back.'
            print 'The exception was:'
            print repr(e)
            trans.rollback()

    finally:
        connection.close()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()