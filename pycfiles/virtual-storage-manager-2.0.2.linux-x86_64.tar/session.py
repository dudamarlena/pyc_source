# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python2.7/dist-packages/vsm/db/sqlalchemy/session.py
# Compiled at: 2016-06-13 14:11:03
"""Session Handling for SQLAlchemy backend."""
import time
from sqlalchemy.exc import DisconnectionError, OperationalError
import sqlalchemy.interfaces, sqlalchemy.orm
from sqlalchemy.pool import NullPool, StaticPool
import vsm.exception, vsm.flags as flags
from vsm.openstack.common import log as logging
FLAGS = flags.FLAGS
LOG = logging.getLogger(__name__)
_ENGINE = None
_MAKER = None

def get_session(autocommit=True, expire_on_commit=False):
    """Return a SQLAlchemy session."""
    global _MAKER
    if _MAKER is None:
        engine = get_engine()
        _MAKER = get_maker(engine, autocommit, expire_on_commit)
    session = _MAKER()
    session.query = vsm.exception.wrap_db_error(session.query)
    session.flush = vsm.exception.wrap_db_error(session.flush)
    return session


def synchronous_switch_listener(dbapi_conn, connection_rec):
    """Switch sqlite connections to non-synchronous mode"""
    dbapi_conn.execute('PRAGMA synchronous = OFF')


def ping_listener(dbapi_conn, connection_rec, connection_proxy):
    """
    Ensures that MySQL connections checked out of the
    pool are alive.

    Borrowed from:
    http://groups.google.com/group/sqlalchemy/msg/a4ce563d802c929f
    """
    try:
        dbapi_conn.cursor().execute('select 1')
    except dbapi_conn.OperationalError as ex:
        if ex.args[0] in (2006, 2013, 2014, 2045, 2055):
            LOG.warn(_('Got mysql server has gone away: %s'), ex)
            raise DisconnectionError('Database server went away')
        else:
            raise


def is_db_connection_error(args):
    """Return True if error in connecting to db."""
    conn_err_codes = ('2002', '2003', '2006')
    for err_code in conn_err_codes:
        if args.find(err_code) != -1:
            return True

    return False


def get_engine():
    """Return a SQLAlchemy engine."""
    global _ENGINE
    if _ENGINE is None:
        connection_dict = sqlalchemy.engine.url.make_url(FLAGS.sql_connection)
        engine_args = {'pool_recycle': FLAGS.sql_idle_timeout, 
           'echo': False, 
           'convert_unicode': True}
        if FLAGS.sql_connection_debug >= 100:
            engine_args['echo'] = 'debug'
        elif FLAGS.sql_connection_debug >= 50:
            engine_args['echo'] = True
        if 'sqlite' in connection_dict.drivername:
            engine_args['poolclass'] = NullPool
            if FLAGS.sql_connection == 'sqlite://':
                engine_args['poolclass'] = StaticPool
                engine_args['connect_args'] = {'check_same_thread': False}
        _ENGINE = sqlalchemy.create_engine(FLAGS.sql_connection, **engine_args)
        if 'mysql' in connection_dict.drivername:
            sqlalchemy.event.listen(_ENGINE, 'checkout', ping_listener)
        else:
            if 'sqlite' in connection_dict.drivername:
                if not FLAGS.sqlite_synchronous:
                    sqlalchemy.event.listen(_ENGINE, 'connect', synchronous_switch_listener)
            try:
                _ENGINE.connect()
            except OperationalError as e:
                if not is_db_connection_error(e.args[0]):
                    raise
                remaining = FLAGS.sql_max_retries
                if remaining == -1:
                    remaining = 'infinite'
                while True:
                    msg = _('SQL connection failed. %s attempts left.')
                    LOG.warn(msg % remaining)
                    if remaining != 'infinite':
                        remaining -= 1
                    time.sleep(FLAGS.sql_retry_interval)
                    try:
                        _ENGINE.connect()
                        break
                    except OperationalError as e:
                        if remaining != 'infinite' and remaining == 0 or not is_db_connection_error(e.args[0]):
                            raise

    return _ENGINE


def get_maker(engine, autocommit=True, expire_on_commit=False):
    """Return a SQLAlchemy sessionmaker using the given engine."""
    return sqlalchemy.orm.sessionmaker(bind=engine, autocommit=autocommit, expire_on_commit=expire_on_commit)