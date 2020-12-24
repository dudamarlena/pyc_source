# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: backstage/settings/backstage_settings.py
# Compiled at: 2014-06-27 19:07:27
"""Settings File for Django Backstage.  Borrows from Django's own settings.py as well as Mezzanine's settings.py;
Compartmentalizes settings into multiple sub-settings files, including 'database_','cache_','app_','local_'"""
from backstage.settings.django_settings import *
UWSGI_VASSALS = '/etc/uwsgi-emperor/vassals/'
NGINX_BASE = '/etc/nginx/'
try:
    from local.local_settings import Mezzanine
except:
    Mezzanine = True

if Mezzanine:
    from backstage.settings.mezzanine_settings import *
from backstage.settings.venue_settings import *
from backstage.settings.db_settings import DATABASES
TEMPLATE_DIRS = TEMPLATE_DIRS + venue_TEMPLATE_DIRS
TEMPLATE_CONTEXT_PROCESSORS = venue_TEMPLATE_CONTEXT_PROCESSORS + TEMPLATE_CONTEXT_PROCESSORS
from backstage.settings.app_settings import INSTALLED_APPS
from backstage.settings.static_settings import *
if Mezzanine:
    INSTALLED_APPS = INSTALLED_APPS + MEZZANINE_INSTALLED_APPS
    TEMPLATE_CONTEXT_PROCESSORS = TEMPLATE_CONTEXT_PROCESSORS + MEZZANINE_TEMPLATE_CONTEXT_PROCESSORS
    AUTHENTICATION_BACKENDS = MEZZANINE_AUTHENTICATION_BACKENDS + AUTHENTICATION_BACKENDS
    MIDDLEWARE_CLASSES = MEZZANINE_MIDDLEWARE_CLASSES_PREPEND + MIDDLEWARE_CLASSES + MEZZANINE_MIDDLEWARE_CLASSES_APPEND
    TEMPLATE_DIRS = TEMPLATE_DIRS + MEZZANINE_TEMPLATE_DIRS
    try:
        from backstage.settings.flexipage_settings import *
        if FLEXIPAGE:
            INSTALLED_APPS.append('flexipage')
    except:
        pass

if len(CACHES) > 0:
    MIDDLEWARE_CLASSES.insert(0, 'django.middleware.cache.UpdateCacheMiddleware')
    MIDDLEWARE_CLASSES.append('django.middleware.cache.FetchFromCacheMiddleware')
from misc_settings import *
if Mezzanine:
    try:
        from mezzanine.utils.conf import set_dynamic_settings
    except ImportError:
        pass
    else:
        set_dynamic_settings(globals())