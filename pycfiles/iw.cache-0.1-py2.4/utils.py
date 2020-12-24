# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.3-fat/egg/iw/cache/utils.py
# Compiled at: 2007-12-05 09:41:22
"""
utils
"""
__docformat__ = 'restructuredtext'
import zope.component
from zope.component.interfaces import ComponentLookupError
from iw.cache.ramcache import IWRAMCache
from iw.cache.interfaces import IIWRAMCache, IIWMemcachedClient
import logging
LOG = logging.getLogger('iw.cache')

def get_storage(ns, maxAge=3600, storage=IIWRAMCache, servers=None):
    """return the correct cache method::

        >>> from iw.cache.testing import clearZCML
        >>> clearZCML()
        >>> from iw.cache.decorators import get_storage
        >>> cache = get_storage(ns='iw.cache')
        >>> cache is get_storage(ns='iw.cache') is not None
        True

    """
    if storage:
        obj = zope.component.queryUtility(storage, name=ns)
        if not obj and storage is IIWRAMCache:
            obj = zope.component.queryUtility(IIWMemcachedClient, name=ns)
    if not obj:
        zope.component.getUtility(storage, name=ns)
        raise ComponentLookupError('No cache found for the %s namespace' % ns)
    return obj


def purge(ns=None, storage=IIWRAMCache):
    """puge a cache for ns or all cache
    """
    if ns:
        cache = get_storage(ns, storage=storage)
        cache.invalidateAll()
        LOG.info('cache %s purged' % (cache,))
    else:
        caches = zope.component.getAllUtilitiesRegisteredFor(storage)
        for (name, cache) in caches:
            cache.invalidateAll()
            LOG.info('cache %s purged' % (cache,))