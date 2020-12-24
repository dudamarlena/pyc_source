# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/jgorset/Code/python/fandjango/fandjango/settings.py
# Compiled at: 2015-12-28 07:16:58
from warnings import warn
from django.conf import settings
FACEBOOK_APPLICATION_ID = getattr(settings, 'FACEBOOK_APPLICATION_ID')
FACEBOOK_APPLICATION_CANVAS_URL = getattr(settings, 'FACEBOOK_APPLICATION_CANVAS_URL', None)
FACEBOOK_AUTHORIZATION_REDIRECT_URL = getattr(settings, 'FACEBOOK_AUTHORIZATION_REDIRECT_URL', None)
FACEBOOK_APPLICATION_SECRET_KEY = getattr(settings, 'FACEBOOK_APPLICATION_SECRET_KEY')
FACEBOOK_APPLICATION_NAMESPACE = getattr(settings, 'FACEBOOK_APPLICATION_NAMESPACE')
DISABLED_PATHS = getattr(settings, 'FANDJANGO_DISABLED_PATHS', [])
ENABLED_PATHS = getattr(settings, 'FANDJANGO_ENABLED_PATHS', [])
AUTHORIZATION_DENIED_VIEW = getattr(settings, 'FANDJANGO_AUTHORIZATION_DENIED_VIEW', 'fandjango.views.authorization_denied')
FACEBOOK_APPLICATION_INITIAL_PERMISSIONS = getattr(settings, 'FACEBOOK_APPLICATION_INITIAL_PERMISSIONS', None)
FACEBOOK_APPLICATION_DOMAIN = getattr(settings, 'FACEBOOK_APPLICATION_DOMAIN', 'apps.facebook.com')
FANDJANGO_CACHE_SIGNED_REQUEST = getattr(settings, 'FACEBOOK_SIGNED_REQUEST_COOKIE', True)
FANDJANGO_SITE_URL = getattr(settings, 'FANDJANGO_SITE_URL', None)