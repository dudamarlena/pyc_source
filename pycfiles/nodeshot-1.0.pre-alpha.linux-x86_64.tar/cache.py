# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python2.7/dist-packages/nodeshot/core/base/cache.py
# Compiled at: 2014-06-06 06:09:45
"""
utilities for caching
"""
from django.core.cache import cache

def cache_delete_pattern_or_all(pattern):
    if hasattr(cache, 'delete_pattern'):
        cache.delete_pattern(pattern)
    else:
        cache.clear()


def cache_by_group(view_instance, view_method, request, args, kwargs):
    """
    Cache view response by media type and user group.
    The cache_key is constructed this way: "{view_name:path.group.media_type}"
    EG: "MenuList:/api/v1/menu/.public.application/json"
    Possible groups are:
        * public
        * superuser
        * the rest are retrieved from DB (registered, community, trusted are the default ones)
    """
    if request.user.is_anonymous():
        group = 'public'
    elif request.user.is_superuser:
        group = 'superuser'
    else:
        try:
            group = request.user.groups.all().order_by('-id').first().name
        except IndexError:
            group = 'public'

    key = '%s:%s.%s.%s' % (
     view_instance.__class__.__name__,
     request.META['PATH_INFO'],
     group,
     request.accepted_media_type)
    return key