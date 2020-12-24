# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/vagrant/envs/conversocial/lib/python2.7/site-packages/shardmonster/operations.py
# Compiled at: 2016-11-29 07:45:10
"""Contains everything to do with making Mongo operations work across multiple
clusters.
"""
import bson, numbers, time
from shardmonster.connection import get_connection, parse_location
from shardmonster.metadata import _get_shards_coll, ShardStatus, _get_realm_for_collection, _get_location_for_shard, _get_all_locations_for_realm, _get_metadata_for_shard
untargetted_query_callback = None

def _create_collection_iterator(collection_name, query, with_options={}):
    """Creates an iterator that returns collections and queries that can then
    be used to perform multishard operations:

        for collection, query, location in _create_collection_iterator(...):
            for doc in collection.find(query):
                yield doc

    This does all the hardwork of figuring out what collections to query and how
    to adjust the query to account for any shards that are currently moving.
    """
    global untargetted_query_callback
    realm = _get_realm_for_collection(collection_name)
    shard_field = realm['shard_field']
    shard_key = _get_query_target(collection_name, query)
    if shard_key:
        location = _get_location_for_shard(realm, shard_key)
        locations = {location.location: location}
    else:
        locations = _get_all_locations_for_realm(realm)
        if untargetted_query_callback:
            untargetted_query_callback(collection_name, query)
        for location, location_meta in locations.iteritems():
            cluster_name, database_name = parse_location(location)
            connection = get_connection(cluster_name)
            collection = connection[database_name][collection_name]
            if with_options:
                collection = collection.with_options(**with_options)
            if location_meta.excludes:
                if len(location_meta.excludes) == 1:
                    query = {'$and': [query, {shard_field: {'$ne': location_meta.excludes[0]}}]}
                else:
                    raise Exception('Multiple shards in transit. Aborting')
            yield (
             collection, query, location)
            if location_meta.excludes:
                query = query['$and'][0]


class MultishardCursor(object):

    def __init__(self, collection_name, query, *args, **kwargs):
        self.query = query
        self.collection_name = collection_name
        self.args = args
        self.kwargs = kwargs
        self._hint = kwargs.pop('_hint', None)
        self.with_options = kwargs.pop('with_options', {})
        self._prepared = False
        self._skip = 0
        self._explains = []
        return

    def _create_collection_iterator(self):
        return _create_collection_iterator(self.collection_name, self.query, self.with_options)

    def _prepare_for_iteration(self):
        self._queries_pending = list(self._create_collection_iterator())
        self._targetted = len(self._queries_pending) == 1
        self._cached_results = None
        self._next_cursor()
        self._prepared = True
        self._skipped = 0
        return

    def _next_cursor(self):
        collection, query, location = self._queries_pending.pop(0)
        if self._targetted:
            query_kwargs = self.kwargs.copy()
            query_kwargs['skip'] = self._skip
        elif self._skip and self.kwargs.get('limit'):
            query_kwargs = self.kwargs.copy()
            query_kwargs['limit'] = query_kwargs['limit'] + self._skip
        else:
            query_kwargs = self.kwargs
        cursor = collection.find(query, *self.args, **query_kwargs)
        if self._hint:
            cursor = cursor.hint(self._hint)
        self._explains.append((location, cursor.explain))
        self._current_cursor = cursor

    def __iter__(self):
        return self

    def __len__(self):
        return self.count()

    def next(self):
        res = self._next()
        return res

    def _next(self):
        if not self._prepared:
            self.evaluate()
        safe_skip = self._skip or 0
        if 'sort' not in self.kwargs:
            while self._skipped < safe_skip:
                self._skipped += 1
                self._next_result()

        return self._next_result()

    def _next_result(self):
        """Gets the next result from any cache or cursors available. Ignores
        skipping as that is done in a higher layer.
        """
        while True:
            if self._cached_results:
                return self._cached_results.pop(0)
            try:
                return self._current_cursor.next()
            except StopIteration:
                if self._queries_pending:
                    length_before = len(self._queries_pending)
                    self._next_cursor()
                    assert length_before > len(self._queries_pending)
                else:
                    raise

    def limit(self, limit):
        self.kwargs['limit'] = limit
        return self

    def skip(self, skip):
        self._skip = skip
        return self

    def sort(self, key_or_list, direction=None):
        if direction:
            self.kwargs['sort'] = [
             (
              key_or_list, direction)]
        else:
            self.kwargs['sort'] = key_or_list
        return self

    def clone(self):
        return MultishardCursor(self.collection_name, self.query, _hint=self._hint, *self.args, **self.kwargs)

    def __getitem__(self, i):
        if isinstance(i, int):
            new_cursor = self.clone()
            new_cursor.limit(1)
            new_cursor.skip(i)
            return list(new_cursor)[0]
        else:
            new_cursor = self.clone()
            new_cursor.skip(i.start or 0)
            if i.stop:
                new_cursor.limit(i.stop - (i.start or 0))
            else:
                new_cursor.limit(0)
            return new_cursor

    def explain(self):
        return {location:e() for location, e in self._explains}

    def evaluate(self):
        self._prepare_for_iteration()
        if len(self._queries_pending) == 0:
            return
        if 'sort' in self.kwargs:
            all_results = list(self)

            def comparator(d1, d2):
                for key, sort_order in self.kwargs['sort']:
                    if d1[key] < d2[key]:
                        return -sort_order
                    if d1[key] > d2[key]:
                        return sort_order

                return 0

            self._cached_results = list(sorted(all_results, cmp=comparator))
            if self._skip:
                self._cached_results = self._cached_results[self._skip:]
        if self.kwargs.get('limit'):
            self._cached_results = list(self)[:self.kwargs['limit']]

    def count(self, **count_kwargs):
        total = 0
        for collection, query, _ in self._create_collection_iterator():
            cursor = collection.find(query, *self.args, **self.kwargs)
            if self._hint:
                cursor = cursor.hint(self._hint)
            total += cursor.count(**count_kwargs)

        if self.kwargs.get('limit'):
            return min(self.kwargs['limit'], total)
        else:
            return total

    def rewind(self):
        self._cached_results = None
        self._current_cursor = None
        self._queries_pending = None
        self._prepared = False
        return

    def hint(self, index):
        self._hint = index
        return self

    @property
    def alive(self):
        if not self._prepared:
            self.evaluate()
        current_alive = self._current_cursor.alive or self._cached_results
        if not current_alive and self._queries_pending:
            self._next_cursor()
            return self.alive
        return current_alive


def _create_multishard_iterator(collection_name, query, *args, **kwargs):
    return MultishardCursor(collection_name, query, *args, **kwargs)


def multishard_find(collection_name, query, *args, **kwargs):
    return _create_multishard_iterator(collection_name, query, *args, **kwargs)


def multishard_find_one(collection_name, query, **kwargs):
    kwargs['limit'] = 1
    cursor = _create_multishard_iterator(collection_name, query, **kwargs)
    try:
        return cursor.next()
    except StopIteration:
        return

    return


def multishard_insert(collection_name, doc_or_docs, with_options={}, *args, **kwargs):
    is_multi_insert = isinstance(doc_or_docs, list)
    if not is_multi_insert:
        all_docs = [
         doc_or_docs]
    else:
        all_docs = doc_or_docs
    _wait_for_pause_to_end(collection_name, doc_or_docs)
    realm = _get_realm_for_collection(collection_name)
    shard_field = realm['shard_field']
    for doc in all_docs:
        if shard_field not in doc:
            raise Exception('Cannot insert document without shard field (%s) present' % shard_field)

    result = []
    for doc in all_docs:
        simple_query = {shard_field: doc[shard_field]}
        (collection, _, _), = _create_collection_iterator(collection_name, simple_query, with_options)
        result.append(collection.insert(doc, *args, **kwargs))

    if not is_multi_insert:
        return result[0]
    return result


def _is_valid_type_for_sharding(value):
    return isinstance(value, (numbers.Integral, basestring, bson.ObjectId))


def _get_query_target(collection_name, query):
    """Gets out the targetted shard key from the query if there is one.
    Otherwise, returns None.
    """
    realm = _get_realm_for_collection(collection_name)
    shard_field = realm['shard_field']
    if shard_field in query and _is_valid_type_for_sharding(query[shard_field]):
        return query[shard_field]
    else:
        return


def _should_pause_write(collection_name, query):
    realm = _get_realm_for_collection(collection_name)
    shard_key = _get_query_target(collection_name, query)
    if shard_key:
        meta = _get_metadata_for_shard(realm, shard_key)
        return meta['status'] == ShardStatus.POST_MIGRATION_PAUSED_AT_DESTINATION
    else:
        paused_query = {'realm': realm['name'], 
           'status': ShardStatus.POST_MIGRATION_PAUSED_AT_DESTINATION}
        shards_coll = _get_shards_coll()
        return shards_coll.find(paused_query).count() > 0


def _wait_for_pause_to_end(collection_name, query):
    while _should_pause_write(collection_name, query):
        time.sleep(0.05)


def _get_collection_for_targetted_upsert(collection_name, query, update, with_options={}):
    shard_key = _get_query_target(collection_name, update)
    if not shard_key:
        shard_key = _get_query_target(collection_name, update['$set'])
    realm = _get_realm_for_collection(collection_name)
    location = _get_location_for_shard(realm, shard_key)
    cluster_name, database_name = parse_location(location.location)
    connection = get_connection(cluster_name)
    collection = connection[database_name][collection_name]
    if with_options:
        collection = collection.with_options(with_options)
    return collection


def multishard_update(collection_name, query, update, with_options={}, **kwargs):
    _wait_for_pause_to_end(collection_name, query)
    overall_result = None
    collection_iterator = None
    if kwargs.get('upsert', False) and '$set' in update and _get_query_target(collection_name, update['$set']):
        collection = _get_collection_for_targetted_upsert(collection_name, query, update, with_options)
        collection_iterator = [(collection, query, None)]
    if kwargs.get('upsert', False) and _get_query_target(collection_name, update):
        collection = _get_collection_for_targetted_upsert(collection_name, query, update, with_options)
        collection_iterator = [(collection, query, None)]
    if not collection_iterator:
        collection_iterator = _create_collection_iterator(collection_name, query, with_options)
    for collection, targetted_query, _ in collection_iterator:
        result = collection.update(targetted_query, update, **kwargs)
        if not overall_result:
            overall_result = result
        else:
            overall_result['n'] += result['n']

    return overall_result


def multishard_remove(collection_name, query, with_options={}, **kwargs):
    _wait_for_pause_to_end(collection_name, query)
    overall_result = None
    collection_iterator = _create_collection_iterator(collection_name, query, with_options)
    for collection, targetted_query, _ in collection_iterator:
        result = collection.remove(targetted_query, **kwargs)
        if not overall_result:
            overall_result = result
        else:
            overall_result['n'] += result['n']

    return overall_result


def multishard_aggregate(collection_name, pipeline, with_options={}, *args, **kwargs):
    realm = _get_realm_for_collection(collection_name)
    shard_field = realm['shard_field']
    if '$match' not in pipeline[0]:
        raise Exception('Sharded aggregation needs match in the first part of the pipeline')
    if shard_field not in pipeline[0]['$match']:
        raise Exception('Cannot perform aggregation without shard field (%s) present' % shard_field)
    match_query = pipeline[0]['$match']
    (collection, _, _), = _create_collection_iterator(collection_name, match_query, with_options)
    return collection.aggregate(pipeline, useCursor=False, *args, **kwargs)


def multishard_save(collection_name, doc, with_options={}, *args, **kwargs):
    _wait_for_pause_to_end(collection_name, doc)
    realm = _get_realm_for_collection(collection_name)
    shard_field = realm['shard_field']
    if shard_field not in doc:
        raise Exception('Cannot save document without shard field (%s) present' % shard_field)
    simple_query = {shard_field: doc[shard_field]}
    (collection, _, _), = _create_collection_iterator(collection_name, simple_query, with_options)
    return collection.save(doc, *args, **kwargs)


def multishard_ensure_index(collection_name, *args, **kwargs):
    collection_iterator = _create_collection_iterator(collection_name, {})
    for collection, _, _ in collection_iterator:
        collection.ensure_index(*args, **kwargs)


def multishard_find_and_modify(collection_name, query, update, **kwargs):
    _wait_for_pause_to_end(collection_name, query)
    realm = _get_realm_for_collection(collection_name)
    shard_field = realm['shard_field']
    if shard_field not in query:
        raise Exception('Cannot perform find_and_modify without shard field (%s) present' % shard_field)
    collection = _get_collection_for_targetted_upsert(collection_name, query, {'$set': query})
    return collection.find_and_modify(query, update, **kwargs)