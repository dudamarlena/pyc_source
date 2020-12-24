# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: E:\workspace\django-template-project\source\conf\settings\main.py
# Compiled at: 2011-06-19 15:32:23
import os, sys
DEBUG = False
TEMPLATE_DEBUG = DEBUG
FORCE_SCRIPT_NAME = ''
PROJECT_ROOT = os.path.abspath('..')
sys.path.insert(0, os.path.abspath('apps'))
sys.path.insert(0, os.path.abspath(os.path.join('apps', 'ext')))
sys.path.insert(0, os.path.abspath('lib'))
sys.path.insert(0, os.path.abspath(os.path.join('lib', 'ext')))
ADMINS = (('Alerts', 'alert@example.com'), )
MANAGERS = ADMINS
TIME_ZONE = 'America/Chicago'
LANGUAGE_CODE = 'en-us'
SITE_ID = 1
USE_I18N = False
USE_L10N = True
MEDIA_ROOT = os.path.abspath(os.path.join(PROJECT_ROOT, 'media'))
MEDIA_URL = '/media/'
STATIC_ROOT = os.path.abspath(os.path.join(PROJECT_ROOT, 'static'))
STATIC_URL = '/static/'
ADMIN_MEDIA_PREFIX = '/static/admin/'
STATICFILES_DIRS = ()
STATICFILES_FINDERS = ('django.contrib.staticfiles.finders.FileSystemFinder', 'django.contrib.staticfiles.finders.AppDirectoriesFinder')
SECRET_KEY = '+hf(*)n6qwq#-0er!j$6y$zp2&2lb_k2a!t&6ksw0+)j8+)ly='
TEMPLATE_LOADERS = ('django.template.loaders.filesystem.Loader', 'django.template.loaders.app_directories.Loader')
MIDDLEWARE_CLASSES = ('django.middleware.common.CommonMiddleware', 'django.contrib.sessions.middleware.SessionMiddleware',
                      'django.middleware.csrf.CsrfViewMiddleware', 'django.contrib.auth.middleware.AuthenticationMiddleware',
                      'django.contrib.messages.middleware.MessageMiddleware')
ROOT_URLCONF = 'urls'
TEMPLATE_DIRS = ()
INSTALLED_APPS = ('django.contrib.auth', 'django.contrib.contenttypes', 'django.contrib.sessions',
                  'django.contrib.messages', 'django.contrib.staticfiles', 'django.contrib.admin')
LOGGING = {'version': 1, 
   'disable_existing_loggers': False, 
   'handlers': {'mail_admins': {'level': 'ERROR', 
                                'class': 'django.utils.log.AdminEmailHandler'}}, 
   'loggers': {'django.request': {'handlers': [
                                             'mail_admins'], 
                                  'level': 'ERROR', 
                                  'propagate': True}}}