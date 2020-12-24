# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/shodh/Projects/django_ginger/ginger/staging/middleware.py
# Compiled at: 2014-10-06 10:05:25
from django.conf import settings
from django.shortcuts import redirect
from ginger.staging import views
from django.core.exceptions import MiddlewareNotUsed, ImproperlyConfigured
from ginger.staging import conf

class StagingMiddleware(object):
    """
    Configuration check is added here and not apps.py because it should be run if and only if
    middleware has been added
    """

    def __init__(self):
        secret = conf.STAGING_SECRET
        if not secret:
            raise ImproperlyConfigured('No STAGING_SECRET found in settings.py')

    def process_request(self, request):
        value = request.get_signed_cookie(conf.STAGING_SESSION_KEY, default=None)
        path_info = request.path_info.strip('/')
        if value != conf.STAGING_SECRET:
            return views.stage(request)
        else:
            if path_info == 'staging_reset':
                response = redirect('/')
                response.delete_cookie(conf.STAGING_SESSION_KEY)
                return response
            return