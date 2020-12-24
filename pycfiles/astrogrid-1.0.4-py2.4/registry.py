# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.darwin-9.6.0-i386/egg/astrogrid/registry.py
# Compiled at: 2008-10-07 07:00:03
"""
Module to send queries to query the registry.

"""
__id__ = '$Id: registry.py 97 2007-05-29 15:51:00Z eddie $'
from astrogrid import acr
from watcherrors import watcherrors, needslogin

class Registry:
    """Perform queries on the registry"""
    __module__ = __name__

    @watcherrors
    def __init__(self):
        self.registry = acr.ivoa.registry

    def __getitem__(self, id):
        try:
            res = self.registry.getResource(id)
        except:
            res = self.search(id)

        return res

    @watcherrors
    def endpoint(self):
        """Returns the IVORN of the registry endpoint"""
        return self.registry.getSystemRegistryEndpoint()

    @watcherrors
    def keywordSearch(self, keywords, orValues=False):
        """Performs a keyword search on the registry"""
        return self.registry.keywordSearch(keywords, orValues)

    search = keywordSearch

    @watcherrors
    def searchCone(self, key=None):
        """Return all services which provide a cone interface"""
        xq = acr.ivoa.cone.getRegistryXQuery()
        return self._xquery(xq, key=key)

    @watcherrors
    def searchSiap(self, key=None):
        """Return all services which provide a siap interface"""
        xq = acr.ivoa.siap.getRegistryXQuery()
        return self._xquery(xq, key=key)

    @watcherrors
    def searchStap(self, key=None):
        """Return all services which provide a stap interface"""
        xq = acr.astrogrid.stap.getRegistryXQuery()
        return self._xquery(xq, key=key)

    def _xquery(self, xq, key=None, searchDescription=True):
        xq = 'let $cq := ' + xq + "\n\n        for $r in $cq\n        where contains($r/id,'%s') or contains($r/title,'%s') or contains($r/shortName,'%s')\n        return $r\n        "
        tres = self.registry.xquerySearch(xq % (key, key, key))
        return tres