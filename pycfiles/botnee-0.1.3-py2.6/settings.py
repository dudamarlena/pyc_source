# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/botnee/web/settings.py
# Compiled at: 2012-08-15 10:07:40
DEBUG = True
TEMPLATE_DEBUG = DEBUG
ADMINS = (('Tom Diethe', 'tdiethe@bmjgroup.com'), )
MANAGERS = ADMINS
DATABASES = {'default': {'ENGINE': 'django.db.backends.', 
               'NAME': '', 
               'USER': '', 
               'PASSWORD': '', 
               'HOST': '', 
               'PORT': ''}}
TIME_ZONE = 'Europe/London'
LANGUAGE_CODE = 'en-gb'
SITE_ID = 1
USE_I18N = True
USE_L10N = True
MEDIA_ROOT = ''
MEDIA_URL = ''
import os
STATIC_ROOT = os.path.join(os.path.dirname(__file__), 'staticfiles')
STATIC_URL = '/static/'
ADMIN_MEDIA_PREFIX = '/static/admin/'
STATICFILES_DIRS = (
 os.path.join(os.path.dirname(__file__), 'static'),
 os.path.join(os.path.dirname(__file__), 'static', 'css'))
STATICFILES_FINDERS = ('django.contrib.staticfiles.finders.FileSystemFinder', 'django.contrib.staticfiles.finders.AppDirectoriesFinder')
SECRET_KEY = '^_zxzw8zb4sgk*!8e%t406)pc+--^oy_78km%p+k19(=d5q7ge'
TEMPLATE_LOADERS = ('django.template.loaders.filesystem.Loader', 'django.template.loaders.app_directories.Loader')
MIDDLEWARE_CLASSES = ('django.middleware.common.CommonMiddleware', 'django.contrib.sessions.middleware.SessionMiddleware',
                      'django.contrib.auth.middleware.AuthenticationMiddleware',
                      'django.contrib.messages.middleware.MessageMiddleware')
ROOT_URLCONF = 'web.urls'
TEMPLATE_DIRS = (
 os.path.join(os.path.dirname(__file__), 'templates'),)
TEMPLATE_CONTEXT_PROCESSORS = ('django.core.context_processors.debug', 'django.core.context_processors.i18n',
                               'django.core.context_processors.media', 'django.core.context_processors.static',
                               'django.contrib.auth.context_processors.auth', 'django.contrib.messages.context_processors.messages',
                               'django.core.context_processors.request')
INSTALLED_APPS = ('django.contrib.auth', 'django.contrib.contenttypes', 'django.contrib.sessions',
                  'django.contrib.sites', 'django.contrib.messages', 'django.contrib.staticfiles',
                  'django.contrib.admin', 'web.interface', 'django_tables2')
LOGGING = {'version': 1, 
   'disable_existing_loggers': False, 
   'handlers': {'mail_admins': {'level': 'ERROR', 
                                'class': 'django.utils.log.AdminEmailHandler'}}, 
   'loggers': {'django.request': {'handlers': [
                                             'mail_admins'], 
                                  'level': 'ERROR', 
                                  'propagate': True}}}