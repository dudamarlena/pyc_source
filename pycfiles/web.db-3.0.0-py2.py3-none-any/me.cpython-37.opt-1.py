# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /web/db/me.py
# Compiled at: 2019-06-09 23:34:50
# Size of source mod 2**32: 2783 bytes
try:
    from mongoengine import connect
    from mongoengine.connection import disconnect
    from mongoengine.base import get_document
    from mongoengine.errors import NotRegistered
except ImportError:
    raise ImportError('Unable to import mongoengine; pip install mongoengine to fix this.')

from .util import redact_uri
log = __import__('logging').getLogger(__name__)

class MongoEngineProxy:
    __doc__ = 'Lazily load MongoEngine Document subclasses from its registry.\n\t\n\tBecause MongoEngine supports the concept of multiple named connections, if you make multiple\n\t`MongoEngineDBConnection` connections the same Document subclasses are made available across all.\n\t'

    def __init__(self, connection):
        self._connection = connection
        self._database = connection.get_default_database()

    def __getattr__(self, name):
        if name[0] == '_':
            raise AttributeError()
        else:
            if name[0].islower():
                return getattr(self._database, name)
            try:
                return get_document(name)
            except NotRegistered:
                pass

        raise AttributeError()

    def __getitem__(self, name):
        try:
            return self.__getattr__(name)
        except AttributeError:
            pass

        raise KeyError()


class MongoEngineConnection:
    __doc__ = 'WebCore DBExtension interface for projects utilizing MongoEngine.\n\t\n\tURI-style connection strings should always be utilized. Provide a `replicaSet` query string argument to enable\n\treplica set functionality. The alias name is preserved through to MongoEngine to allow use of database switching\n\tmechanisms, such as the `switch_db` context manager, and multiple instances may be used to populate the\n\t`DatabaseExtension` connections.\n\t\n\tAny additional keyword arguments used are passed through to `mongoengine.connect`, which in turn passes the values\n\talong to `mongoengine.connection.register_connection` for further processing.\n\t'

    def __init__(self, uri, alias=None, **kw):
        """Prepare configuration options."""
        kw['host'] = uri
        self.alias = alias
        self.config = kw

    def start(self, context):
        """Initialize the database connection."""
        self.config['alias'] = self.alias
        safe_config = dict(self.config)
        del safe_config['host']
        log.info('Connecting MongoEngine database layer.', extra=dict(uri=(redact_uri(self.config['host'])),
          config=(self.config)))
        self.connection = connect(**self.config)

    def prepare(self, context):
        """Attach this connection's default database to the context using our alias."""
        context.db[self.alias] = MongoEngineProxy(self.connection)

    def stop(self, context):
        """Close the connection pool and clean up references in MongoEngine."""
        disconnect(self.alias)
        del self.connection