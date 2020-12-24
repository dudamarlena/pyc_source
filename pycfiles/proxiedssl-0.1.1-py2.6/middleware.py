# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-x86_64/egg/proxiedssl/middleware.py
# Compiled at: 2012-01-05 12:50:39
from logging import getLogger
log = getLogger('proxiedssl')

class ProxiedSslWsgiMiddleware(object):

    def process_request(self, request):
        if 'HTTP_X_URL_SCHEME' in request.META:
            log.debug('setting wsgi.url_scheme to %s' % (
             request.META['HTTP_X_URL_SCHEME'].lower(),))
            request.environ['wsgi.url_scheme'] = request.META['HTTP_X_URL_SCHEME'].lower()
        elif 'HTTP_X_FORWARDED_PROTOCOL' in request.META:
            log.debug('setting wsgi.url_scheme to %s' % (
             request.META['HTTP_X_FORWARDED_PROTOCOL'].lower(),))
            request.environ['wsgi.url_scheme'] = request.META['HTTP_X_FORWARDED_PROTOCOL'].lower()
        else:
            log.debug('not setting wsgi.url_scheme: request.META=%s' % (
             unicode(request.META),))
            return
        log.debug('request.is_secure = %s' % (request.is_secure(),))