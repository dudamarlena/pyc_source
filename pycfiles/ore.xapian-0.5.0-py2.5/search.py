# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.5-i386/egg/ore/xapian/search.py
# Compiled at: 2008-09-20 14:29:32
"""
$Id: $
"""
from zope import component, interface
from threading import local
import time, thread, xappy, interfaces, logging
log = logging.getLogger('ore.xapian')

class ConnectionHub(object):
    """
    search connection storage and retrieval with automatic
    reconnections with connection aging, connections are
    all thread local.
    """
    auto_refresh_delta = 20

    def __init__(self, index_path):
        self.store = local()
        self.modified = time.time()
        self.index_path = index_path

    def invalidate(self):
        self.modified = time.time()

    def get(self):
        conn = getattr(self.store, 'connection', None)
        now = time.time()
        if self.modified + self.auto_refresh_delta < now:
            self.modified = now
        if conn is None:
            self.store.connection = conn = xappy.SearchConnection(self.index_path)
            self.store.opened = now
        opened = getattr(self.store, 'opened')
        if opened < self.modified:
            if interfaces.DEBUG_LOG:
                log.warn('Reopening Connection')
            conn.reopen()
            self.store.opened = now
        return conn


class IndexSearch(object):
    interface.implements(interfaces.IIndexSearch)

    def __init__(self, index_path):
        self._index_path = index_path
        self.hub = ConnectionHub(index_path)

    def __call__(self):
        return self.hub.get()

    def invalidate(self):
        self.hub.invalidate()


def object(self):
    resolver_id = self.data['resolver'][0]
    resolver = component.getUtility(interfaces.IResolver, resolver_id)
    return resolver.resolve(self.id)


xappy.searchconnection.SearchResult.object = object