# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.9-x86_64/egg/arctic/arctic.py
# Compiled at: 2019-05-18 09:07:34
# Size of source mod 2**32: 25669 bytes
import logging, os, re, threading, pymongo
from pymongo.errors import OperationFailure, AutoReconnect
from six import string_types
from ._cache import Cache
from ._config import ENABLE_CACHE
from ._util import indent
from .auth import authenticate, get_auth
from .chunkstore import chunkstore
from .decorators import mongo_retry
from .exceptions import LibraryNotFoundException, ArcticException, QuotaExceededException
from .hooks import get_mongodb_uri
from .store import version_store, bson_store, metadata_store
from .tickstore import tickstore, toplevel
__all__ = [
 'Arctic', 'VERSION_STORE', 'METADATA_STORE', 'TICK_STORE', 'CHUNK_STORE', 'register_library_type']
logger = logging.getLogger(__name__)
logger.addHandler(logging.NullHandler())
APPLICATION_NAME = 'arctic'
VERSION_STORE = version_store.VERSION_STORE_TYPE
METADATA_STORE = metadata_store.METADATA_STORE_TYPE
TICK_STORE = tickstore.TICK_STORE_TYPE
CHUNK_STORE = chunkstore.CHUNK_STORE_TYPE
LIBRARY_TYPES = {version_store.VERSION_STORE_TYPE: version_store.VersionStore, 
 tickstore.TICK_STORE_TYPE: tickstore.TickStore, 
 toplevel.TICK_STORE_TYPE: toplevel.TopLevelTickStore, 
 chunkstore.CHUNK_STORE_TYPE: chunkstore.ChunkStore, 
 bson_store.BSON_STORE_TYPE: bson_store.BSONStore, 
 metadata_store.METADATA_STORE_TYPE: metadata_store.MetadataStore}

def register_library_type(name, type_):
    """
    Register a Arctic Library Type handler
    """
    if name in LIBRARY_TYPES:
        raise ArcticException('Library %s already registered as %s' % (name, LIBRARY_TYPES[name]))
    LIBRARY_TYPES[name] = type_


class Arctic(object):
    __doc__ = "\n    The Arctic class is a top-level God object, owner of all arctic_<user> databases\n    accessible in Mongo.\n    Each database contains one or more ArcticLibrarys which may have implementation\n    specific functionality.\n\n    Current Mongo Library types:\n       - arctic.VERSION_STORE - Versioned store for chunked Pandas and numpy objects\n                                (other Python types are pickled)\n       - arctic.TICK_STORE - Tick specific library. Supports 'snapshots', efficiently\n                             stores updates, not versioned.\n       - arctic.METADATA_STORE - Stores metadata with timestamps\n\n    Arctic and ArcticLibrary are responsible for Connection setup, authentication,\n    dispatch to the appropriate library implementation, and quotas.\n    "
    DB_PREFIX = 'arctic'
    METADATA_COLL = 'ARCTIC'
    METADATA_DOC_ID = 'ARCTIC_META'
    _MAX_CONNS = 4
    _Arctic__conn = None

    def __init__(self, mongo_host, app_name=APPLICATION_NAME, allow_secondary=False, socketTimeoutMS=600000, connectTimeoutMS=2000, serverSelectionTimeoutMS=30000, **kwargs):
        """
        Constructs a Arctic Datastore.

        Note: If mongo_host is a pymongo connection and the process is later forked, the
                new pymongo connection may have different parameters.

        Parameters:
        -----------
        mongo_host: A MongoDB hostname, alias or Mongo Connection

        app_name: `str` is the name of application used for resolving credentials when
            authenticating against the mongo_host.
            We will fetch credentials using the authentication hook.
            Teams should override this such that different applications don't accidentally
            run with privileges to other applications' databases

        allow_secondary: `bool` indicates if we allow reads against
             secondary members in the cluster.  These reads may be
             a few seconds behind (but are usually split-second up-to-date).

        serverSelectionTimeoutMS: `int` the main tunable used for configuring how long
            the pymongo driver will spend on MongoDB cluster discovery.  This parameter
            takes precedence over connectTimeoutMS: https://jira.mongodb.org/browse/DRIVERS-222

        kwargs: 'dict' extra keyword arguments to pass when calling pymongo.MongoClient,
            for example ssl parameters.
        """
        self._application_name = app_name
        self._library_cache = {}
        self._allow_secondary = allow_secondary
        self._socket_timeout = socketTimeoutMS
        self._connect_timeout = connectTimeoutMS
        self._server_selection_timeout = serverSelectionTimeoutMS
        self._lock = threading.RLock()
        self._pid = os.getpid()
        self._pymongo_kwargs = kwargs
        self._cache = None
        if isinstance(mongo_host, string_types):
            self._given_instance = False
            self.mongo_host = mongo_host
        else:
            self._given_instance = True
            self._Arctic__conn = mongo_host
            mongo_host.server_info()
            self.mongo_host = ','.join(['{}:{}'.format(x[0], x[1]) for x in mongo_host.nodes])
            self._adminDB = self._conn.admin
            self._cache = Cache(self._conn)

    @property
    @mongo_retry
    def _conn(self):
        with self._lock:
            curr_pid = os.getpid()
            if curr_pid != self._pid:
                if self._given_instance:
                    logger.warn('Forking process. Arctic was passed a pymongo connection during init, the new pymongo connection may have different parameters.')
                self._pid = curr_pid
                self.reset()
            if self._Arctic__conn is None:
                host = get_mongodb_uri(self.mongo_host)
                logger.info('Connecting to mongo: {0} ({1})'.format(self.mongo_host, host))
                self._Arctic__conn = (pymongo.MongoClient)(host=host, maxPoolSize=self._MAX_CONNS, 
                 socketTimeoutMS=self._socket_timeout, 
                 connectTimeoutMS=self._connect_timeout, 
                 serverSelectionTimeoutMS=self._server_selection_timeout, **self._pymongo_kwargs)
                self._adminDB = self._Arctic__conn.admin
                self._cache = Cache(self._Arctic__conn)
                auth = get_auth(self.mongo_host, self._application_name, 'admin')
                if auth:
                    authenticate(self._adminDB, auth.user, auth.password)
                self._Arctic__conn.server_info()
            return self._Arctic__conn

    def reset(self):
        logger.debug('Arctic.reset()')
        with self._lock:
            if self._Arctic__conn is not None:
                self._Arctic__conn.close()
                self._Arctic__conn = None
            for _, l in self._library_cache.items():
                if hasattr(l, '_reset') and callable(l._reset):
                    logger.debug('Library reset() %s' % l)
                    l._reset()

    def __str__(self):
        return '<Arctic at %s, connected to %s>' % (hex(id(self)), str(self._conn))

    def __repr__(self):
        return str(self)

    def __getstate__(self):
        return {'mongo_host':self.mongo_host, 
         'app_name':self._application_name, 
         'allow_secondary':self._allow_secondary, 
         'socketTimeoutMS':self._socket_timeout, 
         'connectTimeoutMS':self._connect_timeout, 
         'serverSelectionTimeoutMS':self._server_selection_timeout}

    def __setstate__(self, state):
        return (Arctic.__init__)(self, **state)

    def is_caching_enabled(self):
        """
        Allows people to enable or disable caching for list_libraries globally.
        """
        _ = self._conn
        return self._cache.is_caching_enabled(ENABLE_CACHE)

    def list_libraries(self, newer_than_secs=None):
        """
        Returns
        -------
        list of Arctic library names
        """
        if self.is_caching_enabled():
            return self._list_libraries_cached(newer_than_secs)
        return self._list_libraries()

    @mongo_retry
    def _list_libraries(self):
        libs = []
        for db in self._conn.list_database_names():
            if db.startswith(self.DB_PREFIX + '_'):
                for coll in self._conn[db].list_collection_names():
                    if coll.endswith(self.METADATA_COLL):
                        libs.append(db[len(self.DB_PREFIX) + 1:] + '.' + coll[:-1 * len(self.METADATA_COLL) - 1])

            elif db == self.DB_PREFIX:
                for coll in self._conn[db].list_collection_names():
                    if coll.endswith(self.METADATA_COLL):
                        libs.append(coll[:-1 * len(self.METADATA_COLL) - 1])

        return libs

    def _list_libraries_cached(self, newer_than_secs=None):
        """
        Returns
        -------
        List of Arctic library names from a cached collection (global per mongo cluster) in mongo.
        Long term list_libraries should have a use_cached argument.
        """
        _ = self._conn
        cache_data = self._cache.get('list_libraries', newer_than_secs)
        if not cache_data:
            logging.debug('Cache has expired data, fetching from slow path and reloading cache.')
            libs = self._list_libraries()
            self._cache.set('list_libraries', libs)
            return libs
        return cache_data

    def reload_cache(self):
        _ = self._conn
        self._cache.set('list_libraries', self._list_libraries())

    def library_exists(self, library):
        """
        Check whether a given library exists.

        Parameters
        ----------
        library : `str`
            The name of the library. e.g. 'library' or 'user.library'

        Returns
        -------
        `bool`
            True if the library with the given name already exists, False otherwise
        """
        exists = False
        try:
            ArcticLibraryBinding(self, library).get_library_type()
            self.get_library(library)
            exists = True
        except OperationFailure:
            exists = library in self.list_libraries()
        except LibraryNotFoundException:
            pass

        return exists

    def _sanitize_lib_name(self, library):
        if library.startswith(self.DB_PREFIX + '_'):
            return library[len(self.DB_PREFIX) + 1:]
        return library

    @mongo_retry
    def initialize_library(self, library, lib_type=VERSION_STORE, **kwargs):
        """
        Create an Arctic Library or a particular type.

        Parameters
        ----------
        library : `str`
            The name of the library. e.g. 'library' or 'user.library'

        lib_type : `str`
            The type of the library.  e.g. arctic.VERSION_STORE or arctic.TICK_STORE
            Or any type registered with register_library_type
            Default: arctic.VERSION_STORE

        kwargs :
            Arguments passed to the Library type for initialization.
        """
        lib = ArcticLibraryBinding(self, library)
        check_library_count = kwargs.pop('check_library_count', True)
        if len(self._conn[lib.database_name].list_collection_names()) > 5000:
            if check_library_count:
                raise ArcticException('Too many namespaces %s, not creating: %s' % (
                 len(self._conn[lib.database_name].list_collection_names()), library))
        lib.set_library_type(lib_type)
        (LIBRARY_TYPES[lib_type].initialize_library)(lib, **kwargs)
        if not lib.get_quota():
            lib.set_quota(10737418240)
        self._cache.append('list_libraries', self._sanitize_lib_name(library))

    @mongo_retry
    def delete_library(self, library):
        """
        Delete an Arctic Library, and all associated collections in the MongoDB.

        Parameters
        ----------
        library : `str`
            The name of the library. e.g. 'library' or 'user.library'
        """
        lib = ArcticLibraryBinding(self, library)
        colname = lib.get_top_level_collection().name
        if not [c for c in lib._db.list_collection_names(False) if re.match('^{}([\\.].*)?$'.format(colname), c)]:
            logger.info('Nothing to delete. Arctic library %s does not exist.' % colname)
        logger.info('Dropping collection: %s' % colname)
        lib._db.drop_collection(colname)
        for coll in lib._db.list_collection_names():
            if coll.startswith(colname + '.'):
                logger.info('Dropping collection: %s' % coll)
                lib._db.drop_collection(coll)

        if library in self._library_cache:
            del self._library_cache[library]
            del self._library_cache[lib.get_name()]
        self._cache.delete_item_from_key('list_libraries', self._sanitize_lib_name(library))

    def get_library(self, library):
        """
        Return the library instance.  Can generally use slicing to return the library:
            arctic_store[library]

        Parameters
        ----------
        library : `str`
            The name of the library. e.g. 'library' or 'user.library'
        """
        if library in self._library_cache:
            return self._library_cache[library]
        try:
            error = None
            lib = ArcticLibraryBinding(self, library)
            lib_type = lib.get_library_type()
        except (OperationFailure, AutoReconnect) as e:
            try:
                error = e
            finally:
                e = None
                del e

        if error:
            raise LibraryNotFoundException('Library %s was not correctly initialized in %s.\nReason: %r)' % (
             library, self, error))
        else:
            if not lib_type:
                raise LibraryNotFoundException('Library %s was not correctly initialized in %s.' % (
                 library, self))
            else:
                if lib_type not in LIBRARY_TYPES:
                    raise LibraryNotFoundException("Couldn't load LibraryType '%s' for '%s' (has the class been registered?)" % (
                     lib_type, library))
        instance = LIBRARY_TYPES[lib_type](lib)
        self._library_cache[library] = instance
        self._library_cache[lib.get_name()] = instance
        return self._library_cache[library]

    def __getitem__(self, key):
        if isinstance(key, string_types):
            return self.get_library(key)
        raise ArcticException('Unrecognised library specification - use [libraryName]')

    def set_quota(self, library, quota):
        """
        Set a quota (in bytes) on this user library.  The quota is 'best effort',
        and should be set conservatively.

        Parameters
        ----------
        library : `str`
            The name of the library. e.g. 'library' or 'user.library'

        quota : `int`
            Advisory quota for the library - in bytes
        """
        ArcticLibraryBinding(self, library).set_quota(quota)

    def get_quota(self, library):
        """
        Return the quota currently set on the library.

        Parameters
        ----------
        library : `str`
            The name of the library. e.g. 'library' or 'user.library'
        """
        return ArcticLibraryBinding(self, library).get_quota()

    def check_quota(self, library):
        """
        Check the quota on the library, as would be done during normal writes.

        Parameters
        ----------
        library : `str`
            The name of the library. e.g. 'library' or 'user.library'

        Raises
        ------
        arctic.exceptions.QuotaExceededException if the quota has been exceeded
        """
        ArcticLibraryBinding(self, library).check_quota()

    def rename_library(self, from_lib, to_lib):
        """
        Renames a library

        Parameters
        ----------
        from_lib: str
            The name of the library to be renamed
        to_lib: str
            The new name of the library
        """
        to_colname = to_lib
        if '.' in from_lib:
            if '.' in to_lib:
                if from_lib.split('.')[0] != to_lib.split('.')[0]:
                    raise ValueError('Collection can only be renamed in the same database')
                to_colname = to_lib.split('.')[1]
        lib = ArcticLibraryBinding(self, from_lib)
        colname = lib.get_top_level_collection().name
        logger.info('Renaming collection: %s' % colname)
        lib._db[colname].rename(to_colname)
        for coll in lib._db.list_collection_names():
            if coll.startswith(colname + '.'):
                lib._db[coll].rename(coll.replace(colname, to_colname))

        if from_lib in self._library_cache:
            del self._library_cache[from_lib]
            del self._library_cache[lib.get_name()]
        self._cache.update_item_for_key('list_libraries', self._sanitize_lib_name(from_lib), self._sanitize_lib_name(to_lib))

    def get_library_type(self, lib):
        """
        Returns the type of the library

        Parameters
        ----------
        lib: str
            the library
        """
        return ArcticLibraryBinding(self, lib).get_library_type()


class ArcticLibraryBinding(object):
    __doc__ = "\n    The ArcticLibraryBinding type holds the binding between the library name and the\n    concrete implementation of the library.\n\n    Also provides access to additional metadata about the library\n        - Access to the library's top-level collection\n        - Enforces quota on the library\n        - Access to custom metadata about the library\n    "
    DB_PREFIX = Arctic.DB_PREFIX
    TYPE_FIELD = 'TYPE'
    QUOTA = 'QUOTA'
    quota = None
    quota_countdown = 0

    @classmethod
    def _parse_db_lib(cls, library):
        """
        Returns the canonical (database_name, library) for the passed in
        string 'library'.
        """
        database_name = library.split('.', 2)
        if len(database_name) == 2:
            library = database_name[1]
            if database_name[0].startswith(cls.DB_PREFIX):
                database_name = database_name[0]
            else:
                database_name = cls.DB_PREFIX + '_' + database_name[0]
        else:
            database_name = cls.DB_PREFIX
        return (
         database_name, library)

    def __init__(self, arctic, library):
        self.arctic = arctic
        self._curr_conn = self.arctic._conn
        self._lock = threading.RLock()
        database_name, library = self._parse_db_lib(library)
        self.library = library
        self.database_name = database_name
        self._auth(self.arctic._conn[self.database_name])

    @property
    def _db(self):
        with self._lock:
            arctic_conn = self.arctic._conn
            if arctic_conn is not self._curr_conn:
                self._auth(arctic_conn[self.database_name])
                self._curr_conn = arctic_conn
        return self.arctic._conn[self.database_name]

    @property
    def _library_coll(self):
        return self._db[self.library]

    def __str__(self):
        return '<ArcticLibrary at %s, %s.%s>\n%s' % (hex(id(self)), self._db.name, self._library_coll.name, indent(str(self.arctic), 4))

    def __repr__(self):
        return str(self)

    def __getstate__(self):
        return {'arctic':self.arctic, 
         'library':'.'.join([self.database_name, self.library])}

    def __setstate__(self, state):
        return ArcticLibraryBinding.__init__(self, state['arctic'], state['library'])

    @mongo_retry
    def _auth(self, database):
        if not hasattr(self.arctic, 'mongo_host'):
            return
        auth = get_auth(self.arctic.mongo_host, self.arctic._application_name, database.name)
        if auth:
            authenticate(database, auth.user, auth.password)

    def reset_auth(self):
        logger.debug('reset_auth() %s' % self)
        self._auth(self._db)

    def get_name(self):
        return self._db.name + '.' + self._library_coll.name

    def get_top_level_collection(self):
        """
        Return the top-level collection for the Library.  This collection is to be used
        for storing data.

        Note we expect (and callers require) this collection to have default read-preference: primary
        The read path may choose to reduce this if secondary reads are allowed.
        """
        return self._library_coll

    def set_quota(self, quota_bytes):
        """
        Set a quota (in bytes) on this user library.  The quota is 'best effort',
        and should be set conservatively.

        A quota of 0 is 'unlimited'
        """
        self.set_library_metadata(ArcticLibraryBinding.QUOTA, quota_bytes)
        self.quota = quota_bytes
        self.quota_countdown = 0

    def get_quota(self):
        """
        Get the current quota on this user library.
        """
        return self.get_library_metadata(ArcticLibraryBinding.QUOTA)

    def check_quota(self):
        """
        Check whether the user is within quota.  Should be called before
        every write.  Will raise() if the library has exceeded its allotted
        quota.
        """
        if self.quota_countdown > 0:
            self.quota_countdown -= 1
            return
            self.quota = self.get_library_metadata(ArcticLibraryBinding.QUOTA)
            if self.quota is None or self.quota == 0:
                self.quota = 0
                return
            library = self.arctic[self.get_name()]
            stats = library.stats()

            def to_gigabytes(bytes_):
                return bytes_ / 1024.0 / 1024.0 / 1024.0

            size = stats['totals']['size']
            count = stats['totals']['count']
            if size >= self.quota:
                raise QuotaExceededException('Mongo Quota Exceeded: %s %.3f / %.0f GB used' % (
                 '.'.join([self.database_name, self.library]),
                 to_gigabytes(size),
                 to_gigabytes(self.quota)))
        else:
            try:
                avg_size = size // count if count > 1 else 102400
                remaining = self.quota - size
                remaining_count = remaining / avg_size
                if remaining_count < 100 or float(remaining) / self.quota < 0.1:
                    logger.warning('Mongo Quota: %s %.3f / %.0f GB used' % (
                     '.'.join([self.database_name, self.library]),
                     to_gigabytes(size),
                     to_gigabytes(self.quota)))
                else:
                    logger.info('Mongo Quota: %s %.3f / %.0f GB used' % (
                     '.'.join([self.database_name, self.library]),
                     to_gigabytes(size),
                     to_gigabytes(self.quota)))
                self.quota_countdown = int(max(remaining_count // 2, 1))
            except Exception as e:
                try:
                    logger.warning('Encountered an exception while calculating quota statistics: %s' % str(e))
                finally:
                    e = None
                    del e

    def get_library_type(self):
        return self.get_library_metadata(ArcticLibraryBinding.TYPE_FIELD)

    def set_library_type(self, lib_type):
        self.set_library_metadata(ArcticLibraryBinding.TYPE_FIELD, lib_type)

    @mongo_retry
    def get_library_metadata(self, field):
        lib_metadata = self._library_coll[self.arctic.METADATA_COLL].find_one({'_id': self.arctic.METADATA_DOC_ID})
        if lib_metadata is not None:
            return lib_metadata.get(field)
        return

    @mongo_retry
    def set_library_metadata(self, field, value):
        self._library_coll[self.arctic.METADATA_COLL].update_one({'_id': self.arctic.METADATA_DOC_ID}, {'$set': {field: value}},
          upsert=True)