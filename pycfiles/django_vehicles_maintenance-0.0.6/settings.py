# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: C:\Users\Admin\Documents\GitHub\maintenance\django_vehicles_maintenance\maintenance\settings.py
# Compiled at: 2015-01-05 23:20:14
import os.path
DEBUG = True
TEMPLATE_DEBUG = DEBUG
ADMINS = ()
MANAGERS = ADMINS
MANTANIMIENTOS_DATA_PATH = os.environ['MANTANIMIENTOS_DATA_PATH']
DATABASES = {'default': {'ENGINE': 'django.db.backends.sqlite3', 
               'NAME': MANTANIMIENTOS_DATA_PATH + '\\maintenance_db', 
               'USER': '', 
               'PASSWORD': '', 
               'HOST': '', 
               'PORT': ''}}
TIME_ZONE = 'America/Mazatlan'
LANGUAGE_CODE = 'es-mx'
SITE_ID = 1
USE_I18N = True
USE_L10N = True
USE_TZ = True
MEDIA_ROOT = os.path.join(MANTANIMIENTOS_DATA_PATH, 'media')
MEDIA_URL = 'http://127.0.0.1:8000/media/'
STATIC_ROOT = ''
STATIC_URL = '/static/'
STATICFILES_DIRS = (
 os.path.join(os.path.abspath(os.path.dirname(__file__)), 'statics'),)
STATICFILES_FINDERS = ('django.contrib.staticfiles.finders.FileSystemFinder', 'django.contrib.staticfiles.finders.AppDirectoriesFinder')
SECRET_KEY = '_wl&amp;!%jvlou1**45&amp;tz!(vi_5=n!!3-jakcsyko18(363hfm)3'
TEMPLATE_LOADERS = ('django.template.loaders.filesystem.Loader', 'django.template.loaders.app_directories.Loader')
MIDDLEWARE_CLASSES = ('django.middleware.common.CommonMiddleware', 'django.contrib.sessions.middleware.SessionMiddleware',
                      'django.middleware.csrf.CsrfViewMiddleware', 'django.contrib.auth.middleware.AuthenticationMiddleware',
                      'django.contrib.messages.middleware.MessageMiddleware')
ROOT_URLCONF = 'maintenance.urls'
WSGI_APPLICATION = 'maintenance.wsgi.application'
TEMPLATE_DIRS = (
 os.path.join(os.path.abspath(os.path.dirname(__file__)), 'templates'),)
INSTALLED_APPS = ('django.contrib.auth', 'django.contrib.contenttypes', 'django.contrib.sessions',
                  'django.contrib.sites', 'django.contrib.messages', 'django.contrib.staticfiles',
                  'maintenance.main', 'south', 'django.contrib.admin')
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