# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/breilly/git/fm-orchestrator/module_build_service/db_session.py
# Compiled at: 2019-12-12 15:53:56
import sqlalchemy.event
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.pool import NullPool
from module_build_service import conf
from module_build_service.models import session_before_commit_handlers
__all__ = ('db_session', )

def _setup_event_listeners(db_session):
    """
    Starts listening for events related to the database session.
    """
    if not sqlalchemy.event.contains(db_session, 'before_commit', session_before_commit_handlers):
        sqlalchemy.event.listen(db_session, 'before_commit', session_before_commit_handlers)
    from module_build_service.monitor import db_hook_event_listeners
    db_hook_event_listeners(db_session.bind.engine)


def apply_engine_options(conf):
    options = {'configuration': {'sqlalchemy.url': conf.sqlalchemy_database_uri}}
    if conf.sqlalchemy_database_uri.startswith('sqlite://'):
        options.update({'connect_args': {'check_same_thread': False}, 'poolclass': NullPool})
    else:
        pool_options = {}

        def apply_mbs_option(mbs_config_key, sa_config_key):
            value = getattr(conf, mbs_config_key, None)
            if value is not None:
                pool_options[sa_config_key] = value
            return

        apply_mbs_option('sqlalchemy_pool_size', 'pool_size')
        apply_mbs_option('sqlalchemy_pool_timeout', 'pool_timeout')
        apply_mbs_option('sqlalchemy_pool_recycle', 'pool_recycle')
        apply_mbs_option('sqlalchemy_max_overflow', 'max_overflow')
        options.update(pool_options)
    return options


engine_opts = apply_engine_options(conf)
engine = sqlalchemy.engine_from_config(**engine_opts)
session_factory = sessionmaker(bind=engine)
db_session = scoped_session(session_factory)
_setup_event_listeners(db_session)