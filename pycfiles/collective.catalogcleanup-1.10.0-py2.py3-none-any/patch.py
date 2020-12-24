# uncompyle6 version 3.6.7
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-i686/egg/collective/catalogcache/patch.py
# Compiled at: 2009-06-10 09:02:40
import BTrees.Length
from BTrees.IIBTree import intersection, weightedIntersection, IISet
from BTrees.OIBTree import OIBTree
from BTrees.IOBTree import IOBTree
from Products.ZCatalog.Lazy import LazyMap, LazyCat
import types
from DateTime import DateTime
from md5 import md5
import time
from Products.ZCatalog.Catalog import LOG
from os import environ
import transaction
from zope.interface import implements
from transaction.interfaces import IDataManager
try:
    import memcache
    s = environ.get('MEMCACHE_SERVERS', '')
    if s:
        servers = s.split(',')
    if not s:
        HAS_MEMCACHE = False
        LOG.info('No memcached servers defined. Catalog will function as normal.')
    else:
        mem_cache = memcache.Client(servers, debug=0)
        HAS_MEMCACHE = True
        LOG.info('Using memcached servers %s' % (',').join(servers))
except ImportError:
    mem_cache = None
    HAS_MEMCACHE = False
    LOG.info('Cannot import memcached. Catalog will function as normal.')

MEMCACHE_DURATION = 7200
MEMCACHE_RETRY_INTERVAL = 10
memcache_insertion_timestamps = {}
_hits = {}
_misses = {}
_memcache_failure_timestamp = 0
_cache_misses = {}

class MemcachedDataManager(object):
    __module__ = __name__
    implements(IDataManager)

    def __init__(self, id, cacheadapter, key_prefix='', to_set={}, to_delete=[], duration=None):
        self.id = id
        self.cacheadapter = cacheadapter
        self.key_prefix = key_prefix
        self.to_set = to_set
        self.to_delete = to_delete
        self.duration = duration

    def abort(self, trans):
        pass

    def commit(self, trans):
        pass

    def tpc_begin(self, trans):
        pass

    def tpc_vote(self, trans):
        self.cacheadapter.commit()

    def tpc_finish(self, trans):
        pass

    def tpc_abort(self, trans):
        pass

    def sortKey(self):
        return 'MemcachedDataManager%s' % self.id


class MemcachedAdapter(object):
    __module__ = __name__

    def __init__(self, memcache, default_duration):
        self.memcache = memcache
        self.default_duration = default_duration
        self.counter = 1000000
        txn = transaction.get()
        txn.join(MemcachedDataManager(self.counter, self))

    def set_multi(self, to_set, key_prefix, duration=None, immediate=False):
        """
        Returns: 
            failure: (a) list of keys which failed to be stored or 
                     (b) False if no memcache servers could be reached
            success: empty list
        """
        global _memcache_failure_timestamp
        if immediate:
            try:
                result = self.memcache.set_multi(to_set, key_prefix=key_prefix, time=duration or self.default_duration)
            except TypeError:
                return False
            else:
                if isinstance(result, types.ListType) and len(result):
                    LOG.error('_cache_result set_multi failed')
                    _memcache_failure_timestamp = int(time.time())
                    if len(result) != len(to_set.keys()):
                        LOG.error('Some keys were successfully written to memcache. This case needs further handling.')
                return result
        txn = transaction.get()
        self.counter += 1
        if not hasattr(txn, 'v_cache'):
            txn.v_cache = dict()
        for (k, v) in to_set.items():
            s_k = key_prefix + str(k)
            txn.v_cache[s_k] = v
            if hasattr(txn, 'v_delete_cache') and s_k in txn.v_delete_cache:
                try:
                    txn.v_delete_cache.remove(s_k)
                except ValueError:
                    pass

    def get(self, key, default=[]):
        """
        Parameter key is already prefixed

        Returns: 
            success: value
            failure: default
        """
        txn = transaction.get()
        if hasattr(txn, 'v_delete_cache') and key in txn.v_delete_cache:
            return default
        if hasattr(txn, 'v_cache') and txn.v_cache.has_key(key):
            try:
                return txn.v_cache[key]
            except KeyError:
                pass

        result = self.memcache.get(key)
        if result is None:
            return default
        return result

    def get_multi(self, to_get, key_prefix):
        """
        Returns: 
            success, failure: dictionary
        """
        if not to_get:
            return {}
        txn = transaction.get()
        new_to_get = []
        if hasattr(txn, 'v_delete_cache'):
            for k in to_get:
                s_k = key_prefix + str(k)
                if s_k not in txn.v_delete_cache:
                    new_to_get.append(k)

        else:
            new_to_get = to_get
        result_cache = {}
        keys_still_to_get = []
        if hasattr(txn, 'v_cache'):
            for k in new_to_get:
                s_k = key_prefix + str(k)
                if txn.v_cache.has_key(s_k):
                    try:
                        result_cache[k] = txn.v_cache[s_k]
                    except KeyError:
                        keys_still_to_get.append(k)

                else:
                    keys_still_to_get.append(k)

        else:
            keys_still_to_get = new_to_get
        result_memcache = {}
        if keys_still_to_get:
            try:
                result_memcache = self.memcache.get_multi(keys_still_to_get, key_prefix=key_prefix)
            except KeyError:
                pass

        result_memcache.update(result_cache)
        return result_memcache

    def delete_multi(self, to_delete, immediate=False):
        """
        All elements in to_delete are already prefixed

        Returns:
            success: 1
            failure: not 1
        """
        if not to_delete:
            return 1
        if immediate:
            return self.memcache.delete_multi(to_delete)
        txn = transaction.get()
        if not hasattr(txn, 'v_delete_cache'):
            txn.v_delete_cache = []
        for k in to_delete:
            if k not in txn.v_delete_cache:
                txn.v_delete_cache.append(k)

        self.counter += 1
        if hasattr(txn, 'v_cache'):
            for k in to_delete:
                if txn.v_cache.has_key(k):
                    try:
                        del txn.v_cache[k]
                    except KeyError:
                        pass

        return 1

    def flush_all(self):
        """
        Returns:
            success, failure: undefined
        """
        txn = transaction.get()
        if hasattr(txn, 'v_cache'):
            txn.v_cache.clear()
        if hasattr(txn, 'v_cache'):
            txn.v_delete_cache = []
        return self.memcache.flush_all()

    def commit(self):
        """
        Do one atomic commit. This is in fact not atomic since the memcached wrapper
        needs more work but it is the best we can do.
        """
        txn = transaction.get()
        if hasattr(txn, 'v_delete_cache'):
            if self.delete_multi(to_delete=txn.v_delete_cache, immediate=True) != 1:
                LOG.error('_invalidate_cache delete_multi failed')
            txn.v_delete_cache = []
        if hasattr(txn, 'v_cache'):
            result_set = self.set_multi(to_set=txn.v_cache, key_prefix='', duration=self.default_duration, immediate=True)
            txn.v_cache.clear()


def _getMemcachedAdapter(self):
    global MEMCACHE_DURATION
    global mem_cache
    txn = transaction.get()
    if not hasattr(txn, 'v_memcached_adapter'):
        txn.v_memcached_adapter = MemcachedAdapter(mem_cache, default_duration=MEMCACHE_DURATION)
    return txn.v_memcached_adapter


def _memcache_available(self):
    global HAS_MEMCACHE
    global MEMCACHE_RETRY_INTERVAL
    global _memcache_failure_timestamp
    if not HAS_MEMCACHE:
        return False
    now_seconds = int(time.time())
    if now_seconds - _memcache_failure_timestamp < MEMCACHE_RETRY_INTERVAL:
        return False
    _memcache_failure_timestamp = 0
    return True


def _cache_result(self, cache_key, rs, search_indexes=[]):
    if not self._memcache_available():
        return
    if rs is None:
        return
    cache_id = ('/').join(self.getPhysicalPath())
    to_set = {}
    lcache_key = cache_id + cache_key
    to_set[cache_key] = rs
    to_get = []
    for r in rs:
        to_get.append(str(r))
        to_set[str(r)] = [lcache_key]

    for idx in search_indexes:
        if idx in ('sort_on', 'sort_order', 'sort_limit'):
            continue
        to_get.append(idx)
        to_set[idx] = [lcache_key]

    result = self._getMemcachedAdapter().get_multi(to_get, key_prefix=cache_id)
    for (k, v) in result.items():
        if not isinstance(v, types.ListType):
            continue
        to_set[k].extend(v)

    if to_set:
        now_seconds = int(time.time())
        li = to_set.items()
        li.sort()
        hash = md5(str(li)).hexdigest()
        if now_seconds - memcache_insertion_timestamps.get(hash, 0) < 10:
            LOG.debug('Prevent a call to set_multi since the same insert was done recently')
            return
        memcache_insertion_timestamps[hash] = now_seconds
        result = self._getMemcachedAdapter().set_multi(to_set, key_prefix=cache_id, duration=MEMCACHE_DURATION)
        if result == False:
            return
    return


def _get_cached_result(self, cache_key, default=[]):
    global _memcache_failure_timestamp
    if not self._memcache_available():
        return default
    cache_id = ('/').join(self.getPhysicalPath())
    key = cache_id + cache_key
    _cache_misses.setdefault(key, 0)
    result = self._getMemcachedAdapter().get(key, default)
    if result is None:
        now_seconds = int(time.time())
        if _cache_misses.get(key, 0) > 10:
            LOG.error('_get_cache_key failed 10 times')
            _memcache_failure_timestamp = now_seconds
            _cache_misses.clear()
        try:
            _cache_misses[key] += 1
        except KeyError:
            pass
        else:
            return default
    _cache_misses[key] = 0
    return result


def _invalidate_cache(self, rid=None, index_name='', immediate=False):
    """ Invalidate cached results affected by rid and / or index_name
    """
    global _memcache_failure_timestamp
    if not self._memcache_available():
        return
    cache_id = ('/').join(self.getPhysicalPath())
    LOG.debug('[%s] _invalidate_cache rid=%s, index_name=%s' % (cache_id, rid, index_name))
    to_delete = []
    if rid is not None:
        s_rid = cache_id + str(rid)
        rid_map = self._getMemcachedAdapter().get(s_rid, [])
        if rid_map is not None:
            to_delete.extend(rid_map)
        to_delete.append(s_rid)
    if index_name:
        s_index_name = cache_id + index_name
        index_map = self._getMemcachedAdapter().get(s_index_name, [])
        if index_map is not None:
            to_delete.extend(index_map)
        to_delete.append(s_index_name)
    if to_delete:
        now_seconds = int(time.time())
        LOG.debug('[%s] Remove %s items from cache' % (cache_id, len(to_delete)))
        if self._getMemcachedAdapter().delete_multi(to_delete, immediate=immediate) != 1:
            LOG.error('_invalidate_cache delete_multi failed')
            _memcache_failure_timestamp = now_seconds
    return


def _clear_cache(self):
    if not self._memcache_available():
        return
    LOG.debug('Flush cache')
    self._getMemcachedAdapter().flush_all()
    _hits.clear()
    _misses.clear()


def _get_cache_key(self, args):

    def pin_datetime(dt):
        return dt.strftime('%Y-%m-%d.%h:%m %Z')

    items = list(args.request.items())
    items.extend(list(args.keywords.items()))
    items.sort()
    sorted = []
    for (k, v) in items:
        if isinstance(v, types.ListType):
            v.sort()
        elif isinstance(v, types.TupleType):
            v = list(v)
            v.sort()
        elif isinstance(v, DateTime):
            v = pin_datetime(v)
        elif isinstance(v, types.DictType):
            tsorted = []
            titems = v.items()
            titems.sort()
            for (tk, tv) in titems:
                if isinstance(tv, DateTime):
                    tv = pin_datetime(tv)
                elif isinstance(tv, types.ListType) or isinstance(tv, types.TupleType):
                    li = []
                    for item in list(tv):
                        if isinstance(item, DateTime):
                            item = pin_datetime(item)
                        li.append(item)

                    tv = li
                tsorted.append((tk, tv))

            v = tsorted
        sorted.append((k, v))

    cache_key = str(sorted)
    return md5(cache_key).hexdigest()


def _get_search_indexes(self, args):
    keys = list(args.request.keys())
    keys.extend(list(args.keywords.keys()))
    return keys


def clear(self):
    """ clear catalog """
    self._clear_cache()
    self.data = IOBTree()
    self.uids = OIBTree()
    self.paths = IOBTree()
    self._length = BTrees.Length.Length()
    for index in self.indexes.keys():
        self.getIndex(index).clear()


def catalogObject(self, object, uid, threshold=None, idxs=None, update_metadata=1):
    """
    Adds an object to the Catalog by iteratively applying it to
    all indexes.

    'object' is the object to be cataloged

    'uid' is the unique Catalog identifier for this object

    If 'idxs' is specified (as a sequence), apply the object only
    to the named indexes.

    If 'update_metadata' is true (the default), also update metadata for
    the object.  If the object is new to the catalog, this flag has
    no effect (metadata is always created for new objects).

    """
    if idxs is None:
        idxs = []
    data = self.data
    index = self.uids.get(uid, None)
    if index is not None:
        self._invalidate_cache(rid=index)
    if index is None:
        index = self.updateMetadata(object, uid)
        if not hasattr(self, '_length'):
            self.migrate__len__()
        self._length.change(1)
        self.uids[uid] = index
        self.paths[index] = uid
    elif update_metadata:
        self.updateMetadata(object, uid)
    total = 0
    if idxs == []:
        use_indexes = self.indexes.keys()
    else:
        use_indexes = idxs
    for name in use_indexes:
        x = self.getIndex(name)
        if hasattr(x, 'index_object'):
            before = self.getIndex(name).getEntryForObject(index, '')
            blah = x.index_object(index, object, threshold)
            after = self.getIndex(name).getEntryForObject(index, '')
            if before != after:
                self._invalidate_cache(index_name=name)
            total = total + blah
        else:
            LOG.error('catalogObject was passed bad index object %s.' % str(x))

    return total


def uncatalogObject(self, uid):
    """
    Uncatalog and object from the Catalog.  and 'uid' is a unique
    Catalog identifier

    Note, the uid must be the same as when the object was
    catalogued, otherwise it will not get removed from the catalog

    This method should not raise an exception if the uid cannot
    be found in the catalog.

    """
    data = self.data
    uids = self.uids
    paths = self.paths
    indexes = self.indexes.keys()
    rid = uids.get(uid, None)
    if rid is not None:
        self._invalidate_cache(rid=rid)
        for name in indexes:
            x = self.getIndex(name)
            if hasattr(x, 'unindex_object'):
                x.unindex_object(rid)

        del data[rid]
        del paths[rid]
        del uids[uid]
        if not hasattr(self, '_length'):
            self.migrate__len__()
        self._length.change(-1)
    else:
        LOG.error('uncatalogObject unsuccessfully attempted to uncatalog an object with a uid of %s. ' % str(uid))
    return


def search(self, request, sort_index=None, reverse=0, limit=None, merge=1):
    """Iterate through the indexes, applying the query to each one. If
    merge is true then return a lazy result set (sorted if appropriate)
    otherwise return the raw (possibly scored) results for later merging.
    Limit is used in conjuntion with sorting or scored results to inform
    the catalog how many results you are really interested in. The catalog
    can then use optimizations to save time and memory. The number of
    results is not guaranteed to fall within the limit however, you should
    still slice or batch the results as usual."""
    rs = None
    cache_id = ('/').join(self.getPhysicalPath())
    cache_key = self._get_cache_key(request)
    _misses.setdefault(cache_id, 0)
    _hits.setdefault(cache_id, 0)
    marker = '_marker'
    rs = self._get_cached_result(cache_key, marker)
    if rs is marker:
        LOG.debug('[%s] MISS: %s' % (cache_id, cache_key))
        rs = None
        for i in self.indexes.keys():
            index = self.getIndex(i)
            _apply_index = getattr(index, '_apply_index', None)
            if _apply_index is None:
                continue
            r = _apply_index(request)
            if r is not None:
                (r, u) = r
                (w, rs) = weightedIntersection(rs, r)

        search_indexes = self._get_search_indexes(request)
        LOG.debug('[%s] Search indexes = %s' % (cache_id, str(search_indexes)))
        self._cache_result(cache_key, rs, search_indexes)
        try:
            _misses[cache_id] += 1
        except KeyError:
            pass

    else:
        try:
            _hits[cache_id] += 1
        except KeyError:
            pass

        if int(time.time()) % 10 == 0:
            hits = _hits.get(cache_id)
            if hits:
                misses = _misses.get(cache_id, 0)
                LOG.info('[%s] Hit rate: %.2f%%' % (cache_id, hits * 100.0 / (hits + misses)))
        if rs is None:
            if sort_index is None:
                return LazyMap(self.instantiate, self.data.items(), len(self))
            else:
                return self.sortResults(self.data, sort_index, reverse, limit, merge)
        elif rs:
            if sort_index is None and hasattr(rs, 'values'):
                if not merge:
                    getitem = self.__getitem__
                    return [ (score, (1, score, rid), getitem) for (rid, score) in rs.items() ]
                rs = rs.byValue(0)
                max = float(rs[0][0])

                def getScoredResult(item, max=max, self=self):
                    """
                Returns instances of self._v_brains, or whatever is passed
                into self.useBrains.
                """
                    (score, key) = item
                    r = self._v_result_class(self.data[key]).__of__(self.aq_parent)
                    r.data_record_id_ = key
                    r.data_record_score_ = score
                    r.data_record_normalized_score_ = int(100.0 * score / max)
                    return r

                return LazyMap(getScoredResult, rs, len(rs))
            elif sort_index is None and not hasattr(rs, 'values'):
                if hasattr(rs, 'keys'):
                    rs = rs.keys()
                return LazyMap(self.__getitem__, rs, len(rs))
            else:
                return self.sortResults(rs, sort_index, reverse, limit, merge)
        else:
            return LazyCat([])
    return


def __getitem__(self, index, ttype=type(())):
    """
    Returns instances of self._v_brains, or whatever is passed
    into self.useBrains.
    """
    if type(index) is ttype:
        (normalized_score, score, key) = index
        if not isinstance(key, types.IntType) or not self.data.has_key(key):
            LOG.error('Weighted rid %s leads to KeyError. Removing from cache.' % index)
            self._invalidate_cache(rid=index, immediate=True)
        r = self._v_result_class(self.data[key]).__of__(self.aq_parent)
        r.data_record_id_ = key
        r.data_record_score_ = score
        r.data_record_normalized_score_ = normalized_score
    else:
        if not isinstance(index, types.IntType) or not self.data.has_key(index):
            LOG.error('rid %s leads to KeyError. Removing from cache.' % index)
            self._invalidate_cache(rid=index, immediate=True)
        r = self._v_result_class(self.data[index]).__of__(self.aq_parent)
        r.data_record_id_ = index
        r.data_record_score_ = 1
        r.data_record_normalized_score_ = 1
    return r


from Products.ZCatalog.Catalog import Catalog
Catalog._getMemcachedAdapter = _getMemcachedAdapter
Catalog._memcache_available = _memcache_available
Catalog._cache_result = _cache_result
Catalog._get_cached_result = _get_cached_result
Catalog._invalidate_cache = _invalidate_cache
Catalog._clear_cache = _clear_cache
Catalog._get_cache_key = _get_cache_key
Catalog._get_search_indexes = _get_search_indexes
Catalog.clear = clear
Catalog.catalogObject = catalogObject
Catalog.uncatalogObject = uncatalogObject
Catalog.search = search
Catalog.__getitem__ = __getitem__