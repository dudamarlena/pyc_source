# uncompyle6 version 3.6.7
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/pyowm/caches/lrucache.py
# Compiled at: 2018-12-21 14:52:45
# Size of source mod 2**32: 6014 bytes
__doc__ = '\nModule containing LRU cache related class\n'
from pyowm.abstractions import owmcache
from pyowm.commons import frontlinkedlist
from pyowm.utils import timeutils

class LRUCache(owmcache.OWMCache):
    """LRUCache"""
    _CACHE_MAX_SIZE = 20
    _ITEM_LIFETIME_MILLISECONDS = 600000

    def __init__(self, cache_max_size=_CACHE_MAX_SIZE, item_lifetime_millis=_ITEM_LIFETIME_MILLISECONDS):
        assert cache_max_size > 0 and item_lifetime_millis > 0, 'wrong cache init parameters'
        self._table = {}
        self._usage_recency = frontlinkedlist.FrontLinkedList()
        self._max_size = cache_max_size
        self._item_lifetime = item_lifetime_millis

    def get(self, request_url):
        """
        In case of a hit, returns the JSON string which represents the OWM web
        API response to the request being identified by a specific string URL
        and updates the recency of this request.

        :param request_url: an URL that uniquely identifies the request whose
            response is to be looked up
        :type request_url: str
        :returns: a JSON str in case of cache hit or ``None`` otherwise

        """
        try:
            cached_item = self._table[request_url]
            cur_time = timeutils.now('unix')
            if cur_time - cached_item['insertion_time'] > self._item_lifetime:
                self._clean_item(request_url)
                return
            else:
                cached_item['insertion_time'] = cur_time
                self._promote(request_url)
                return cached_item['data']
        except:
            return

    def set(self, request_url, response_json):
        """
        Checks if the maximum size of the cache has been reached and in case
        discards the least recently used item from 'usage_recency' and 'table';
        then adds the response_json to be cached to the 'table' dict using as
        a lookup key the request_url of the request that generated the value;
        finally adds it at the front of 'usage_recency'

        :param request_url: the request URL that uniquely identifies the
            request whose response is to be cached
        :type request_url: str
        :param response_json: the response JSON to be cached
        :type response_json: str

        """
        if self.size() == self._max_size:
            popped = self._usage_recency.pop()
            del self._table[popped]
        current_time = timeutils.now('unix')
        if request_url not in self._table:
            self._table[request_url] = {'data': response_json,  'insertion_time': current_time}
            self._usage_recency.add(request_url)
        else:
            self._table[request_url]['insertion_time'] = current_time
            self._promote(request_url)

    def _promote(self, request_url):
        """
        Moves the cache item specified by request_url to the front of the
        'usage_recency' list
        """
        self._usage_recency.remove(request_url)
        self._usage_recency.add(request_url)

    def _clean_item(self, request_url):
        """
        Removes the specified item from the cache's datastructures

        :param request_url: the request URL
        :type request_url: str

        """
        del self._table[request_url]
        self._usage_recency.remove(request_url)

    def clean(self):
        """
        Empties the cache

        """
        self._table.clear()
        for item in self._usage_recency:
            self._usage_recency.remove(item)

    def size(self):
        """
        Returns the number of elements that are currently stored into the cache

        :returns: an int

        """
        return len(self._table)

    def __repr__(self):
        return '<%s.%s - size=%s, max size=%s, item lifetime=%s>' % (
         __name__, self.__class__.__name__, str(self.size()),
         self._max_size, self._item_lifetime)