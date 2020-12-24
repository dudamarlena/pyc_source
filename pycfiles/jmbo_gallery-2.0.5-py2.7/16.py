# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/gallery/tests/settings/16.py
# Compiled at: 2016-03-30 08:57:25
import os
USE_TZ = True
TIME_ZONE = 'Africa/Johannesburg'
DATABASES = {'default': {'ENGINE': 'django.db.backends.postgresql_psycopg2', 
               'NAME': 'jmbo', 
               'USER': 'postgres', 
               'PASSWORD': '', 
               'HOST': '', 
               'PORT': ''}}
INSTALLED_APPS = ('gallery', 'jmbo', 'photologue', 'category', 'likes', 'secretballot',
                  'pagination', 'layers', 'publisher', 'django.contrib.admin', 'django.contrib.auth',
                  'django.contrib.comments', 'django.contrib.contenttypes', 'django.contrib.sites',
                  'south')
ROOT_URLCONF = 'gallery.tests.urls'
MIDDLEWARE_CLASSES = ('django.middleware.common.CommonMiddleware', 'django.contrib.sessions.middleware.SessionMiddleware',
                      'django.middleware.csrf.CsrfViewMiddleware', 'django.contrib.auth.middleware.AuthenticationMiddleware',
                      'django.contrib.messages.middleware.MessageMiddleware', 'likes.middleware.SecretBallotUserIpUseragentMiddleware',
                      'pagination.middleware.PaginationMiddleware')
TEMPLATE_CONTEXT_PROCESSORS = ('django.contrib.auth.context_processors.auth', 'django.core.context_processors.debug',
                               'django.core.context_processors.i18n', 'django.core.context_processors.media',
                               'django.core.context_processors.static', 'django.core.context_processors.tz',
                               'django.core.context_processors.request', 'django.contrib.messages.context_processors.messages')
SITE_ID = 1
STATIC_URL = '/static/'
CELERY_ALWAYS_EAGER = True
BROKER_BACKEND = 'memory'
SECRET_KEY = 'SECRET_KEY'
STAGING = False
SOUTH_TESTS_MIGRATE = False
TEMPLATE_DIRS = (
 os.path.realpath(os.path.dirname(__file__)) + '/../templates/',)
LAYERS = {'layers': ['basic']}
TEMPLATE_LOADERS = ('layers.loaders.filesystem.Loader', 'django.template.loaders.filesystem.Loader',
                    'layers.loaders.app_directories.Loader', 'django.template.loaders.app_directories.Loader')
STATICFILES_FINDERS = ('layers.finders.FileSystemFinder', 'django.contrib.staticfiles.finders.FileSystemFinder',
                       'layers.finders.AppDirectoriesFinder', 'django.contrib.staticfiles.finders.AppDirectoriesFinder')