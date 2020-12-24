# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/bdgt/storage/database.py
# Compiled at: 2014-10-31 03:15:09
import logging, os
from contextlib import contextmanager
from alembic.config import Config
from alembic import command
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
_log = logging.getLogger(__name__)
Base = declarative_base()
session_factory = sessionmaker()
Session = scoped_session(session_factory)

def open_database(url):
    engine = create_engine(url, echo=False)
    Session.configure(bind=engine)
    with open(os.devnull, 'w') as (devnull):
        alembic_cfg = Config('alembic.ini', stdout=devnull)
        alembic_cfg.set_main_option('sqlalchemy.url', url)
        if os.path.exists(url[10:]):
            _log.info('Opening existing database')
            if command.current(alembic_cfg) != 'head':
                _log.info('Migrating database to latest version')
                command.upgrade(alembic_cfg, 'head')
        else:
            _log.info('Creating new database')
            import bdgt.models
            Base.metadata.create_all(engine)
            command.stamp(alembic_cfg, 'head')


@contextmanager
def session_scope():
    """Provide a transactional scope around a series of operations."""
    session = Session()
    try:
        yield session
        session.commit()
    except:
        session.rollback()
        raise