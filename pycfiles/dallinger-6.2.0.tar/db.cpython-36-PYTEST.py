# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/travis/build/Dallinger/Dallinger/dallinger/db.py
# Compiled at: 2020-04-24 19:15:49
# Size of source mod 2**32: 5709 bytes
"""Create a connection to the database."""
import builtins as @py_builtins, _pytest.assertion.rewrite as @pytest_ar
from contextlib import contextmanager
from functools import wraps
import logging, os, psycopg2, redis, sys, time, random
from psycopg2.extensions import TransactionRollbackError
from sqlalchemy import create_engine
from sqlalchemy import event
from sqlalchemy.orm import Session
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.exc import OperationalError
logger = logging.getLogger('dallinger.db')
db_url_default = 'postgresql://dallinger:dallinger@localhost/dallinger'
db_url = os.environ.get('DATABASE_URL', db_url_default)
engine = create_engine(db_url, pool_size=1000)
session_factory = sessionmaker(autocommit=False, autoflush=True, bind=engine)
session = scoped_session(session_factory)
Base = declarative_base()
Base.query = session.query_property()
redis_url = os.getenv('REDIS_URL', 'redis://localhost:6379')
redis_conn = redis.from_url(redis_url)
db_user_warning = '\n*********************************************************\n*********************************************************\n\n\nDallinger now requires a database user named "dallinger".\n\nRun:\n\n    createuser -P dallinger --createdb\n\nConsult the developer guide for more information.\n\n\n*********************************************************\n*********************************************************\n\n'

def check_connection():
    """Test that postgres is running and that we can connect using the
    configured URI.

    Raises a psycopg2.OperationalError on failure.
    """
    conn = psycopg2.connect(db_url)
    conn.close()


@contextmanager
def sessions_scope(local_session, commit=False):
    """Provide a transactional scope around a series of operations."""
    try:
        try:
            yield local_session
            if commit:
                local_session.commit()
                logger.debug('DB session auto-committed as requested')
        except Exception as e:
            logger.exception('Exception during scoped worker transaction, rolling back.')
            local_session.rollback()
            raise e

    finally:
        local_session.remove()
        logger.debug('Session complete, db session closed')


def scoped_session_decorator(func):
    """Manage contexts and add debugging to db sessions."""

    @wraps(func)
    def wrapper(*args, **kwargs):
        with sessions_scope(session):
            logger.debug('Running worker %s in scoped DB session', func.__name__)
            return func(*args, **kwargs)

    return wrapper


def init_db(drop_all=False, bind=engine):
    """Initialize the database, optionally dropping existing tables."""
    try:
        if drop_all:
            Base.metadata.drop_all(bind=bind)
        Base.metadata.create_all(bind=bind)
    except OperationalError as err:
        msg = 'password authentication failed for user "dallinger"'
        if msg in err.message:
            sys.stderr.write(db_user_warning)
        raise

    return session


def serialized(func):
    """Run a function within a db transaction using SERIALIZABLE isolation.

    With this isolation level, committing will fail if this transaction
    read data that was since modified by another transaction. So we need
    to handle that case and retry the transaction.
    """

    @wraps(func)
    def wrapper(*args, **kw):
        attempts = 100
        session.remove()
        while attempts > 0:
            try:
                try:
                    session.connection(execution_options={'isolation_level': 'SERIALIZABLE'})
                    result = func(*args, **kw)
                    session.commit()
                    return result
                except OperationalError as exc:
                    session.rollback()
                    if isinstance(exc.orig, TransactionRollbackError):
                        if attempts > 0:
                            attempts -= 1
                        else:
                            raise Exception('Could not commit serialized transaction after 100 attempts.')
                    else:
                        raise

            finally:
                session.remove()

            time.sleep(random.expovariate(0.5))

    return wrapper


@event.listens_for(Session, 'after_begin')
def after_begin(session, transaction, connection):
    session.info['outbox'] = []


@event.listens_for(Session, 'after_soft_rollback')
def after_soft_rollback(session, previous_transaction):
    session.info['outbox'] = []


def queue_message(channel, message):
    logger.debug('Enqueueing message to {}: {}'.format(channel, message))
    if 'outbox' not in session.info:
        session.info['outbox'] = []
    session.info['outbox'].append((channel, message))


@event.listens_for(Session, 'after_commit')
def after_commit(session):
    for channel, message in session.info.get('outbox', ()):
        logger.debug('Publishing message to {}: {}'.format(channel, message))
        redis_conn.publish(channel, message)