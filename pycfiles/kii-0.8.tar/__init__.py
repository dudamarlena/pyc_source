# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/eliotberriot/Seafile/kii/kii_main/kii/__init__.py
# Compiled at: 2015-01-20 14:26:09
from django.utils.version import get_version
VERSION = (0, 8, 0, 'alpha', 0)
__version__ = get_version(VERSION)
PROJECT_URL = 'http://code.eliotberriot.com/kii/kii'
APPS = ('kii.locale', 'kii.hook', 'kii.permission', 'kii.user', 'kii.api', 'kii.glue',
        'kii.classify', 'kii.search', 'kii.file', 'kii.stream', 'kii.discussion',
        'kii.base_models', 'kii.activity', 'kii.app', 'kii.vendor')
APPS_CONFIGS = ()
for app in APPS:
    APPS_CONFIGS += (('.').join([app, 'apps.App']),)