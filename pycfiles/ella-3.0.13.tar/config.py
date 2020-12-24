# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/xaralis/Workspace/elladev/ella/test_ella/settings/config.py
# Compiled at: 2013-09-22 07:03:20
ADMINS = ()
MANAGERS = ADMINS
DEBUG = False
TEMPLATE_DEBUG = DEBUG
DISABLE_CACHE_TEMPLATE = DEBUG
DATABASES = {'default': {'ENGINE': 'django.db.backends.sqlite3', 
               'NAME': ':memory:'}}
TEST_CORE_REDIS = PHOTOS_REDIS = {'db': 15}
TIME_ZONE = 'Europe/Prague'
LANGUAGE_CODE = 'en-us'
SITE_ID = 1
SECRET_KEY = '88b-01f^x4lh$-s5-hdccnicekg07)niir2g6)93!0#k(=mfv$'
CACHES = {'default': {'BACKEND': 'django.core.cache.backends.dummy.DummyCache'}}
USE_PRIORITIES = True