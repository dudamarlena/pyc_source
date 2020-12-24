# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/tsab/__init__.py
# Compiled at: 2008-07-12 17:49:28
"""
    Trac SQLAlchemy Bridge
    ======================

    tsab
    ~~~~

    This module enables a plugin developer to use SQLAlchemy for database work.

    :copyright: 2008 by Armin Ronacher, Pedro Algarvio.
    :license: WTFPL.

"""
__version__ = '0.1.0'
__author__ = 'Armin Ronacher, Pedro Algarvio'
__email__ = 'armin.ronacher@active-4.com, ufs@ufsoft.org'
__package__ = 'TracSqlAlchemyBridge'
__license__ = 'WTFPL'
__url__ = ''
__summary__ = 'Bridge for a plugin developer to use SQLAlchemy with trac'
__description__ = 'Bridge for a plugin developer to use SQLAlchemy with trac'
from weakref import WeakKeyDictionary
from threading import local
from sqlalchemy.engine import create_engine
from sqlalchemy.orm import create_session, scoped_session
from sqlalchemy.pool import NullPool
from sqlalchemy.engine.url import URL
from trac.db.api import DatabaseManager
from trac.db.util import ConnectionWrapper

class DummyPool(NullPool):

    def do_return_conn(self, conn):
        pass


_engines = WeakKeyDictionary()

def engine(env):
    engine = _engines.get(env)
    if engine is None:
        schema = DatabaseManager(env).connection_uri.split(':')[0]
        echo = env.config.get('logging', 'log_level').lower() == 'debug'
        echo = False

        def connect():
            cnx = env.get_db_cnx().cnx
            while isinstance(cnx, ConnectionWrapper):
                cnx = cnx.cnx

            return cnx

        engine = create_engine(URL(schema), poolclass=DummyPool, creator=connect, echo=echo)
        if echo:
            engine.logger = env.log
            _engines[env] = engine
    return engine


def session(env):
    db_session = create_session(engine(env), transactional=True)
    env.db_session = db_session
    return db_session


__all__ = [
 'engine', 'session']