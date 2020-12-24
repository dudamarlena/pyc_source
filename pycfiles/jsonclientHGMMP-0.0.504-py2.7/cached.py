# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\jsonclient\cached.py
# Compiled at: 2013-03-01 08:20:56
import logging
log = logging.getLogger(__name__)
all_cacheds = {}

class CachedLoader(object):

    def __init__(self, loader, cache_key):
        self.loader = loader
        self.cache_key = cache_key
        all_cacheds[cache_key] = self

    def refresh(self, request):
        obj = self.loader(request)
        request.globals.cache.set(self.cache_key, obj)
        return obj

    def get(self, request):
        obj = request.globals.cache.get_or_create(self.cache_key, lambda : self.loader(request))
        return obj


def refreshAllCacheds(request):
    for key, obj in all_cacheds.items():
        log.info('REFRESHING CACHED: %s', key)
        obj.refresh(request)