# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/shodh/Projects/django_ginger/ginger/contrib/staging/middleware.py
# Compiled at: 2015-11-12 01:21:07
# Size of source mod 2**32: 732 bytes
from django.core.exceptions import ImproperlyConfigured
from django.shortcuts import redirect
from ginger.contrib.staging import views
from ginger.contrib.staging import conf
from django.conf import settings

class StagingMiddleware(object):

    def process_request(self, request):
        session_key = conf.get('SESSION_KEY')
        secret = conf.get('SECRET')
        value = request.get_signed_cookie(session_key, default=None)
        path_info = request.path_info.strip('/')
        if value != secret:
            return views.stage(request)
        if path_info == conf.get('RESET_URL').strip('/'):
            response = redirect('/')
            response.delete_cookie(session_key)
            return response