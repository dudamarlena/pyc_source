# uncompyle6 version 3.7.4
# Python bytecode 3.3 (3230)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: C:\Dev\python\django-quickview\docs\examplesite\examplesite\settings.py
# Compiled at: 2013-02-26 03:19:13
# Size of source mod 2**32: 5502 bytes
DEBUG = True
TEMPLATE_DEBUG = DEBUG
ADMINS = ()
MANAGERS = ADMINS
DATABASES = {'default': {'ENGINE': 'django.db.backends.sqlite3', 
             'NAME': 'test.db', 
             'USER': '', 
             'PASSWORD': '', 
             'HOST': '', 
             'PORT': ''}}
TIME_ZONE = 'America/Chicago'
LANGUAGE_CODE = 'en-us'
SITE_ID = 1
USE_I18N = True
USE_L10N = True
USE_TZ = True
MEDIA_ROOT = ''
MEDIA_URL = ''
import os
STATIC_ROOT = os.path.join(os.path.abspath(os.curdir), 'static')
if not os.path.exists(STATIC_ROOT):
    os.makedirs(STATIC_ROOT)
STATIC_URL = '/static/'
STATICFILES_DIRS = ()
STATICFILES_FINDERS = ('django.contrib.staticfiles.finders.FileSystemFinder', 'django.contrib.staticfiles.finders.AppDirectoriesFinder',
                       'django.contrib.staticfiles.finders.DefaultStorageFinder')
SECRET_KEY = '!d-(yf(bu*5n()5b0cit(ml342w608c5xahb6+^hm(#s9njza-'
TEMPLATE_LOADERS = ('django.template.loaders.filesystem.Loader', 'django.template.loaders.app_directories.Loader')
MIDDLEWARE_CLASSES = ('django.middleware.common.CommonMiddleware', 'django.contrib.sessions.middleware.SessionMiddleware',
                      'django.middleware.csrf.CsrfViewMiddleware', 'django.contrib.auth.middleware.AuthenticationMiddleware',
                      'django.contrib.messages.middleware.MessageMiddleware')
ROOT_URLCONF = 'examplesite.urls'
WSGI_APPLICATION = 'examplesite.wsgi.application'
TEMPLATE_DIRS = ()
TEMPLATE_CONTEXT_PROCESSORS = ('django.core.context_processors.request', 'django.core.context_processors.static')
INSTALLED_APPS = ('django.contrib.auth', 'django.contrib.contenttypes', 'django.contrib.sessions',
                  'django.contrib.sites', 'django.contrib.messages', 'django.contrib.staticfiles',
                  'quickview', 'friendslist')
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