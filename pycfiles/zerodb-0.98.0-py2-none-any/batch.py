# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /zerodb/storage/batch.py
# Compiled at: 2016-03-08 18:12:41
from six.moves import zip as izip
import logging
from ZEO.ClientStorage import ClientStorage
from ZEO.Exceptions import ClientDisconnected

class ZEOBatchStorage(object):
    """
    ZEOStorage which loadEx object can return many oids at once
    """

    def loadBulk(self, oids):
        """
        Load multiple oids

        :param list oids: Iterable oids to load at once
        :return: Loaded oid objects
        :rtype: list
        """
        return [ self.loadEx(oid) for oid in oids ]


class BatchClientStorage(ClientStorage):
    """
    Allows to get objects in batches
    zlibstorage should wrap *after* this
    """

    def __init__(self, *args, **kw):
        super(BatchClientStorage, self).__init__(*args, **kw)
        self._load_oids = {}

    def _process_invalidations(self, tid, oids):
        for oid in oids:
            if self._load_oids.get(oid, None):
                self._load_oids[oid] = 0
            self._cache.invalidate(oid, tid)

        self._cache.setLastTid(tid)
        if self._db is not None:
            self._db.invalidate(tid, oids)
        return

    def loadBulk(self, oids):
        """
        Storage API to return multiple objects
        We load a unique set of them, just in case

        :param list oids: Iterable oids to load at once
        :return: Loaded oid objects
        :rtype: list
        """
        self._load_lock.acquire()
        try:
            self._lock.acquire()
            try:
                result = []
                for oid in oids:
                    out = self._cache.load(oid)
                    if not out:
                        self._load_oids[oid] = 1
                    else:
                        result.append(out)

            finally:
                self._lock.release()

            if len(self._load_oids) == 0:
                return result
            if self._server is None:
                raise ClientDisconnected()
            load_oids = list(self._load_oids.keys())
            bulk_data = self._server.rpc.call('loadBulk', load_oids)
            data_size = 0
            for oid, (data, tid) in izip(load_oids, bulk_data):
                data_size += len(data)
                self._lock.acquire()
                try:
                    if self._load_oids[oid]:
                        self._cache.store(oid, tid, None, data)
                    del self._load_oids[oid]
                    result.append((data, tid))
                finally:
                    self._lock.release()

            logging.debug(('Bulk-loaded {0} objects of size {1}').format(len(load_oids), data_size))
        finally:
            self._load_lock.release()

        return result