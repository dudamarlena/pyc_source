# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/nazrul/www/python/Contributions/apps/hybrid-access-control-system/hacs/defaults.py
# Compiled at: 2016-06-28 13:49:55
# Size of source mod 2**32: 679 bytes
from __future__ import unicode_literals
from django.apps import apps
from django.conf import settings
from django.utils._os import safe_join
from .globals import HACS_APP_NAME
__author__ = 'Md Nazrul Islam<connect2nazrul@gmail.com>'
HACS_CACHE_SETTING_NAME = 'default'
HACS_FALLBACK_URLCONF = settings.ROOT_URLCONF
HACS_GENERATED_URLCONF_DIR = safe_join(apps.get_app_config(HACS_APP_NAME).path, 'generated')
HACS_SERIALIZED_ROUTING_DIR = None
HACS_USER_OBJECT_QUERY_CALLABLE = 'hacs.utils.get_user_object'
HACS_DEVELOPMENT_MODE = False
HACS_AUTO_DISCOVER_URL_MODULE = ['admin.site.urls']