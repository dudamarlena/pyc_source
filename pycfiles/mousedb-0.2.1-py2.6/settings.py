# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/mousedb/settings.py
# Compiled at: 2010-08-21 21:05:33
import os.path
PROJECT_DIR = os.path.dirname(__file__)
LANGUAGE_CODE = 'en-us'
SITE_ID = 1
USE_I18N = True
MEDIA_ROOT = os.path.join(PROJECT_DIR, 'media')
MEDIA_URL = '/mousedb-media/'
ADMIN_MEDIA_PREFIX = '/mousedb-media/admin-media/'
SECRET_KEY = 'ci%^08ig-0qu*&b(kz_=n6lvbx*puyx6=8!yxzm0+*z)w@7+%6'
LOGIN_URL = '/mousedb/accounts/login/'
TEMPLATE_LOADERS = ('django.template.loaders.filesystem.load_template_source', 'django.template.loaders.app_directories.load_template_source')
MIDDLEWARE_CLASSES = ('django.middleware.common.CommonMiddleware', 'django.contrib.sessions.middleware.SessionMiddleware',
                      'django.contrib.auth.middleware.AuthenticationMiddleware',
                      'django.middleware.csrf.CsrfViewMiddleware', 'django.contrib.messages.middleware.MessageMiddleware')
ROOT_URLCONF = 'mousedb.urls'
TEMPLATE_DIRS = (
 os.path.join(PROJECT_DIR, 'templates'),)
TEMPLATE_CONTEXT_PROCESSORS = ('django.core.context_processors.auth', 'django.core.context_processors.debug',
                               'django.core.context_processors.i18n', 'django.core.context_processors.media',
                               'django.contrib.messages.context_processors.messages',
                               'mousedb.context_processors.group_info')
INSTALLED_APPS = ('django.contrib.auth', 'django.contrib.contenttypes', 'django.contrib.sessions',
                  'django.contrib.messages', 'django.contrib.admin', 'mousedb.data',
                  'mousedb.animal', 'mousedb.timed_mating', 'mousedb.groups', 'django.contrib.admin',
                  'ajax_select', 'south')
MESSAGE_STORAGE = 'django.contrib.messages.storage.fallback.FallbackStorage'
AJAX_LOOKUP_CHANNELS = {'animal': ('mousedb.animal.lookups', 'AnimalLookup'), 
   'animal-male': ('mousedb.animal.lookups', 'AnimalLookupMale'), 
   'animal-female': ('mousedb.animal.lookups', 'AnimalLookupFemale')}
try:
    from localsettings import *
except ImportError:
    print 'localsetting could not be imported'