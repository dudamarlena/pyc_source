# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/ztfy/utils/zodb.py
# Compiled at: 2013-12-05 05:44:50
__docformat__ = 'restructuredtext'
from persistent import Persistent
from persistent.interfaces import IPersistent
from transaction.interfaces import ITransactionManager
from ZODB.interfaces import IConnection
from zope.schema.interfaces import IVocabularyFactory
from ztfy.utils.interfaces import IZEOConnection
from ZEO import ClientStorage
from ZODB import DB
from zope.component import adapter
from zope.componentvocabulary.vocabulary import UtilityVocabulary
from zope.container.contained import Contained
from zope.interface import implementer, implements, classProvides
from zope.schema import getFieldNames
from zope.schema.fieldproperty import FieldProperty
from zope.security.proxy import removeSecurityProxy

class ZEOConnectionInfo(object):
    """ZEO connection info
    
    Provides a context manager which directly returns
    ZEO connection root
    """
    implements(IZEOConnection)
    _storage = None
    _db = None
    _connection = None
    server_name = FieldProperty(IZEOConnection['server_name'])
    server_port = FieldProperty(IZEOConnection['server_port'])
    storage = FieldProperty(IZEOConnection['storage'])
    username = FieldProperty(IZEOConnection['username'])
    password = FieldProperty(IZEOConnection['password'])
    server_realm = FieldProperty(IZEOConnection['server_realm'])
    blob_dir = FieldProperty(IZEOConnection['blob_dir'])
    shared_blob_dir = FieldProperty(IZEOConnection['shared_blob_dir'])

    def getSettings(self):
        result = {}
        for name in getFieldNames(IZEOConnection):
            result[name] = getattr(self, name)

        return result

    def update(self, settings):
        names = getFieldNames(IZEOConnection)
        for k, v in settings.items():
            if k in names:
                setattr(self, k, unicode(v) if isinstance(v, str) else v)

    def getConnection(self, wait=False, get_storage=False):
        """Get a tuple made of storage and DB connection for given settings"""
        storage = ClientStorage.ClientStorage((str(self.server_name), self.server_port), storage=self.storage, username=self.username or '', password=self.password or '', realm=self.server_realm, blob_dir=self.blob_dir, shared_blob_dir=self.shared_blob_dir, wait=wait)
        db = DB(storage)
        if get_storage:
            return (storage, db)
        return db

    @property
    def connection(self):
        return self._connection

    def __enter__(self):
        self._storage, self._db = self.getConnection(get_storage=True)
        self._connection = self._db.open()
        return self._connection.root()

    def __exit__(self, exc_type, exc_value, traceback):
        if self._connection is not None:
            self._connection.close()
        if self._storage is not None:
            self._storage.close()
        return


class ZEOConnectionUtility(ZEOConnectionInfo, Persistent, Contained):
    """Persistent ZEO connection settings utility"""
    pass


class ZEOConnectionVocabulary(UtilityVocabulary):
    """ZEO connections vocabulary"""
    classProvides(IVocabularyFactory)
    interface = IZEOConnection
    nameOnly = True


@adapter(IPersistent)
@implementer(ITransactionManager)
def transactionManager(obj):
    conn = IConnection(removeSecurityProxy(obj))
    try:
        return conn.transaction_manager
    except AttributeError:
        return conn._txn_mgr