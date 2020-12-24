# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: alembic/env.py
# Compiled at: 2013-06-08 14:56:46
from __future__ import with_statement
from alembic import context
from sqlalchemy import engine_from_config, pool
from logging.config import fileConfig
import logging, sys
sys.path.insert(0, '.')
from yworklog.core import get_main_db
from yworklog import model
config = context.config
fileConfig(config.config_file_name)
log = logging.getLogger(__name__)
url = get_main_db()
model.init(url)
target_metadata = model.Base.metadata

def run_migrations_offline():
    """Run migrations in 'offline' mode.

    This configures the context with just a URL
    and not an Engine, though an Engine is acceptable
    here as well.  By skipping the Engine creation
    we don't even need a DBAPI to be available.

    Calls to context.execute() here emit the given string to the
    script output.

    """
    global url
    context.configure(url=url)
    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online():
    """Run migrations in 'online' mode.

    In this scenario we need to create an Engine
    and associate a connection with the context.

    """
    log.debug('%s %s', config, config.__class__)
    config.set_main_option('sqlalchemy.url', url)
    engine = engine_from_config(config.get_section(config.config_ini_section), prefix='sqlalchemy.', poolclass=pool.NullPool)
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