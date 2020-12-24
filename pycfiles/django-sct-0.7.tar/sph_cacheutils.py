# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/herbert/dev/python/sctdev/simpleproject/simpleproject/../../communitytools/sphenecoll/sphene/community/sph_cacheutils.py
# Compiled at: 2012-03-17 12:42:14
from django.core.cache import cache
from django.conf import settings

def get_cache_group_id(group_code, timeout=None):
    """ Get id for group_code that is stored in cache.
        This id is supposed to be included in cache key
        for all items from specific group.
    """
    cache_group_key = '%s-%s-GROUP' % (settings.CACHE_MIDDLEWARE_KEY_PREFIX, group_code)
    group_id = cache.get(cache_group_key, 1)
    if not timeout:
        timeout = cache.default_timeout * 2
    cache.set(cache_group_key, group_id, timeout)
    return group_id


def invalidate_cache_group_id(group_code):
    """ Invalidation of group is in fact only incrementation of group_id
    """
    cache_group_key = '%s-%s-GROUP' % (settings.CACHE_MIDDLEWARE_KEY_PREFIX, group_code)
    try:
        cache.incr(cache_group_key)
    except ValueError:
        pass