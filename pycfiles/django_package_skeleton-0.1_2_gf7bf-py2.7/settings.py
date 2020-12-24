# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/tests/settings.py
# Compiled at: 2012-01-14 11:36:57
import os
ROOT = os.path.dirname(__file__)
DEBUG = True
TEMPLATE_DEBUG = DEBUG
ADMINS = ()
MANAGERS = ADMINS
DATABASES = {'default': {'ENGINE': 'django.db.backends.sqlite3', 
               'NAME': os.path.join(ROOT, 'database.db'), 
               'USER': '', 
               'PASSWORD': '', 
               'HOST': '', 
               'PORT': ''}}
TIME_ZONE = 'America/Chicago'
LANGUAGE_CODE = 'en-us'
SITE_ID = 1
USE_I18N = True
USE_L10N = True
MEDIA_ROOT = ''
MEDIA_URL = ''
STATIC_ROOT = ''
STATIC_URL = '/static/'
ADMIN_MEDIA_PREFIX = '/static/admin/'
STATICFILES_DIRS = (
 os.path.join(ROOT, 'static'),)
STATICFILES_FINDERS = ('django.contrib.staticfiles.finders.FileSystemFinder', 'django.contrib.staticfiles.finders.AppDirectoriesFinder')
SECRET_KEY = '4et6(22#@lgie4wogk)6um6^jklpkk0!z-l%uj&kvs*u2xrvfj%'
TEMPLATE_LOADERS = ('django.template.loaders.filesystem.Loader', 'django.template.loaders.app_directories.Loader')
MIDDLEWARE_CLASSES = ('django.middleware.common.CommonMiddleware', 'django.contrib.sessions.middleware.SessionMiddleware',
                      'django.middleware.csrf.CsrfViewMiddleware', 'django.contrib.auth.middleware.AuthenticationMiddleware',
                      'django.contrib.messages.middleware.MessageMiddleware')
ROOT_URLCONF = 'tests.urls'
TEMPLATE_DIRS = (
 os.path.join(ROOT, 'templates'),)
INSTALLED_APPS = ('django.contrib.auth', 'django.contrib.contenttypes', 'django.contrib.sessions',
                  'django.contrib.sites', 'django.contrib.messages', 'django.contrib.staticfiles',
                  'django.contrib.admin', 'tests.blogs')
FIXTURE_DIRS = (
 os.path.join(ROOT, 'fixtures'),)
LOGIN_REDIRECT_URL = '/'
LOGGING = {'version': 1, 
   'disable_existing_loggers': False, 
   'handlers': {'mail_admins': {'level': 'ERROR', 
                                'class': 'django.utils.log.AdminEmailHandler'}}, 
   'loggers': {'django.request': {'handlers': [
                                             'mail_admins'], 
                                  'level': 'ERROR', 
                                  'propagate': True}}}