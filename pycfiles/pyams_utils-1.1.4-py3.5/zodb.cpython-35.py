# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/pyams_utils/zodb.py
# Compiled at: 2020-02-18 19:11:13
# Size of source mod 2**32: 11368 bytes
""""PyAMS_utils.zodb module

This modules provides several utilities used to manage ZODB connections and persistent objects
"""
from ZEO import DB
from ZODB.interfaces import IConnection
from persistent import Persistent
from persistent.interfaces import IPersistent
from pyramid.events import subscriber
from pyramid_zodbconn import db_from_uri, get_uris
from transaction.interfaces import ITransactionManager
from zope.annotation.interfaces import IAttributeAnnotatable
from zope.container.contained import Contained
from zope.interface import implementer
from zope.lifecycleevent.interfaces import IObjectAddedEvent, IObjectRemovedEvent
from zope.schema import getFieldNames
from zope.schema.fieldproperty import FieldProperty
from zope.schema.vocabulary import SimpleTerm, SimpleVocabulary
from pyams_utils.adapter import adapter_config
from pyams_utils.interfaces import IOptionalUtility
from pyams_utils.interfaces.zeo import IZEOConnection
from pyams_utils.registry import get_global_registry, get_utilities_for
from pyams_utils.vocabulary import vocabulary_config
__docformat__ = 'restructuredtext'

@adapter_config(context=IPersistent, provides=IConnection)
def persistent_connection(obj):
    """An adapter which gets a ZODB connection from a persistent object

    We are assuming the object has a parent if it has been created in
    this transaction.

    Raises ValueError if it is impossible to get a connection.
    """
    cur = obj
    while not getattr(cur, '_p_jar', None):
        cur = getattr(cur, '__parent__', None)
        if cur is None:
            return

    return cur._p_jar


@adapter_config(context=IPersistent, provides=ITransactionManager)
def persistent_transaction_manager(obj):
    """Transaction manager adapter for persistent objects"""
    conn = IConnection(obj)
    try:
        return conn.transaction_manager
    except AttributeError:
        return conn._txn_mgr


@implementer(IZEOConnection)
class ZEOConnection:
    __doc__ = "ZEO connection object\n\n    This object can be used to store all settings to be able to open a ZEO connection.\n    Note that this class is required only for tasks specifically targeting a ZEO database\n    connection (like a ZEO packer scheduler task); for generic ZODB operations, just use a\n    :py:class:`ZODBConnection <pyams_utils.zodb.ZODBConnection>` class defined through Pyramid's\n    configuration file.\n\n    Note that a ZEO connection object is a context manager, so you can use it like this:\n\n    .. code-block:: python\n\n        from pyams_utils.zodb import ZEOConnection\n\n        def my_method(zeo_settings):\n            zeo_connection = ZEOConnection()\n            zeo_connection.update(zeo_settings)\n            with zeo_connection as root:\n                # *root* is then the ZODB root object\n                # do whatever you want with ZEO connection,\n                # which is closed automatically\n    "
    _storage = None
    _db = None
    _connection = None
    name = FieldProperty(IZEOConnection['name'])
    server_name = FieldProperty(IZEOConnection['server_name'])
    server_port = FieldProperty(IZEOConnection['server_port'])
    storage = FieldProperty(IZEOConnection['storage'])
    username = FieldProperty(IZEOConnection['username'])
    password = FieldProperty(IZEOConnection['password'])
    server_realm = FieldProperty(IZEOConnection['server_realm'])
    blob_dir = FieldProperty(IZEOConnection['blob_dir'])
    shared_blob_dir = FieldProperty(IZEOConnection['shared_blob_dir'])

    def get_settings(self):
        """Get mapping of all connection settings

        These settings can be converted to JSON and sent to another process, for example
        via a ØMQ connection.

        :return: dict
        """
        result = {}
        for name in getFieldNames(IZEOConnection):
            result[name] = getattr(self, name)

        return result

    def update(self, settings):
        """Update connection properties with settings as *dict*

        :param dict settings: typically extracted via the :py:meth:`get_settings` method from
            another process
        """
        names = getFieldNames(IZEOConnection)
        for key, value in settings.items():
            if key in names:
                setattr(self, key, value)

    def get_connection(self, wait_timeout=30, get_storage=False):
        """Create ZEO client connection from current settings

        :param boolean wait_timeout: connection timeout, in seconds
        :param boolean get_storage: if *True*, the method should return a tuple containing
            storage and DB objects; otherwise only DB object is returned
        :return: tuple containing ZEO client storage and DB object (if *get_storage* argument is
            set to *True*), or only DB object otherwise
        """
        zdb = DB((self.server_name, self.server_port), storage=self.storage, username=self.username or '', password=self.password or '', realm=self.server_realm, blob_dir=self.blob_dir, shared_blob_dir=self.shared_blob_dir, wait_timeout=wait_timeout)
        if get_storage:
            return (zdb.storage, zdb)
        return zdb

    @property
    def connection(self):
        """Connection getter"""
        return self._connection

    def __enter__(self):
        self._storage, self._db = self.get_connection(get_storage=True)
        self._connection = self._db.open_then_close_db_when_connection_closes()
        return self._connection.root()

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self._connection is not None:
            self._connection.close()
        if self._storage is not None:
            self._storage.close()


@implementer(IOptionalUtility, IAttributeAnnotatable)
class ZEOConnectionUtility(ZEOConnection, Persistent, Contained):
    __doc__ = 'Persistent ZEO connection utility'


@subscriber(IObjectAddedEvent, context_selector=IZEOConnection)
def handle_added_connection(event):
    """Register new ZEO connection when added"""
    manager = event.newParent
    manager.registerUtility(event.object, IZEOConnection, name=event.object.name)


@subscriber(IObjectRemovedEvent, context_selector=IZEOConnection)
def handle_removed_connection(event):
    """Un-register ZEO connection when deleted"""
    manager = event.oldParent
    manager.unregisterUtility(event.object, IZEOConnection, name=event.object.name)


@vocabulary_config(name='PyAMS ZEO connections')
class ZEOConnectionVocabulary(SimpleVocabulary):
    __doc__ = 'ZEO connections vocabulary'

    def __init__(self, context=None):
        terms = [SimpleTerm(name, title=util.name) for name, util in get_utilities_for(IZEOConnection)]
        super(ZEOConnectionVocabulary, self).__init__(terms)


def get_connection_from_settings(settings=None):
    """Load connection matching registry settings"""
    if settings is None:
        settings = get_global_registry().settings
    for name, uri in get_uris(settings):
        zdb = db_from_uri(uri, name, {})
        return zdb.open()


class ZODBConnection:
    __doc__ = "ZODB connection wrapper\n\n    Connections are extracted from Pyramid's settings file in *zodbconn.uri* entries.\n\n    Note that a ZODB connection object is a context manager, so you can use it like this:\n\n    .. code-block:: python\n\n        from pyams_utils.zodb import ZODBConnection\n\n        def my_method(zodb_name):\n            zodb_connection = ZODBConnection(zodb_name)\n            with zodb_connection as root:\n                # *root* is then the ZODB root object\n                # do whatever you want with ZODB connection,\n                # which is closed automatically\n    "

    def __init__(self, name='', settings=None):
        self.name = name or ''
        if not settings:
            settings = get_global_registry().settings
        self.settings = settings

    _connection = None
    _db = None
    _storage = None

    @property
    def connection(self):
        """Connection getter"""
        return self._connection

    @property
    def db(self):
        """Database getter"""
        return self._db

    @property
    def storage(self):
        """Storage getter"""
        return self._storage

    def get_connection(self):
        """Load named connection matching registry settings"""
        for name, uri in get_uris(self.settings):
            if name == self.name:
                zdb = db_from_uri(uri, name, {})
                connection = self._connection = zdb.open()
                self._db = connection.db()
                self._storage = self.db.storage
                return connection

    def close(self):
        """Connection close"""
        self._connection.close()
        self._db.close()
        self._storage.close()

    def __enter__(self):
        connection = self.get_connection()
        return connection.root()

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()


@vocabulary_config(name='PyAMS ZODB connections')
class ZODBConnectionVocabulary(SimpleVocabulary):
    __doc__ = 'ZODB connections vocabulary'

    def __init__(self, context=None):
        settings = get_global_registry().settings
        terms = [SimpleTerm(name, title=name) for name, uri in get_uris(settings)]
        super(ZODBConnectionVocabulary, self).__init__(terms)


VOLATILE_MARKER = object()

class volatile_property:
    __doc__ = 'Property decorator to define volatile attributes into persistent classes'

    def __init__(self, fget, doc=None):
        self.fget = fget
        self.__doc__ = doc or fget.__doc__
        self.__name__ = fget.__name__
        self.__module__ = fget.__module__

    def __get__(self, inst, cls):
        if inst is None:
            return self
        attrname = '_v_{0}'.format(self.__name__)
        value = getattr(inst, attrname, VOLATILE_MARKER)
        if value is VOLATILE_MARKER:
            value = self.fget(inst)
            setattr(inst, attrname, value)
        return value

    def __delete__(self, inst):
        attrname = '_v_{0}'.format(self.__name__)
        if hasattr(inst, attrname):
            delattr(inst, attrname)