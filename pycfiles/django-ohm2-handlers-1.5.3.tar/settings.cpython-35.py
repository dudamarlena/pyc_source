# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/tonra/ohm2/Clients/ohm2/Entwicklung/ohm2-dev/application/website/apps/ohm2_handlers/socialstatistics/settings.py
# Compiled at: 2017-01-19 17:23:47
# Size of source mod 2**32: 1956 bytes
from django.conf import settings
from django.utils.translation import ugettext as _
import os
DEBUG = getattr(settings, 'DEBUG')
BASE_DIR = getattr(settings, 'BASE_DIR')
STRING_SINGLE = getattr(settings, 'STRING_SINGLE')
STRING_SHORT = getattr(settings, 'STRING_SHORT')
STRING_MEDIUM = getattr(settings, 'STRING_MEDIUM')
STRING_NORMAL = getattr(settings, 'STRING_NORMAL')
STRING_LONG = getattr(settings, 'STRING_LONG')
STRING_DOUBLE = getattr(settings, 'STRING_DOUBLE')
HOST = getattr(settings, 'HOST')
SUBDOMAINS = getattr(settings, 'SUBDOMAINS')
PROTOCOL = getattr(settings, 'PROTOCOL')
HOSTNAME = getattr(settings, 'HOSTNAME')
WEBSITE_URL = getattr(settings, 'WEBSITE_URL')
STATIC_URL = getattr(settings, 'STATIC_URL')
STATIC_ROOT = getattr(settings, 'STATIC_ROOT')
MEDIA_URL = getattr(settings, 'MEDIA_URL')
MEDIA_ROOT = getattr(settings, 'MEDIA_ROOT')
APP = 'OHM2_HANDLERS_SOCIALSTATISTICS_'
SAVE_RUN_EXCEPTIONS = getattr(settings, APP + 'SAVE_RUN_EXCEPTIONS', True)
SAVE_INPUT_EXCEPTIONS = getattr(settings, APP + 'SAVE_INPUT_EXCEPTIONS', True)
SAVE_METHOD_EXCEPTIONS = getattr(settings, APP + 'SAVE_METHOD_EXCEPTIONS', True)
TWITTER_CONSUMER_KEY = getattr(settings, APP + 'TWITTER_CONSUMER_KEY', '')
TWITTER_CONSUMER_SECRET = getattr(settings, APP + 'TWITTER_CONSUMER_SECRET', '')
TWITTER_AUTHORIZED_URL = getattr(settings, APP + 'TWITTER_AUTHORIZED_URL', None)
FACEBOOK_CLIENT_ID = getattr(settings, APP + 'FACEBOOK_CLIENT_ID', '')
FACEBOOK_APP_SECRET = getattr(settings, APP + 'FACEBOOK_APP_SECRET', '')
FACEBOOK_REDIRECT_URI = getattr(settings, APP + 'FACEBOOK_REDIRECT_URI', WEBSITE_URL)
FACEBOOK_SCOPE = getattr(settings, APP + 'FACEBOOK_SCOPE', 'manage_pages')
FACEBOOK_LOGIN_DIALOG_URL = getattr(settings, APP + 'FACEBOOK_LOGIN_DIALOG_URL', 'https://www.facebook.com/v2.8/dialog/oauth?')
FACEBOOK_GET_ACCESS_TOKEN_URL = getattr(settings, APP + 'FACEBOOK_GET_ACCESS_TOKEN_URL', 'https://graph.facebook.com/v2.8/oauth/access_token?')