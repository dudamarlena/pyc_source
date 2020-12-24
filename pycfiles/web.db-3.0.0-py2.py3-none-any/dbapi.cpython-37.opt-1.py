# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /web/db/dbapi.py
# Compiled at: 2019-06-09 23:35:07
# Size of source mod 2**32: 1826 bytes
from marrow.package.loader import load
from .util import redact_uri
log = __import__('logging').getLogger(__name__)

class DBAPIConnection:
    __doc__ = 'WebCore DBExtension interface for projects utilizing PEP 249 DB API database engines.'
    uri_safety = True
    thread_safe = True

    def __init__(self, engine, uri, safe=True, protect=True, alias=None, **kw):
        """Prepare configuration options."""
        self.engine = engine
        self.uri = uri
        self.safe = safe
        self.protect = protect
        self.alias = alias
        self.config = kw
        self._connector = load(engine, 'db_api_connect')
        if self.safe:
            self.start = self._connect
            self.stop = self._disconnect
        else:
            self.prepare = self._connect
            self.done = self._disconnect

    def __repr__(self):
        return '{self.__class__.__name__}({self.alias}, "{self.engine}", "{uri}")'.format(self=self,
          uri=(redact_uri(self.uri, self.protect)))

    def _connect(self, context):
        """Initialize the database connection."""
        log.info(('Connecting ' + self.engine.partition(':')[0] + ' database layer.'), extra=dict(uri=(redact_uri(self.uri, self.protect)),
          config=(self.config),
          alias=(self.alias)))
        self.connection = context.db[self.alias] = (self._connector)((self.uri), **self.config)

    def _disconnect(self, context):
        """Close the connection and clean up references."""
        self.connection.close()
        del self.connection


class SQLite3Connection(DBAPIConnection):

    def __init__(self, path, alias=None, **kw):
        (super().__init__)('sqlite3:connect', path, False, False, alias, **kw)