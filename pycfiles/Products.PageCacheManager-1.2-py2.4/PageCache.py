# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.3-i386/egg/Products/PageCacheManager/PageCache.py
# Compiled at: 2008-04-16 05:00:11
"""Failover RAM cache for content.  Stores both html and headers.

Portions of this file were derived from from Zope 2.8's standard cache managers,
specifically, ~Zope/lib/python/Products/StandardCacheManagers/RAMCacheManager.py
The code has been modified considerably.  The modified code falls under the
Zope Public License, version 2.0.  See LICENSE.txt.
"""
from Products.CMFCore.CachingPolicyManager import createCPContext
from Products.CacheSetup.cmf_utils import _checkConditionalGET as CSCheckConditionalGET
from thread import allocate_lock
import Globals, copy, time
try:
    from Products.CMFCore.utils import _checkConditionalGET as CMFCheckConditionalGET
except:
    CMFCheckConditionalGET = None

_marker = []

class PageCacheEntry:
    """Represents the cache for one template view of one content object.
    """
    __module__ = __name__

    def __init__(self, data, headers):
        self.data = data
        self.headers = headers
        self.created = time.time()
        self.access_count = 0


class PageCacheEntries:
    """Represents the cache for one page template
    """
    __module__ = __name__
    hits = 0
    misses = 0

    def __init__(self, template_path, context_path):
        self.template_path = template_path
        self.context_path = context_path
        self.entries = {}

    def getEntry(self, index):
        return self.entries.get(index, _marker)

    def setEntry(self, index, data, headers):
        self.entries[index] = PageCacheEntry(data, headers)

    def delEntry(self, index):
        try:
            del self.entries[index]
        except KeyError:
            pass


class PageCache:
    __module__ = __name__
    max_age = 0

    def __init__(self):
        self.cache = {}
        self.writelock = allocate_lock()
        self.next_cleanup = 0

    def initSettings(self, settings):
        self.writelock.acquire()
        try:
            self.threshold = settings['threshold']
            self.cleanup_interval = settings['cleanup_interval']
            self.max_age = settings['max_age']
            self.active = settings.get('active', 'on_always')
        finally:
            self.writelock.release()

    def isActive(self):
        if self.active == 'on_always':
            return True
        if self.active == 'on_in_production' and not Globals.DevelopmentMode:
            return True
        return False

    def getPageCacheEntries(self, template, REQUEST, create=0):
        """Find or create the associated PageCacheEntries object.
        
        Remember to lock writelock when calling with the 'create' flag.
        """
        cache = self.cache
        template_path = template.getPhysicalPath()
        context_path = REQUEST.ACTUAL_URL
        oc = cache.get((template_path, context_path), None)
        if oc is None:
            if create:
                self.writelock.acquire()
                try:
                    cache[(template_path, context_path)] = oc = PageCacheEntries(template_path, context_path)
                finally:
                    self.writelock.release()
            else:
                return
        return oc

    def countAllEntries(self):
        """Return the count of all cache entries.
        """
        count = 0
        for oc in self.cache.values():
            count = count + len(oc.entries)

        return count

    def countAccesses(self):
        """Return a mapping of (n) -> # of entries accessed (n) times.
        """
        counters = {}
        for oc in self.cache.values():
            for entry in oc.entries.values():
                access_count = entry.access_count
                counters[access_count] = counters.get(access_count, 0) + 1

        return counters

    def clearAccessCounters(self):
        """Clear access_count for each cache entry.
        """
        self.writelock.acquire()
        try:
            for oc in self.cache.values():
                for entry in oc.entries.values():
                    entry.access_count = 0

        finally:
            self.writelock.release()

    def deleteEntriesAtOrBelowThreshold(self, threshold_access_count):
        """Delete entries that haven't been accessed recently.
        """
        self.writelock.acquire()
        try:
            for (p, oc) in self.cache.items():
                for (agindex, entry) in oc.entries.items():
                    if entry.access_count <= threshold_access_count:
                        del oc.entries[agindex]

                if len(oc.entries) < 1:
                    del self.cache[p]

        finally:
            self.writelock.release()

    def deleteStaleEntries(self):
        """Delete entries that have expired.
        """
        if self.max_age > 0:
            self.writelock.acquire()
            try:
                min_created = time.time() - self.max_age
                for (p, oc) in self.cache.items():
                    for (agindex, entry) in oc.entries.items():
                        if entry.created < min_created:
                            del oc.entries[agindex]

                    if len(oc.entries) < 1:
                        del self.cache[p]

            finally:
                self.writelock.release()

    def cleanup(self):
        """Remove cache entries.
        """
        self.deleteStaleEntries()
        new_count = self.countAllEntries()
        if new_count > self.threshold:
            counters = self.countAccesses()
            priorities = counters.items()
            if len(priorities) > 0:
                priorities.sort()
                access_count = 0
                for (access_count, effect) in priorities:
                    new_count = new_count - effect
                    if new_count <= self.threshold:
                        break

                self.deleteEntriesAtOrBelowThreshold(access_count)
                self.clearAccessCounters()
        self.writelock.acquire()
        try:
            self.next_cleanup = time.time() + self.cleanup_interval
        finally:
            self.writelock.release()

    def getCacheReport(self):
        """Report on the contents of the cache.
        """
        rval = []
        for oc in self.cache.values():
            size = 0
            ac = 0
            views = []
            for entry in oc.entries.values():
                size = size + entry.size
                ac = ac + entry.access_count
                view = entry.view_name or '<default>'
                if view not in views:
                    views.append(view)

            views.sort()
            info = {'template_path': ('/').join(oc.template_path), 'context_path': ('/').join(oc.context_path), 'hits': oc.hits, 'misses': oc.misses, 'size': size, 'counter': ac, 'views': views, 'entries': len(oc.entries)}
            rval.append(info)

        return rval

    def invalidate(self, template, REQUEST=None):
        """Invalidate the cache entries that apply to template.
        """
        template_path = template.getPhysicalPath()
        if REQUEST is not None:
            context_path = REQUEST.ACTUAL_URL
        else:
            context_path = None
        self.writelock.acquire()
        try:
            for (p, oc) in self.cache.items():
                tp = oc.template_path
                if tp[:len(template_path)] == template_path:
                    if context_path is None or context_path == oc.context_path[:len(context_path)]:
                        del self.cache[p]

        finally:
            self.writelock.release()
        return

    def _check_for_cleanup(self, check_size):
        now = time.time()
        if self.next_cleanup <= now or check_size and self.countAllEntries() > self.threshold:
            self.cleanup()

    def get(self, template, REQUEST, etag, default):
        """Get a cache entry or return default.
        """
        self._check_for_cleanup(check_size=False)
        oc = self.getPageCacheEntries(template, REQUEST)
        if oc is None:
            return default
        entry = oc.getEntry(etag)
        if entry is _marker:
            return default
        if self.max_age > 0 and entry.created < time.time() - self.max_age:
            self.writelock.acquire()
            try:
                oc.delEntry(etag)
            finally:
                self.writelock.release()
            return default
        self.writelock.acquire()
        try:
            oc.hits = oc.hits + 1
            entry.access_count = entry.access_count + 1
        finally:
            self.writelock.release()
        return (entry.data, copy.copy(entry.headers))

    def purge(self):
        """Clear the cache.
        """
        self.writelock.acquire()
        try:
            del self.cache
            self.cache = {}
            self.next_cleanup = 0
        finally:
            self.writelock.release()

    def set(self, template, REQUEST, etag, data, headers):
        """Set a cache entry.
        """
        self._check_for_cleanup(check_size=True)
        oc = self.getPageCacheEntries(template, REQUEST, create=1)
        self.writelock.acquire()
        try:
            oc.setEntry(etag, data, headers)
            oc.misses = oc.misses + 1
        finally:
            self.writelock.release()

    def ZCache_invalidate(self, ob):
        """Invalidate the cache entries that apply to ob.
        """
        return self.invalidate(ob)

    def ZCache_get(self, ob, view_name='', keywords=None, mtime_func=None, default=None):
        """Get a cache entry or return default.
        """
        if not self.isActive():
            ob.REQUEST.RESPONSE.setHeader('X-PageCache', 'OFF')
            return default
        etag = self._getETag(ob, keywords, check_conditional_get=True)
        if ob.REQUEST.RESPONSE.getStatus() == 304:
            return ''
        if etag is None:
            ob.REQUEST.RESPONSE.setHeader('X-PageCache', 'NO-ETAG')
            return default
        cached_page = self.get(ob, ob.REQUEST, etag, default)
        if cached_page == default:
            ob.REQUEST.RESPONSE.setHeader('X-PageCache', 'MISS')
            return cached_page
        (data, headers) = cached_page
        ob.REQUEST.RESPONSE.use_HTTP_content_compression = headers['use_http_content_compression']
        del headers['use_http_content_compression']
        for (k, v) in headers.items():
            if k == 'ETag':
                ob.REQUEST.RESPONSE.setHeader(k, v, literal=1)
            else:
                ob.REQUEST.RESPONSE.setHeader(k, v)

        ob.REQUEST.RESPONSE.setHeader('X-PageCache', 'HIT')
        return data

    def ZCache_set(self, ob, data, view_name='', keywords=None, mtime_func=None):
        """Set a cache entry.
        """
        if not self.isActive():
            return
        template = ob
        etag = self._getETag(ob, keywords, check_conditional_get=False)
        if etag is None:
            return
        headers = ob.REQUEST.RESPONSE.headers
        status = headers.get('status', None)
        if status:
            status = status.split(' ')[0]
            if not status == '200':
                return
        headers = copy.copy(headers)
        headers['use_http_content_compression'] = ob.REQUEST.RESPONSE.use_HTTP_content_compression
        self.set(template, ob.REQUEST, etag, data, headers)
        return

    def _getETag(self, ob, keywords, time=None, check_conditional_get=None):
        """Return ETag for content object, view method and keywords.

        Slightly modified from CachingPolicyManager's method
        getModTimeAndETag in that it ignores the getEnable304s
        setting.
        """
        object = ob.getParentNode()
        view = ob.getId()
        etag = None
        pcs = getattr(object, 'portal_cache_settings', None)
        if pcs:
            request = object.REQUEST
            member = pcs.getMember()
            (rule, header_set) = pcs.getRuleAndHeaderSet(request, object, view, member)
            if rule and header_set.getEtag():
                expr_context = rule._getExpressionContext(request, object, view, member, keywords, time)
                if header_set.getEnable304s() and check_conditional_get:
                    CSCheckConditionalGET(ob, keywords, rule, header_set, expr_context)
                etag = header_set.getPageCacheKey(expr_context)
            return etag
        cpm = getattr(object, 'caching_policy_manager', None)
        if not cpm:
            return
        if check_conditional_get:
            CMFCheckConditionalGET(ob, keywords)
        expr_context = createCPContext(object, view, keywords, time=time)
        for (policy_id, policy) in cpm.listPolicies():
            if policy.testPredicate(expr_context):
                headers = policy.getHeaders(expr_context)
                if headers:
                    for (key, value) in headers:
                        lk = key.lower()
                        if lk == 'etag':
                            return value

        return