# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/lib/python2.7/site-packages/key/auth.py
# Compiled at: 2011-11-17 12:47:53
from django.http import HttpResponse
from django.core import cache
from django.contrib.auth.models import *
from key.models import ApiKey
from key.signals import api_user_logged_in
from key import settings
import logging, hashlib

def _key_cache_key(auth_string):
    kstr = 'key.%s' % auth_string
    return hashlib.md5(kstr).hexdigest()


class ApiKeyAuthentication(object):

    def is_authenticated(self, request):
        auth_header = getattr(settings, 'AUTH_HEADER')
        auth_header = 'HTTP_%s' % auth_header.upper().replace('-', '_')
        auth_string = request.META.get(auth_header)
        if not auth_string:
            return False
        try:
            user = cache.get_cache('default').get(_key_cache_key(auth_string))
            if user:
                request.user = user
            else:
                key = ApiKey.objects.get(key=auth_string)
                request.user = key.profile.user
                cache.get_cache('default').set(_key_cache_key(key.key), request.user)
                if not key.profile.user.has_perm('key.can_use_api'):
                    return False
                key.login(request.META.get('REMOTE_ADDR'))
        except ApiKey.DoesNotExist:
            return False

        request.key = auth_string
        return True

    def challenge(self):
        auth_header = getattr(settings, 'AUTH_HEADER')
        resp = HttpResponse('Authorization Required')
        resp['WWW-Authenticate'] = 'KeyBasedAuthentication realm="API"'
        resp[auth_header] = 'Key Needed'
        resp.status_code = 401
        return resp