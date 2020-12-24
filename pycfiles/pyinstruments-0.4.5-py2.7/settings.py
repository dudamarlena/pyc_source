# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\pyinstruments\datastore\settings.py
# Compiled at: 2013-12-04 10:19:45
import os
from PyQt4.QtCore import QSettings
settings = QSettings('pyinstruments', 'pyinstruments')
MEDIA_ROOT = None
DATABASE_FILE = str(settings.value('database_file').toString())
if DATABASE_FILE == '':
    DATABASE_FILE = None
else:
    MEDIA_ROOT = os.path.splitext(DATABASE_FILE)[0]
DATABASES = {'default': {'ENGINE': 'django.db.backends.sqlite3', 
               'NAME': DATABASE_FILE, 
               'USER': '', 
               'PASSWORD': '', 
               'HOST': '', 
               'PORT': ''}}
DEBUG = False
TEMPLATE_DEBUG = DEBUG
ADMINS = (('samuel', 'your_email@example.com'), )
MANAGERS = ADMINS
ALLOWED_HOSTS = []
TIME_ZONE = 'Europe/London'
LANGUAGE_CODE = 'en-us'
SITE_ID = 1
USE_I18N = True
USE_L10N = True
USE_TZ = False
MEDIA_URL = ''
STATIC_ROOT = ''
STATIC_URL = '/static/'
STATICFILES_DIRS = ()
STATICFILES_FINDERS = ('django.contrib.staticfiles.finders.FileSystemFinder', 'django.contrib.staticfiles.finders.AppDirectoriesFinder')
SECRET_KEY = 'oa&7-w14!4e%%ngj#rgf*o$605uj7g_a#5^hmnly_&+wzxjvd('
TEMPLATE_LOADERS = ('django.template.loaders.filesystem.Loader', 'django.template.loaders.app_directories.Loader')
MIDDLEWARE_CLASSES = ('django.middleware.common.CommonMiddleware', 'django.contrib.sessions.middleware.SessionMiddleware',
                      'django.middleware.csrf.CsrfViewMiddleware', 'django.contrib.auth.middleware.AuthenticationMiddleware',
                      'django.contrib.messages.middleware.MessageMiddleware')
ROOT_URLCONF = 'datastore.urls'
WSGI_APPLICATION = 'datastore.wsgi.application'
TEMPLATE_DIRS = ()
INSTALLED_APPS = ('django.contrib.auth', 'django.contrib.contenttypes', 'django.contrib.sessions',
                  'django.contrib.sites', 'django.contrib.messages', 'django.contrib.staticfiles',
                  'django.contrib.admin', 'pyinstruments.curvestore', 'pyinstruments.datalogger',
                  'django_evolution')
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