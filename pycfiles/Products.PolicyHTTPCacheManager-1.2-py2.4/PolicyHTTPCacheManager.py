# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.3-i386/egg/Products/PolicyHTTPCacheManager/PolicyHTTPCacheManager.py
# Compiled at: 2008-04-16 07:07:54
"""
Policy HTTP cache manager --
  Use CMF Caching Policy Manager to add caching headers to
  the response so that downstream caches will cache
  according to a common policy.

$Id: PolicyHTTPCacheManager.py 62766 2008-04-16 11:07:45Z wichert $
"""
from zope.interface import implements
import time
from cgi import escape
from OFS.Cache import Cache, CacheManager
from OFS.SimpleItem import SimpleItem
from Globals import DTMLFile, InitializeClass
from Products.CMFCore.utils import _setCacheHeaders
from Products.CMFCore.utils import _ViewEmulator
from Products.CMFCore.utils import getToolByName
from Products.CMFCore.interfaces import ICachingPolicy
from Products.CMFCore.interfaces import ICachingPolicyManager
from Products.CMFCore.interfaces.CachingPolicyManager import CachingPolicyManager as z2ICachingPolicyManager
VIEW_METATYPES = ('Page Template', 'DTML Method', 'DTML Document', 'Filesystem DTML Method',
                  'Filesystem Page Template')

class PolicyHTTPCache(Cache):
    __module__ = __name__

    def __init__(self):
        self.hit_counts = {}

    def initSettings(self, kw):
        self.__dict__.update(kw)

    def ZCache_invalidate(self, ob):
        st = getToolByName(ob, 'portal_squid', None)
        if st is None:
            return 'Squid Tool not found, invalidation ignored.'
        results = st.pruneObject(ob)
        phys_path = ob.getPhysicalPath()
        if self.hit_counts.has_key(phys_path):
            del self.hit_counts[phys_path]
        results = [ ('\t').join(map(str, line)) for line in results ]
        return 'Server response(s): ' + (';').join(results)

    def ZCache_get(self, ob, view_name, keywords, mtime_func, default):
        """Just return the default.

        This cache isn't meant to cache anything (sic). The goal is to
        be able to set headers just before the response gets returned.
        """
        return default

    def ZCache_set(self, ob, data, view_name, keywords, mtime_func):
        """Set the cache headers if the response is 200 or 304.
        """
        REQUEST = ob.REQUEST
        RESPONSE = REQUEST.RESPONSE
        phys_path = ob.getPhysicalPath()
        if self.hit_counts.has_key(phys_path):
            hits = self.hit_counts[phys_path]
        else:
            self.hit_counts[phys_path] = hits = [
             0]
        headers = getattr(RESPONSE, 'headers', {})
        l_headers = dict([ (h.lower(), h) for h in headers.keys() ])
        if self.remove_last_modified:
            key = l_headers.get('last-modified')
            if key is not None:
                del headers[key]
        key = l_headers.get('status', None)
        if key is None:
            return
        status = headers.get(key, None)
        if status is None:
            return
        status = status.split(' ')[0]
        if status not in ('200', '304'):
            return
        hits[0] += 1
        if ob.meta_type in VIEW_METATYPES:
            view = ob
        else:
            view = _ViewEmulator(view_name).__of__(ob)
        _setCacheHeaders(view, extra_context=keywords)
        return


caches = {}

class PolicyHTTPCacheManager(CacheManager, SimpleItem):
    """
    A Cache Manager that delegates to the Caching Policy Manager
    """
    __module__ = __name__
    implements(ICachingPolicyManager)
    __implements__ = z2ICachingPolicyManager
    __ac_permissions__ = (
     (
      'View management screens', ('getSettings', 'manage_main', 'manage_stats', 'getCacheReport', 'sort_link')), ('Change cache managers', ('manage_editProps', ), ('Manager', )))
    manage_options = ({'label': 'Properties', 'action': 'manage_main'}, {'label': 'Statistics', 'action': 'manage_stats'}) + CacheManager.manage_options + SimpleItem.manage_options
    meta_type = 'Policy HTTP Cache Manager'

    def __init__(self, ob_id):
        self.id = ob_id
        self.title = ''
        self._settings = {'remove_last_modified': 1}
        self.__cacheid = '%s_%f' % (id(self), time.time())

    def getId(self):
        """ Object Identifier
        """
        return self.id

    ZCacheManager_getCache__roles__ = ()

    def ZCacheManager_getCache(self):
        cacheid = self.__cacheid
        try:
            return caches[cacheid]
        except KeyError:
            cache = PolicyHTTPCache()
            cache.initSettings(self._settings)
            caches[cacheid] = cache
            return cache

    def getSettings(self):
        """Configured Settings
        """
        return self._settings.copy()

    manage_main = DTMLFile('dtml/propsPolicy', globals())

    def manage_editProps(self, title, settings=None, REQUEST=None):
        """Change Settings
        """
        if settings is None:
            settings = REQUEST
        self.title = str(title)
        remove_last_modified = settings.get('remove_last_modified') and 1 or 0
        self._settings = {'remove_last_modified': remove_last_modified}
        cache = self.ZCacheManager_getCache()
        cache.initSettings(self._settings)
        if REQUEST is not None:
            return self.manage_main(self, REQUEST, manage_tabs_message='Properties changed.')
        return

    manage_stats = DTMLFile('dtml/statsPolicy', globals())

    def _getSortInfo(self):
        """
        Returns the value of sort_by and sort_reverse.
        If not found, returns default values.
        """
        req = self.REQUEST
        sort_by = req.get('sort_by', 'hits')
        sort_reverse = int(req.get('sort_reverse', 1))
        return (sort_by, sort_reverse)

    def getCacheReport(self):
        """
        Returns the list of objects in the cache, sorted according to
        the user's preferences.
        """
        (sort_by, sort_reverse) = self._getSortInfo()
        c = self.ZCacheManager_getCache()
        rval = []
        for (path, (hits,)) in c.hit_counts.items():
            rval.append({'path': ('/').join(path), 'hits': hits})

        if sort_by:
            rval.sort(lambda e1, e2, sort_by=sort_by: cmp(e1[sort_by], e2[sort_by]))
            if sort_reverse:
                rval.reverse()
        return rval

    def sort_link(self, name, id):
        """
        Utility for generating a sort link.
        """
        (sort_by, sort_reverse) = self._getSortInfo()
        url = self.absolute_url() + '/manage_stats?sort_by=' + id
        newsr = 0
        if sort_by == id:
            newsr = not sort_reverse
        url = url + '&sort_reverse=' + (newsr and '1' or '0')
        return '<a href="%s">%s</a>' % (escape(url, 1), escape(name))


InitializeClass(PolicyHTTPCacheManager)
manage_addPolicyHTTPCacheManagerForm = DTMLFile('dtml/addPolicy', globals())

def manage_addPolicyHTTPCacheManager(self, id, REQUEST=None):
    """Add Policy HTTP Cache Manager
    """
    self._setObject(id, PolicyHTTPCacheManager(id))
    if REQUEST is not None:
        return self.manage_main(self, REQUEST)
    return