# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/jordansuchow/Dropbox/Berkeley/Projects/Current/Wallace/wallace/db.py
# Compiled at: 2016-07-28 05:24:16
"""Create a connection to the database."""
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy.ext.declarative import declarative_base
from contextlib import contextmanager
from functools import wraps
import logging, os
logger = logging.getLogger('wallace.db')
db_url_default = 'postgresql://postgres@localhost/wallace'
db_url = os.environ.get('DATABASE_URL', db_url_default)
engine = create_engine(db_url, pool_size=1000)
session = scoped_session(sessionmaker(autocommit=False, autoflush=True, bind=engine))
Base = declarative_base()
Base.query = session.query_property()

@contextmanager
def sessions_scope(local_session, commit=False):
    """Provide a transactional scope around a series of operations."""
    try:
        try:
            yield local_session
            if commit:
                local_session.commit()
                logger.debug('DB session auto-committed as requested')
        except:
            logger.exception('Exception during scoped worker transaction, rolling back.')
            local_session.rollback()
            raise

    finally:
        local_session.remove()
        logger.debug('Session complete, db session closed')


def scoped_session_decorator(func):
    """Manage contexts and add debugging to psiTurk sessions."""

    @wraps(func)
    def wrapper(*args, **kwargs):
        from wallace.db import session as wallace_session
        with sessions_scope(wallace_session) as (session):
            from psiturk.db import db_session as psi_session
            with sessions_scope(psi_session) as (session_psiturk):
                logger.debug('Running worker %s in scoped DB sessions', func.__name__)
                return func(*args, **kwargs)

    return wrapper


def init_db(drop_all=False):
    """Initialize the database, optionally dropping existing tables."""
    if drop_all:
        Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    return session