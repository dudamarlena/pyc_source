# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/lucaswiman/opensource/django-predicate/tests/testapp/settings.py
# Compiled at: 2016-02-13 23:54:37
import os, re
DEBUG = True
TEMPLATE_DEBUG = DEBUG
ADMINS = ()
MANAGERS = ADMINS
_BACKEND = os.environ.get('DB_BACKEND', 'sqlite3')
_ENVNAME = re.sub('\\W', '', os.environ.get('TOXENV', ''))
if _BACKEND == 'sqlite3':
    DATABASES = {'default': {'ENGINE': 'django.db.backends.sqlite3', 
                   'NAME': 'test%s.db' % _ENVNAME, 
                   'USER': '', 
                   'PASSWORD': '', 
                   'HOST': '', 
                   'PORT': ''}}
elif _BACKEND == 'postgresql_psycopg2':
    DATABASES = {'default': {'NAME': 'predicatedb%s' % _ENVNAME, 
                   'ENGINE': 'django.db.backends.postgresql_psycopg2', 
                   'USER': 'django', 
                   'PASSWORD': 'secret'}}
TIME_ZONE = 'America/Chicago'
LANGUAGE_CODE = 'en-us'
SITE_ID = 1
USE_I18N = True
USE_L10N = True
USE_TZ = True
MEDIA_ROOT = ''
MEDIA_URL = ''
STATIC_ROOT = ''
STATIC_URL = '/static/'
STATICFILES_DIRS = ()
STATICFILES_FINDERS = ('django.contrib.staticfiles.finders.FileSystemFinder', 'django.contrib.staticfiles.finders.AppDirectoriesFinder')
SECRET_KEY = '#0&k@ztj55vtu(7pr1x2#n1)g9msz$ebqj1o_b2@+qw!+2^(zu'
TEMPLATE_LOADERS = ('django.template.loaders.filesystem.Loader', 'django.template.loaders.app_directories.Loader')
MIDDLEWARE_CLASSES = ('django.middleware.common.CommonMiddleware', 'django.contrib.sessions.middleware.SessionMiddleware',
                      'django.middleware.csrf.CsrfViewMiddleware', 'django.contrib.auth.middleware.AuthenticationMiddleware',
                      'django.contrib.messages.middleware.MessageMiddleware')
ROOT_URLCONF = 'testapp.urls'
WSGI_APPLICATION = 'testapp.wsgi.application'
TEMPLATE_DIRS = ()
INSTALLED_APPS = ('tests.testapp', )
LOGGING = {'version': 1, 
   'disable_existing_loggers': False, 
   'filters': {'require_debug_false': {'()': 'django.utils.log.RequireDebugFalse'}}, 
   'handlers': {'mail_admins': {'level': 'ERROR', 
                                'filters': [
                                          'require_debug_false'], 
                                'class': 'django.utils.log.AdminEmailHandler'}}, 
   'loggers': {'django.request': {'handlers': [
                                             'mail_admins'], 
                                  'level': 'ERROR', 
                                  'propagate': True}}}