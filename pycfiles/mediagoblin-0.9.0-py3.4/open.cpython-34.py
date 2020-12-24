# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/mediagoblin/db/open.py
# Compiled at: 2016-02-04 13:34:40
# Size of source mod 2**32: 5639 bytes
from contextlib import contextmanager
import logging, six
from sqlalchemy import create_engine, event
from mediagoblin import mg_globals
from mediagoblin.db.base import Base
_log = logging.getLogger(__name__)
from mediagoblin.tools.transition import DISABLE_GLOBALS

def set_models_as_attributes(obj):
    """
    Set all models as attributes on this object, for convenience

    TODO: This should eventually be deprecated.
    """
    for k, v in six.iteritems(Base._decl_class_registry):
        setattr(obj, k, v)


if not DISABLE_GLOBALS:
    from mediagoblin.db.base import Session

    class DatabaseMaster(object):

        def __init__(self, engine):
            self.engine = engine
            set_models_as_attributes(self)

        def commit(self):
            Session.commit()

        def save(self, obj):
            Session.add(obj)
            Session.flush()

        def check_session_clean(self):
            for dummy in Session():
                _log.warn('STRANGE: There are elements in the sql session. Please report this and help us track this down.')
                break

        def reset_after_request(self):
            Session.rollback()
            Session.remove()

        @property
        def query(self):
            return Session.query


else:
    from sqlalchemy.orm import sessionmaker

    class DatabaseManager(object):
        __doc__ = '\n        Manage database connections.\n\n        The main method here is session_scope which can be used with a\n        "with" statement to get a session that is properly torn down\n        by the end of execution.\n        '

        def __init__(self, engine):
            self.engine = engine
            self.Session = sessionmaker(bind=engine)
            set_models_as_attributes(self)

        @contextmanager
        def session_scope(self):
            """
            This is a context manager, use like::

              with dbmanager.session_scope() as request.db:
                  some_view(request)
            """
            session = self.Session()

            def save(obj):
                session.add(obj)
                session.flush()

            def check_session_clean():
                for dummy in session:
                    _log.warn('STRANGE: There are elements in the sql session. Please report this and help us track this down.')
                    break

            def reset_after_request():
                session.rollback()
                session.remove()

            session.save = save
            session.check_session_clean = check_session_clean
            session.reset_after_request = reset_after_request
            set_models_as_attributes(session)
            try:
                yield session
            finally:
                session.rollback()
                session.close()


def load_models(app_config):
    import mediagoblin.db.models
    for plugin in mg_globals.global_config.get('plugins', {}).keys():
        _log.debug('Loading %s.models', plugin)
        try:
            __import__(plugin + '.models')
        except ImportError as exc:
            _log.debug('Could not load {0}.models: {1}'.format(plugin, exc))


def _sqlite_fk_pragma_on_connect(dbapi_con, con_record):
    """Enable foreign key checking on each new sqlite connection"""
    dbapi_con.execute('pragma foreign_keys=on')


def _sqlite_disable_fk_pragma_on_connect(dbapi_con, con_record):
    """
    Disable foreign key checking on each new sqlite connection
    (Good for migrations!)
    """
    dbapi_con.execute('pragma foreign_keys=off')


def setup_connection_and_db_from_config(app_config, migrations=False, app=None):
    engine = create_engine(app_config['sql_engine'])
    engine.app = app
    if app_config['sql_engine'].startswith('sqlite://'):
        if migrations:
            event.listen(engine, 'connect', _sqlite_disable_fk_pragma_on_connect)
        else:
            event.listen(engine, 'connect', _sqlite_fk_pragma_on_connect)
    if DISABLE_GLOBALS:
        return DatabaseManager(engine)
    else:
        Session.configure(bind=engine)
        return DatabaseMaster(engine)


def check_db_migrations_current(db):
    pass