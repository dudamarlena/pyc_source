# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /web/db/sa.py
# Compiled at: 2019-06-09 23:34:24
# Size of source mod 2**32: 1915 bytes
try:
    from sqlalchemy import create_engine
    from sqlalchemy.orm import scoped_session, sessionmaker
except ImportError:
    raise ImportError('Unable to import sqlalchemy; pip install sqlalchemy to fix this.')

from .util import redact_uri
log = __import__('logging').getLogger(__name__)

class SQLAlchemyConnection:
    __doc__ = "SQLAlchemy database engine support for WebCore's DatabaseExtension."

    def __init__(self, uri, alias=None, **config):
        """Prepare SQLAlchemy configuration."""
        config.setdefault('pool_recycle', 3600)
        self.uri = uri
        self.alias = alias
        self.config = config
        self.engine = None
        self.Session = None

    def __repr__(self):
        return '{self.__class__.__name__}({self.alias}, "{uri}")'.format(self=self,
          uri=(redact_uri(self.uri)))

    def start(self, context):
        """Construct the SQLAlchemy engine and session factory."""
        log.info('Connecting SQLAlchemy database layer.', extra=dict(uri=(redact_uri(self.uri)),
          config=(self.config),
          alias=(self.alias)))
        engine = self.engine = create_engine((self.uri), **self.config)
        self.Session = scoped_session(sessionmaker(bind=engine))
        engine.connect().close()
        context.db[self.alias] = engine

    def prepare(self, context):
        """Prepare a sqlalchemy session on the WebCore context"""
        context.db[self.alias] = self.Session

    def done(self, context):
        """Close and clean up the request local session, if any."""
        context.db[self.alias].remove()

    def stop(self, context):
        """Disconnect any hanging connections in the pool."""
        self.engine.dispose()