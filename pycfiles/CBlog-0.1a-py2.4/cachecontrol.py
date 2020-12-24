# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/cblog/cachecontrol.py
# Compiled at: 2006-12-06 04:38:10
import logging, cherrypy
from time import strftime, gmtime, time
from turbogears import config
log = logging.getLogger('cblog.controllers')

class ExpiresFilter(cherrypy.filters.basefilter.BaseFilter):
    __module__ = __name__

    def before_finalize(self):
        if config.get('expiresFilter.on', False) or cherrypy.response.headerMap.get('Pragma') != 'no-cache':
            log.debug('Caching disabled!')
            return
            log.debug('Adding cache control headers.')
            cache_seconds = config.get('expiresFilter.seconds ', 300)
            cherrypy.response.headerMap['Last-Modified'] = strftime('%a, %d %b %Y %H:%M:%S GMT', gmtime(time()))
            cherrypy.response.headerMap['Expires'] = strftime('%a, %d %b %Y %H:%M:%S GMT', gmtime(time() + cache_seconds))
        cherrypy.response.headerMap['Vary'] = 'Cookie'


def strongly_expire(func):
    """Decorator that sends headers that instruct browsers and proxies not to cache.
    """

    def newfunc(*args, **kwargs):
        cherrypy.response.headerMap['Expires'] = 'Thu, 01 Jan 1970 00:00:00 GMT'
        cherrypy.response.headerMap['Cache-Control'] = 'no-store, no-cache, must-revalidate, post-check=0, pre-check=0'
        cherrypy.response.headerMap['Pragma'] = 'no-cache'
        return func(*args, **kwargs)

    return newfunc