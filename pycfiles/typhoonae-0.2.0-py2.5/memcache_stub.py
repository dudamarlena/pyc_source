# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-i386/egg/typhoonae/memcache/memcache_stub.py
# Compiled at: 2010-12-12 04:36:57
"""Memcache integration."""
import base64, cPickle, google.appengine.api.apiproxy_stub, google.appengine.api.memcache.memcache_service_pb, google.appengine.runtime.apiproxy_errors, logging, os, pylibmc, time
DEFAULT_ADDR = '127.0.0.1'
DEFAULT_PORT = 11211
MemcacheSetResponse = google.appengine.api.memcache.memcache_service_pb.MemcacheSetResponse
MemcacheSetRequest = google.appengine.api.memcache.memcache_service_pb.MemcacheSetRequest
MemcacheIncrementRequest = google.appengine.api.memcache.memcache_service_pb.MemcacheIncrementRequest
MemcacheIncrementResponse = google.appengine.api.memcache.memcache_service_pb.MemcacheIncrementResponse
MemcacheDeleteResponse = google.appengine.api.memcache.memcache_service_pb.MemcacheDeleteResponse

def getKey(key, namespace=None):
    """Returns a key."""
    app_id = os.environ.get('APPLICATION_ID', '')
    if app_id:
        app_id += '.'
    if namespace:
        key = '%(namespace)s.%(key)s' % locals()
    key = '%(app_id)s%(key)s' % locals()
    return base64.b64encode(key)


class MemcacheServiceStub(google.appengine.api.apiproxy_stub.APIProxyStub):
    """Memcache service stub.

    This stub uses memcached to store data.
    """

    def __init__(self, config=None, service_name='memcache'):
        """Initializes memcache service stub.

        Args:
            config: Dictionary containing configuration parameters.
            service_name: Service name expected for all calls.
        """
        super(MemcacheServiceStub, self).__init__(service_name)
        if config is None:
            config = dict(addr=DEFAULT_ADDR, port=DEFAULT_PORT)
        self._cache = pylibmc.Client(['%(addr)s:%(port)i' % config])
        return

    def _GetMemcacheBehavior(self):
        behaviors = self._cache.behaviors
        keys = sorted((k for k in behaviors if not k.startswith('_')))
        sorted_behaviors = [ (k, behaviors[k]) for k in keys ]
        logging.debug('Memcache behavior: %s' % sorted_behaviors)
        return sorted_behaviors

    def _Dynamic_Get(self, request, response):
        """Implementation of MemcacheService::Get().

        Args:
            request: A MemcacheGetRequest.
            response: A MemcacheGetResponse.
        """
        for key in set(request.key_list()):
            value = self._cache.get(getKey(key, request.name_space()))
            if value is None:
                continue
            flags = 0
            (stored_flags, stored_value) = cPickle.loads(value)
            flags |= stored_flags
            item = response.add_item()
            item.set_key(key)
            item.set_value(stored_value)
            item.set_flags(flags)

        return

    def _Dynamic_Set(self, request, response):
        """Implementation of MemcacheService::Set().

        Args:
            request: A MemcacheSetRequest.
            response: A MemcacheSetResponse.
        """
        for item in request.item_list():
            key = getKey(item.key(), request.name_space())
            set_policy = item.set_policy()
            old_entry = self._cache.get(key)
            set_status = MemcacheSetResponse.NOT_STORED
            set_value = cPickle.dumps([item.flags(), item.value()])
            if set_policy == MemcacheSetRequest.SET or set_policy == MemcacheSetRequest.ADD and old_entry is None or set_policy == MemcacheSetRequest.REPLACE and old_entry is not None:
                if old_entry is None or set_policy == MemcacheSetRequest.SET:
                    self._cache.set(key, set_value, item.expiration_time())
                    set_status = MemcacheSetResponse.STORED
                elif set_policy == MemcacheSetRequest.REPLACE:
                    self._cache.replace(key, set_value)
            response.add_set_status(set_status)

        return

    def _Dynamic_Delete(self, request, response):
        """Implementation of MemcacheService::Delete().

        Args:
            request: A MemcacheDeleteRequest.
            response: A MemcacheDeleteResponse.
        """
        for item in request.item_list():
            key = getKey(item.key(), request.name_space())
            entry = self._cache.get(key)
            delete_status = MemcacheDeleteResponse.DELETED
            if entry is None:
                delete_status = MemcacheDeleteResponse.NOT_FOUND
            else:
                self._cache.delete(key)
            response.add_delete_status(delete_status)

        return

    def _Increment(self, namespace, request):
        """Internal function for incrementing from a MemcacheIncrementRequest.

        Args:
            namespace: A string containing the namespace for the request,
                if any. Pass an empty string if there is no namespace.
            request: A MemcacheIncrementRequest instance.

        Returns:
            An integer or long if the offset was successful, None on error.
        """
        if not request.delta():
            return
        key = getKey(request.key(), namespace)
        value = self._cache.get(key)
        if value is None:
            if not request.has_initial_value():
                return
            flags, stored_value = google.appengine.api.memcache.TYPE_INT, str(request.initial_value())
        else:
            (flags, stored_value) = cPickle.loads(value)
        if flags == google.appengine.api.memcache.TYPE_INT:
            new_value = int(stored_value)
        elif flags == google.appengine.api.memcache.TYPE_LONG:
            new_value = long(stored_value)
        if request.direction() == MemcacheIncrementRequest.INCREMENT:
            new_value += request.delta()
        elif request.direction() == MemcacheIncrementRequest.DECREMENT:
            new_value -= request.delta()
        new_stored_value = cPickle.dumps([flags, str(new_value)])
        try:
            self._cache.set(key, new_stored_value)
        except:
            return

        return new_value

    def _Dynamic_Increment(self, request, response):
        """Implementation of MemcacheService::Increment().

        Args:
            request: A MemcacheIncrementRequest.
            response: A MemcacheIncrementResponse.
        """
        new_value = self._Increment(request.name_space(), request)
        if new_value is None:
            raise google.appengine.runtime.apiproxy_errors.ApplicationError(google.appengine.api.memcache.memcache_service_pb.MemcacheServiceError.UNSPECIFIED_ERROR)
        response.set_new_value(new_value)
        return

    def _Dynamic_BatchIncrement(self, request, response):
        """Implementation of MemcacheService::BatchIncrement().

        Args:
            request: A MemcacheBatchIncrementRequest.
            response: A MemcacheBatchIncrementResponse.
        """
        namespace = request.name_space()
        for request_item in request.item_list():
            new_value = self._Increment(namespace, request_item)
            item = response.add_item()
            if new_value is None:
                item.set_increment_status(MemcacheIncrementResponse.NOT_CHANGED)
            else:
                item.set_increment_status(MemcacheIncrementResponse.OK)
                item.set_new_value(new_value)

        return

    def _Dynamic_FlushAll(self, request, response):
        """Implementation of MemcacheService::FlushAll().

        Args:
            request: A MemcacheFlushRequest.
            response: A MemcacheFlushResponse.
        """
        self._cache.flush_all()

    def _Dynamic_Stats(self, request, response):
        """Implementation of MemcacheService::Stats().

        Args:
            request: A MemcacheStatsRequest.
            response: A MemcacheStatsResponse.
        """
        stats = response.mutable_stats()
        num_servers = 0
        hits_total = 0
        misses_total = 0
        byte_hits_total = 0
        items_total = 0
        bytes_total = 0
        time_total = 0

        def get_stats_value(stats_dict, key, _type=int):
            if key not in stats_dict:
                logging.warn("No stats for key '%s'." % key)
            return _type(stats_dict.get(key, '0'))

        for (server, server_stats) in self._cache.get_stats():
            num_servers += 1
            hits_total += get_stats_value(server_stats, 'get_hits')
            misses_total += get_stats_value(server_stats, 'get_misses')
            byte_hits_total += get_stats_value(server_stats, 'bytes_read')
            items_total += get_stats_value(server_stats, 'curr_items')
            bytes_total += get_stats_value(server_stats, 'bytes')
            time_total += get_stats_value(server_stats, 'time', float)

        stats.set_hits(hits_total)
        stats.set_misses(misses_total)
        stats.set_byte_hits(byte_hits_total)
        stats.set_items(items_total)
        stats.set_bytes(bytes_total)
        stats.set_oldest_item_age(time.time() - time_total / num_servers)