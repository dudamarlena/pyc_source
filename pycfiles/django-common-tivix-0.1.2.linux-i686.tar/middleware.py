# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/craterdome/work/django_common/lib/python2.7/site-packages/django_common/middleware.py
# Compiled at: 2012-03-11 19:20:35
from django.conf import settings
from django.http import HttpResponsePermanentRedirect, HttpResponseRedirect
WWW = 'www'

class WWWRedirectMiddleware(object):
    """
    Redirect requests for example from http://www.mysirw.com/* to http://mysite.com/*
    """

    def process_request(self, request):
        if settings.IS_PROD and request.get_host() != settings.DOMAIN_NAME:
            return HttpResponsePermanentRedirect('http%s://%s%s' % ('s' if request.is_secure() else '',
             settings.DOMAIN_NAME, request.get_full_path()))
        return


class SSLRedirectMiddleware(object):
    """Redirects all the requests that are non SSL to a SSL url"""

    def process_request(self, request):
        if not request.is_secure():
            return HttpResponseRedirect('https://%s%s' % (settings.DOMAIN_NAME, request.get_full_path()))
        else:
            return


class NoSSLRedirectMiddleware(object):
    """
    Redirects if a non-SSL required view is hit. This middleware assumes a SSL protected view has been decorated
    by the 'ssl_required' decorator (see decorators.py)

    Redirects to https for admin though only for PROD
    """
    __DECORATOR_INNER_FUNC_NAME = '_checkssl'

    def __is_in_admin(self, request):
        if request.path.startswith('/admin/'):
            return True
        return False

    def process_view(self, request, view_func, view_args, view_kwargs):
        if view_func.func_name != self.__DECORATOR_INNER_FUNC_NAME and not (self.__is_in_admin(request) and settings.IS_PROD) and request.is_secure():
            return HttpResponseRedirect('http://%s%s' % (settings.DOMAIN_NAME, request.get_full_path()))
        if self.__is_in_admin(request) and not request.is_secure() and settings.IS_PROD:
            return HttpResponseRedirect('https://%s%s' % (settings.DOMAIN_NAME, request.get_full_path()))