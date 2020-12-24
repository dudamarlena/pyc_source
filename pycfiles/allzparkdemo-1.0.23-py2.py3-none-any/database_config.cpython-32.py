# uncompyle6 version 3.6.7
# Python bytecode 3.2 (3180)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/sql_alchemy/database_config.py
# Compiled at: 2013-10-02 09:54:40
__doc__ = '\nCreated on Jan 8, 2012\n\n@package: support sqlalchemy\n@copyright: 2011 Sourcefabric o.p.s.\n@license: http://www.gnu.org/licenses/gpl-3.0.txt\n@author: Gabriel Nistor\n\nContains sql alchemy database setup.\n'
from ally.container import ioc, app
from ally.container.error import ConfigError
from sqlalchemy.engine import create_engine
from sqlalchemy.engine.base import Engine
from sqlalchemy.orm.session import sessionmaker
from sqlalchemy import event
import logging
log = logging.getLogger(__name__)

@ioc.config
def database_url():
    """
    The database URL, something like:
        "sqlite:///{database}.db"
        "mysql+mysqlconnector://{user}:{password}@localhost/{database}"
    """
    raise ConfigError('A database URL is required')


@ioc.config
def alchemy_pool_recycle():
    """The time to recycle pooled connection"""
    return 3600


@ioc.entity
def alchemySessionCreator():
    return sessionmaker(bind=alchemyEngine())


@ioc.entity
def alchemyEngine() -> Engine:
    engine = create_engine(database_url(), pool_recycle=alchemy_pool_recycle())
    if database_url().startswith('sqlite://'):

        @event.listens_for(engine, 'connect')
        def setSQLiteFKs(dbapi_con, con_record):
            dbapi_con.execute('PRAGMA foreign_keys=ON')

    return engine


@ioc.entity
def metas():
    return []


@app.populate(app.DEVEL, app.CHANGED, priority=app.PRIORITY_TOP)
def createTables():
    for meta in metas():
        meta.create_all(alchemyEngine())