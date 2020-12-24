# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: backstage/settings/static_settings.py
# Compiled at: 2014-06-27 19:07:27
"""STATIC SETTINGS
settings for static content
These are default somewhat sane values that
almost certainly will not work off-the shelf and
should be modified """
import sys, os
STATIC_ROOT = '/data/www/static/'
STATIC_URL = 'http://127.0.0.1/static/'
WEBUSER = 'backstage'
STATICFILES_DIRS = []
MEDIA_ROOT_BASE = '/data/www/content/site/'
MEDIA_URL = 'http://127.0.0.1/media/'
ADMIN_MEDIA_PREFIX = STATIC_URL + 'grappelli/'
AUTOCOMPLETE_MEDIA_PREFIX = '/media/autocomplete'