# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/halit/pytr/pytrorg/src/settings.py
# Compiled at: 2012-09-09 12:59:37
import os
DEBUG = False
TEMPLATE_DEBUG = DEBUG
DOCUMENT_ROOT = os.path.realpath(os.path.dirname(__file__))
ADMINS = (('Halit Alptekin', 'info@halitalptekin.com'), )
MANAGERS = ADMINS
DATABASES = {'default': {'ENGINE': 'django.db.backends.sqlite3', 
               'NAME': 'site.db', 
               'USER': '', 
               'PASSWORD': '', 
               'HOST': '', 
               'PORT': ''}}
TIME_ZONE = 'Europe/Istanbul'
LANGUAGE_CODE = 'tr-TR'
SITE_ID = 1
USE_I18N = True
USE_L10N = True
USE_TZ = True
TEMPLATE_DIRS = (
 os.path.join(DOCUMENT_ROOT, 'templates'),)
MEDIA_ROOT = os.path.join(DOCUMENT_ROOT, 'media')
STATIC_ROOT = os.path.join(DOCUMENT_ROOT, 'static')
MEDIA_URL = '/media/'
STATIC_URL = '/static/'
STATICFILES_DIRS = (
 STATIC_ROOT,)
STATICFILES_FINDERS = ('django.contrib.staticfiles.finders.FileSystemFinder', 'django.contrib.staticfiles.finders.AppDirectoriesFinder')
SECRET_KEY = 'gz((*^mg(r32r^dhf7y_ycj3z#mxvl!=re2d7i8ks5a)+ed=eg'
TEMPLATE_LOADERS = ('django.template.loaders.filesystem.Loader', 'django.template.loaders.app_directories.Loader')
MIDDLEWARE_CLASSES = ('django.middleware.common.CommonMiddleware', 'django.contrib.sessions.middleware.SessionMiddleware',
                      'django.middleware.csrf.CsrfViewMiddleware', 'django.contrib.auth.middleware.AuthenticationMiddleware',
                      'django.contrib.messages.middleware.MessageMiddleware', 'pagination.middleware.PaginationMiddleware')
ROOT_URLCONF = 'urls'
WSGI_APPLICATION = 'wsgi.application'
INSTALLED_APPS = ('django.contrib.auth', 'django.contrib.contenttypes', 'django.contrib.sessions',
                  'django.contrib.sites', 'django.contrib.messages', 'django.contrib.staticfiles',
                  'django.contrib.admin', 'django.contrib.sitemaps', 'blog', 'tagging',
                  'pagination', 'sources')
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